# aker-events-notifier
FROM python:3.6.5

# Needed to see log output immediately
ENV PYTHONUNBUFFERED 1

# Install and setup project dependencies
RUN apt-get update && \
    apt-get install -y supervisor

# Create directories
RUN mkdir -p logs
RUN mkdir -p /var/log/supervisor # supervisor log directory

# Create the working directory
# https://docs.docker.com/engine/reference/builder/#workdir
WORKDIR /code

# Add the requirements file
ADD requirements.txt /code/requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

# Install packages required by project
RUN pip install -r requirements.txt

# Add the wait-for-it file to utils
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /utils/wait-for-it.sh
RUN chmod u+x /utils/wait-for-it.sh

# Add specific supervisor config for the notifier
ADD notifier_supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Add all remaining contents to the image
ADD . /code
