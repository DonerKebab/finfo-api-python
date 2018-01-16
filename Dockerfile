# https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/
FROM tiangolo/uwsgi-nginx-flask:flask


# Update the package repository
RUN apt-get update; apt-get upgrade -y

# # install & configure locals 
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales -qq \
# 	&& DEBIAN_FRONTEND=noninteractive locale-gen en_GB.UTF-8 en_gb \
# 	&& DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales \
# 	&& DEBIAN_FRONTEND=noninteractive dpkg-reconfigure locales \
# 	&& DEBIAN_FRONTEND=noninteractive locale-gen C.UTF-8 \
# 	&& DEBIAN_FRONTEND=noninteractive /usr/sbin/update-locale LANG=C.UTF-8


# ENV LANG C.UTF-8
# ENV LANGUAGE C.UTF-8
# ENV LC_ALL C.UTF-8


# configure nginx
COPY nginx.conf /etc/nginx/conf.d/nginx.conf 


# move to app dir
COPY ./app /app
WORKDIR /app


# install dependencies 
RUN pip install -r requirements/production.txt