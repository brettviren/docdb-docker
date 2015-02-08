FROM debian:jessie
MAINTAINER Brett Viren <brett.viren@gmail.com>

# Install packages
RUN apt-get update && \
    apt-get -y install python openssh-server pwgen perl git && \
    mkdir -p /var/run/sshd && \
    sed -i "s/UsePrivilegeSeparation.*/UsePrivilegeSeparation no/g" /etc/ssh/sshd_config

ADD set_root_pw.sh /set_root_pw.sh
ADD run.sh /run.sh
RUN chmod +x /*.sh

ENV AUTHORIZED_KEYS **None**

VOLUME  ["/etc/mysql", "/var/lib/mysql", "/var/lib/docdb" ]

EXPOSE 22
CMD ["/run.sh"]
