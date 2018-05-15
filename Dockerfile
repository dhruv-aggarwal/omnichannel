FROM python:2.7.15

ENV product omnichannel
ENV repo_root /www/omnichannel
ENV requirements_file $repo_root/requirements.lock
ENV secrets_file $repo_root/settings.py
ENV uwsgi_file $repo_root/uwsgi.ini

WORKDIR $repo_root

# Get and install required packages.
RUN apt-get update && apt-get install -y -q \
    build-essential \
    python-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    wget && \
    apt-get autoremove -y && \
    apt-get clean && \
    apt-get autoclean && \
    echo -n > /var/lib/apt/extended_states && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/share/man/?? && \
    rm -rf /usr/share/man/??_*

# It is an image dedicated to python.
# To avoid version conflicts of packages installed from apt-get
# and pip install, it is better to not install pip from apt-get.
# Also, python-pip ships with pip 1.5.4 :'(
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py
RUN rm get-pip.py

# Install python deps
RUN apt-get update && apt-get install -y curl git libmysqlclient-dev \
    libssl-dev libffi-dev libpq-dev libjpeg-dev && \
    pip install cffi

COPY requirements.lock .
RUN pip install -r requirements.lock

COPY . $repo_root

ADD docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
EXPOSE 1786
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

