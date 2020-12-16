FROM osixia/openldap:1.4.0

WORKDIR /system
ADD create_ou_users.ldif /system
ADD init.sh /system