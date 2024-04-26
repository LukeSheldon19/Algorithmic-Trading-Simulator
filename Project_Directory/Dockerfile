FROM python:3.12
MAINTAINER PeStory@clarku.edu

# Directories for the source code
RUN mkdir -p /usr/src/django/djangoproject

# Install OS dependencies
RUN apt-get update && apt-get install -y postgresql-client

# Next, install the Python modules
ADD requirements.txt /usr/src/django/requirements.txt
RUN pip install -r /usr/src/django/requirements.txt

WORKDIR /usr/src/django/djangoproject
ENV PYTHONPATH=/usr/src/django/djangoproject
ENV DJANGO_SETTINGS_MODULE='djangoproject.settings'
CMD ["/usr/src/django/setup_and_start.sh"]
