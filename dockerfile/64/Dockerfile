FROM debian:wheezy

MAINTAINER Sylvain Boily "sboily@avencall.com"

ENV DEBIAN_FRONTEND noninteractive

RUN echo 'deb http://mirror.xivo.io/debian/ xivo-dev main' > /etc/apt/sources.list.d/xivo.list
RUN echo 'deb http://ftp.ca.debian.org/debian/ wheezy-backports main' > /etc/apt/sources.list.d/wheezy-backports.list
RUN apt-key adv --recv-keys --keyserver pgp.mit.edu 0x2D0C2DE0DFB0B268
RUN apt-get -yqq update
RUN apt-get -yqq install simple-cdd \
                    syslinux-common \
                    netpbm \
                    sudo \
                    mtools \
                    dosfstools

RUN groupadd builder
RUN useradd -r -g builder -G sudo -s /bin/bash -u 1000 builder
RUN mkdir -p /home/builder/
RUN echo 'builder ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/builder
RUN chmod 440 /etc/sudoers.d/builder
ADD . /home/builder/xivo-install-cd
RUN chown -R builder.builder /home/builder/

WORKDIR /home/builder/xivo-install-cd
USER builder

CMD ./build-iso.sh
