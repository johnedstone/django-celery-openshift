## Creating an openshift project

Two templates are provided: 

 * openshift/templates/parse_image_data_with_celery.yml
 * openshift/templates/parse_image_data_no_celery.yml

```
# first source a file such as example_env.sh
oc new-project parse-image-data
oc secrets new-sshauth sshsecret --ssh-privatekey=$HOME/.ssh/<your private key>
oc secret add serviceaccount/builder secrets/sshsecret
oc new-app \
    --param=SOURCE_REPOSITORY_URL=${SOURCE_REPOSITORY_URL} \
    --param=SOURCE_REPOSITORY_REF=${SOURCE_REPOSITORY_REF} \
    --param=CONTEXT_DIR=${CONTEXT_DIR} \
    --param=APPLICATION_DOMAIN=${APPLICATION_DOMAIN} \
    --param=OPENSHIFT_MASTER_POC=${OPENSHIFT_MASTER_POC} \
    --param=API_TOKEN_POC=${API_TOKEN_POC} \
    --param=API_TOKEN_NP=${API_TOKEN_NP} \
    --param=API_TOKEN_PRD=${API_TOKEN_PRD} \
    --param=OPENSHIFT_MASTER_NP=${OPENSHIFT_MASTER_NP} \
    --param=OPENSHIFT_MASTER_PRD=${OPENSHIFT_MASTER_PRD} \
    -f openshift/templates/parse_image_data_with_celery.yml

# Later
oc get pods
NAME                       READY     STATUS      RESTARTS   AGE
parse-image-data-1-build   0/1       Completed   0          21h
parse-image-data-1-grbi1   1/1       Running     0          21h
postgresql-1-e72f2         1/1       Running     0          21h
project.celery-1-1p7u7     1/1       Running     0          21h
redis-1-3504l              1/1       Running     0          21h

```

### To do ...
Add flower container for monitoring.

## Development (notes for runserver)

### Using Openshift postgres image in development:

```
docker run -p 5432:5432 --name some-postgres -e POSTGRESQL_USER=postgres_user -e POSTGRESQL_DATABASE=postgres_db -e POSTGRESQL_PASSWORD=mysecretpassword -d rhscl/postgresql-95-rhel7:9.5
docker run -it --rm --link some-postgres:postgres_alias rhscl/postgresql-95-rhel7:9.5 psql -h postgres_alias -U postgres_user -d postgres_db
```
### Populate postgres

One can populate the postgres with this custom management command

```
python manage.py migrate
python manage.py populate_database_with_build_configs
```

In the openshift template, this is accomplished in the run script.

### Using https://hub.docker.com/_/postgres/
Not using, using Openshift image

```
docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres:9.4.11
docker run -it --rm --link some-postgres:postgres postgres:9.4.11 psql -h postgres -U postgres
```

### Start Redis
More on redis in the celery README

```
docker run -d -p 6379:6379 --name some-redis rhscl/redis-32-rhel7:latest
docker run -it --link some-redis:redis --rm rhscl/redis-32-rhel7:latest redis-cli -h redis -p 6379 ping
PONG

docker run -it --link some-redis:redis --rm rhscl/redis-32-rhel7:latest redis-cli -h redis -p 6379
```

###### vim: ai et ts=4 sw=4 sts=4 nu
