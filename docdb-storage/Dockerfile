FROM debian:jessie
MAINTAINER Brett Viren <brett.viren@gmail.com>

# Install packages
RUN apt-get update && \
    apt-get -y install python openssh-server pwgen perl git && \
    mkdir -p /var/run/sshd && \
    sed -i "s/UsePrivilegeSeparation.*/UsePrivilegeSeparation no/g" /etc/ssh/sshd_config

ADD set_root_pw.sh /set_root_pw.sh
ADD run.sh /run.sh

RUN mkdir -p /var/lib/docdb/installation/
COPY install_docdb.py /var/lib/docdb/installation/install_docdb.py

## Apparently globs don't actually work in the version of Docker I'm using
# COPY *.template  /var/lib/docdb/installation/
COPY  apache-site.template		/var/lib/docdb/installation/
COPY  mysql-secgrp.sql.template		/var/lib/docdb/installation/
COPY  ProjectMessages.pm.template	/var/lib/docdb/installation/
COPY  my.cnf.template			/var/lib/docdb/installation/
COPY  ProjectGlobals.pm.template	/var/lib/docdb/installation/
COPY  ProjectRoutines.pm.template	/var/lib/docdb/installation/
COPY  mysql-init.sql.template		/var/lib/docdb/installation/
COPY  ProjectHelp.xml.template		/var/lib/docdb/installation/

RUN chmod +x /*.sh

ENV AUTHORIZED_KEYS **None**



EXPOSE 22
CMD ["/run.sh"]
