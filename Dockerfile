FROM kylemanna/openvpn

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update

RUN apk add --no-cache --update python3 socat && \
    apk add py3-pip && \
    pip3 install --ignore-installed pipenv && \
    pip3 install twisted && \
    mkdir -p /app

WORKDIR /app

COPY Pipfile /app/Pipfile

RUN apk add -t install_dep python3-dev build-base
RUN pipenv install
RUN apk del -r install_dep

COPY learn-address.sh /app/learn-address.sh
COPY route_listener.py /app/route_listener.py
RUN chmod -R 777 /app/learn-address.sh

CMD /usr/bin/python3 /app/route_listener.py