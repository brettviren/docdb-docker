# https://docs.docker.com/articles/using_supervisord/

FROM debian:jessie
MAINTAINER Brett Viren <brett.viren@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV INITRD No

RUN apt-get update && \
  apt-get -y install git pwgen python \
                     supervisor \
  	     	     openssh-server \
  	     	     apache2 apache2-utils \
                     mysql-server mysql-client \
                     libcgi-untaint-perl libxml-sax-perl libxml-perl \
		     libxml-twig-perl libxml-grove-perl libdatetime-perl libdigest-sha-perl libdigest-perl 
RUN apt-get -y remove --purge libcgi-pm-perl && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir /var/run/sshd

# https://github.com/allisson/docker-mysql
RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf
ADD set-mysql-password.sh /tmp/set-mysql-password.sh
RUN /bin/sh /tmp/set-mysql-password.sh

RUN sed -i -e"s/^PermitRootLogin without-password/PermitRootLogin yes/" /etc/ssh/sshd_config
RUN echo "root:root" | chpasswd
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

RUN a2dissite 000-default
RUN a2enmod rewrite
RUN a2enmod cgi

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor /var/log/mysql


# DocDB
RUN mkdir -p /var/lib/docdb
RUN git clone https://github.com/brettviren/docdb-install.git /var/lib/docdb/installation


EXPOSE 22 80 3306
CMD ["/usr/bin/supervisord"]
