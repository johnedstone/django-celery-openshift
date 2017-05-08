unset SOURCE_REPOSITORY_URL
unset SOURCE_REPOSITORY_REF
unset CONTEXT_DIR
unset API_TOKEN_POC
unset OPENSHIFT_MASTER_POC

unset API_TOKEN_NP
unset OPENSHIFT_MASTER_NP

unset API_TOKEN_PRD
unset OPENSHIFT_MASTER_PRD

unset DATABASE_ENGINE
unset DATABASE_SERVICE_NAME
unset DATABASE_NAME
unset DATABASE_USER
unset SOME_POSTGRES_SERVICE_HOST
unset SOME_POSTGRES_SERVICE_PORT
unset APPLICATION_DOMAIN
unset REDIS_SERVER

export SOURCE_REPOSITORY_URL='git@github repository'
export SOURCE_REPOSITORY_REF='a branch'
export CONTEXT_DIR='directory of project'
export OPENSHIFT_MASTER_POC='example.servername.fqdn:8443'
export API_TOKEN_POC=''

export OPENSHIFT_MASTER_NP='example.servername.fqdn:8443'
export API_TOKEN_NP=''

export OPENSHIFT_MASTER_PRD='example.servername.fqdn:8443'
export API_TOKEN_PRD=''

export APPLICATION_DOMAIN='vanity.fqdn'

# For development, not for openshift
export REDIS_SERVER=<standalone.redis.fqdn>
export SOME_POSTGRES_SERVICE_HOST=<standalone.postgres.fqdn>

# vim: set ai et ts=4 sw=4 sts=4
