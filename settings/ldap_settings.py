from base import *

# == LDAP ==
AUTH_LDAP_SERVER_URI = "ldap://10.10.20.220:389"

import ldap
from django_auth_ldap.config import GroupOfUniqueNamesType
from django_auth_ldap.config import LDAPSearch

AUTH_LDAP_BIND_DN = "cn=Directory Manager"
AUTH_LDAP_BIND_PASSWORD = "ab12cd"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,ou=staff,dc=insigma,dc=com", \
        ldap.SCOPE_SUBTREE, "(cn=%(user)s)")
AUTH_LDAP_USER_BASE_SEARCH = LDAPSearch("ou=users,ou=staff,dc=insigma,dc=com", \
        ldap.SCOPE_SUBTREE, "(objectClass=organizationalPerson)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,ou=staff,dc=insigma,dc=com", \
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfUniqueNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType()
AUTH_LDAP_MIRROR_GROUPS = True

LDAP_USER_BASE_DN = "ou=users,ou=staff,dc=insigma,dc=com"
LDAP_GROUP_BASE_DN = "ou=groups,ou=staff,dc=insigma,dc=com"
LDAP_USER_DEFAULT_GROUPS = ('IOT.ALL', 'confluence-users', 'jira-users', 'jira-developers')
LDAP_INACTIVE_BASE_DN = 'ou=inactive,ou=staff,dc=insigma,dc=com'

AUTHENTICATION_BACKENDS += ('django_auth_ldap.backend.LDAPBackend',)