# -*- coding: utf-8 -*-
from flask import current_app

from elasticsearch import Elasticsearch as PyElasticSearch, RequestsHttpConnection

from .utils import get_config

import json


class ElasticSearch(object):
  
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)


    def init_app(self, app):

        port = get_config(app)['PORT']
        host = get_config(app)['HOST']

        try:
            # connect to ElasticSearch
            app.extensions['elasticsearch'] = PyElasticSearch(host, timeout=60, port=port,
                                                              connection_class=RequestsHttpConnection)
            app.extensions['elasticsearch'].cluster.health()
        
        except Exception as e:
           print('Can not connect to Elasticsearch')

            
    def __getattr__(self, item):
        if not 'elasticsearch' in current_app.extensions.keys():
            raise Exception('not initialised')
        return getattr(current_app.extensions['elasticsearch'], item)


    def check_cluster(self):
        try:
            # check active ElasticSearch cluster
            current_app.extensions['elasticsearch'].cluster.health()
        
        except Exception as e:
            if current_app.sentry:
                current_app.sentry.captureMessage('Can not connect to active cluster, switching to backup')

            print('Can not connect to active cluster, switching to backup')            
            ic = current_app.config[self.inactive_cluster]
            current_app.extensions['elasticsearch'] = PyElasticSearch(ic, timeout=60, port=get_config(current_app)['PORT'])


    def search(self, *args, **kwargs):

        page = kwargs['body'].pop('page', 1)
        body = current_app.extensions['elasticsearch'] \
            .search(index=current_app.config.get('ELASTICSEARCH_INDEX'), *args, **kwargs)

        results = body.get('hits', [])
        results['from'] = kwargs['body'].get('from', -1)
        results['limit'] = kwargs['body'].get('size', -1)
        results['page'] = page

        return results

    def get(self, *args, **kwargs):

        return current_app.extensions['elasticsearch'] \
            .get(index=current_app.config.get('ELASTICSEARCH_INDEX', None), _source=True, *args, **kwargs)

    def count(self, *args, **kwargs):

        return current_app.extensions['elasticsearch'] \
            .count(index=current_app.config.get('ELASTICSEARCH_INDEX', None), *args, **kwargs)['count']

    def status(self, *args, **kwargs):

        return current_app.extensions['elasticsearch'] \
            .indices.status(index=current_app.config.get('ELASTICSEARCH_INDEX', None), *args, **kwargs)

    def filtered_search(self, *args, **kwargs):


        doc_type = kwargs.get('doc_type', False)
        query_params = kwargs.get('args', False)
        filters = kwargs.get('filters', False)
        aggregates = kwargs.get('aggregates', False)
        sort = kwargs.get('sort', False)
        aggs = kwargs.get('aggs', False)

        # disable pagination
        pagination_off = kwargs.get('pagination_off', False)

        # base query
        query = {}

        # pagination
        if not pagination_off:
            page = query_params.get('page', 1)
            limit = query_params.get('limit', 2000)

            query = {
                "from": (page - 1) * limit,
                "size": limit,
                "page": page
            }
        else:
            query["size"] = 2000

        # filters
        if filters:
            query["query"] = {
                "filtered": {
                    "filter": {
                        "and": list(filters)
                    }
                }
            }

        # sort by
        if sort:
            query["sort"] = list(sort)

        # aggregators
        if aggs:
            query["aggs"] = aggs

        # source control
        if '_source' in query_params:
            query['_source'] = query_params['_source'].split(",")

        return self.search(body=query, doc_type=doc_type, filter_path=['hits.hits._source', 'hits.total'])

    def publish(self, query, _type, es_index=None):
        try:
            docs = []
            bulk_max = 1000

            for item in query:
                docs.append({
                    "index": {
                        "_index": es_index,
                        "_type": _type,
                    }
                })

                docs.append(item)
                if len(docs) >= bulk_max:
                    current_app.extensions['elasticsearch'].bulk(index=es_index, body=docs)

                    docs[:] = []

            if docs:
                current_app.extensions['elasticsearch'].bulk(index=es_index, body=docs)

        except Exception as e:
            print("PUBLISH ERROR {} {}".format(type(e), str(e)))
        
