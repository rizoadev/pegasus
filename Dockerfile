FROM python:3.9-buster


# =========================
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN echo "Asia/Jakarta" > /etc/timezone
RUN dpkg-reconfigure tzdata
RUN date

RUN apt-get update -y
RUN apt-get install -y \
    supervisor \
    nginx \
    redis-server \
    curl \
    git

RUN rm -rf /var/lib/apt/lists/*
WORKDIR /home


RUN pip install --no-cache-dir --upgrade pip

COPY ./app/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN rm -rf /root/.cache/pip

COPY conf/nginx /etc/nginx
COPY conf/redis.conf /etc/redis.conf
COPY conf/supervisord /etc/supervisord

COPY ./app /home

CMD supervisord -c /etc/supervisord/supervisord.conf
