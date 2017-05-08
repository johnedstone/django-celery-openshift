### Comments on using Celery and Django with Openshift

References:

* http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
* https://docs.djangoproject.com/en/1.11/releases/1.7/#standalone-scripts

Note:

* To do: move tasks into an app directory (too complicated at the moment)
* Currently using django 11.x and celery 4.x
* Currently running celery and beat together
* Two templates provided:
    * One to run without celery, just populates the database one time
    * One to run django in one container and celery and beat in a separate container

### Examples

```
oc exec -it project.celery-1-0xss1 -- celery inspect -A project ping
-> celery@project.celery-1-0xss1: OK
        pong

# Looking for jobs submitted
oc exec -it project.celery-1-0xss1 -- celery inspect -A project stats |egrep 'total": {'
        "total": {}

# What are the registered tasks
oc exec -it project.celery-1-rry3a -- celery inspect -A project registered
-> celery@project.celery-1-rry3a: OK
    * add_bc
    * add_bc_periodic
    * hitchhiker
    * project.celery.debug_task

```
##### vim: ai et ts=4 sw=4 sts=4 nu ru
