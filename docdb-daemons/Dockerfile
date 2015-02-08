FROM debian:jessie
MAINTAINER Brett Viren <brett.viren@gmail.com>

# packages
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
  apt-get -y install supervisor git apache2 apache2-utils \
                     mysql-server mysql-client \
		     pwgen \
                     libcgi-untaint-perl libxml-sax-perl libxml-perl \
		     libxml-grove-perl libdatetime-perl libdigest-sha-perl libdigest-perl


# Supervirosd prep
ADD supervisord-apache2.conf /etc/supervisor/conf.d/supervisord-apache2.conf
ADD supervisord-mysqld.conf /etc/supervisor/conf.d/supervisord-mysqld.conf
#ADD supervisord-sshd.conf /etc/supervisor/conf.d/supervisord-sshd.conf
ADD start-apache2.sh /start-apache2.sh
ADD start-mysqld.sh /start-mysqld.sh
#ADD start-sshd.sh /start-sshd.sh

# Mysql prep
ADD my.cnf /etc/mysql/conf.d/my.cnf
RUN rm -rf /var/lib/mysql/*

# Apache prep
ADD apache_default /etc/apache2/sites-available/000-default.conf
RUN a2enmod rewrite
RUN a2enmod cgi

# Main entry point
ADD create_mysql_admin_user.sh /create_mysql_admin_user.sh
ADD run.sh /run.sh
RUN chmod 755 /*.sh

# Must be set at run time
# ENV AUTHORIZED_KEYS **None**

EXPOSE 80
CMD ["/run.sh"]
