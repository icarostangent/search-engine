FROM ubuntu:22.04

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y install build-essential curl autotools-dev automake libevent-dev libssl-dev zlib1g-dev jq

RUN apt-get -y install git && \
    git clone https://gitlab.torproject.org/tpo/core/tor.git &&\
    cd tor && \
    ./autogen.sh &&\
    ./configure --disable-asciidoc &&\
    make && make install

COPY . .

HEALTHCHECK --interval=5s --timeout=1s --retries=5 \
    CMD test "$(curl -x socks5h://localhost:9050 -s https://check.torproject.org/api/ip | jq '.IsTor')" == 'true'

CMD ["tor", "-f", "torrc"]
