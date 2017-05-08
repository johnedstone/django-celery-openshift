# Understanding Celery in Development
## Celery Worker

Some of this may be out of date, but leaving here for historical reasons. 
These notes are for developing celery, before using in Openshift.

### Notes for Celery, Redis
References:

* (Celery 4.x] (http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
* https://realpython.com/blog/python/asynchronous-tasks-with-django-and-celery/
* http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/
* https://blog.syncano.io/configuring-running-django-celery-docker-containers-pt-1/
* https://github.com/johnedstone/docker-django-celery
* http://matthewminer.com/2015/02/21/pattern-for-async-task-queue-results.html
* http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django
* http://docs.celeryproject.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor
* http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#starting-the-scheduler 

#### Development

* Start Redis
    ```
    docker run -d -p 6379:6379 --name some-redis rhscl/redis-32-rhel7:latest
    docker run -it --link some-redis:redis --rm rhscl/redis-32-rhel7:latest redis-cli -h redis -p 6379 ping
    PONG

    docker run -it --link some-redis:redis --rm rhscl/redis-32-rhel7:latest redis-cli -h redis -p 6379
    ```

* Celery - Reference: https://realpython.com/blog/python/asynchronous-tasks-with-django-and-celery/

* **Test #1 Celery - running the celery server in worker mode**

    * Start celery

    ```
    celery --app=project.celery worker --loglevel=INFO

     -------------- celery@server v4.0.2 (latentcall)
     ---- **** -----
     --- * ***  * -- Linux-3.10.0-514.10.2.el7.x86_64-x86_64-with-redhat-7.3-Maipo 2017-04-28 21:05:31
     -- * - **** ---
     - ** ---------- [config]
     - ** ---------- .> app:         project.celery:0x2314f50
     - ** ---------- .> transport:   redis://some.server.fqdn:6379//
     - ** ---------- .> results:     redis://some.server.fqdn:6379/
     - *** --- * --- .> concurrency: 2 (prefork)
     -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
     --- ***** -----
      -------------- [queues]
                     .> celery           exchange=celery(direct) key=celery
     
     
     [tasks]
       . project.celery.debug_task
       . project.celery.get_answer
     
     [2017-04-28 21:05:31,567: INFO/MainProcess] Connected to redis://some.server.fqdn:6379//
     [2017-04-28 21:05:31,582: INFO/MainProcess] mingle: searching for neighbors
     [2017-04-28 21:05:32,620: INFO/MainProcess] mingle: all alone
     [2017-04-28 21:05:32,690: INFO/MainProcess] celery@server ready.
    ```

* **Test #2 Running Celery tasks - does NOT depend on Celery server running nor Redis**
    ```
    python manage.py shell
    >>> from project.celery import debug_task, get_answer
    >>> debug_task()
    Request: <Context: {'args': (), 'kwargs': {}}>
    >>> get_answer()
    42
    ```

* **Test #3 Running Celery tasks - which DOES depend on Celery server running (and consequently Redis)**
    ```
    # http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/

    python manage.py shell
    >>> from project.celery import debug_task, get_answer
    >>> get_answer.delay() # Note that the result is not return here, but is 
    mediated through redis

    <AsyncResult: 320c5d42-a80e-4876-b540-a63e61712a79>

    # Output from Celery server running above as in Test #1 - which must be sent through Redis I guess.
    [2017-04-29 03:58:54,622: INFO/MainProcess] Received task: project.celery.get_answer[320c5d42-a80e-4876-b540-a63e61712a79]
    [2017-04-29 03:58:59,631: INFO/PoolWorker-1] Task project.celery.get_answer[320c5d42-a80e-4876-b540-a63e61712a79] succeeded in 5.00662328093s: 42
    ```

* **Test #4 - Running the Celery in beat (scheduler) node**
    ```
    celery --app=project.celery beat --loglevel=INFO
    celery beat v4.0.2 (latentcall) is starting.
    __    -    ... __   -        _
    LocalTime -> 2017-04-28 21:32:08
    Configuration ->
        . broker -> redis://some.server.fqdn:6379//
        . loader -> celery.loaders.app.AppLoader
        . scheduler -> celery.beat.PersistentScheduler
        . db -> celerybeat-schedule
        . logfile -> [stderr]@%INFO
        . maxinterval -> 5.00 minutes (300s)
    [2017-04-28 21:32:08,932: INFO/MainProcess] beat: Starting...
    ```
* **Test #5 - Running the Celery in worker (scheduler) node and checking the status**

    ```
    # Start celery server
    celery --app=project.celery worker --loglevel=INFO

    # Check status of above
    celery --app=project.celery status
    celery@server: OK

    ```

* **Test #6 - Watching the Celery queue**
    ```

    # See http://docs.celeryproject.org/en/latest/userguide/monitoring.html#flower-real-time-celery-web-monitor
    # What needs to be running
    celery --app=project.celery worker --loglevel=INFO # that is all

    # This worked:
    pip install flower
    celery --app=project.celery flower # some errors (from __init__.py that can be ignored for this test)

    # then check 127.0.0.1:5555 and the tasks appear when in a django shell one types
    >>> from project.celery import get_answer
    get_answer.delay()

    # From another Celery project I did - this DID NOT working here
    # http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/
    # Watch UI for celery to confirm it running
    # with X tunnelling
    # 28-Apr-2017 - not working - probably a terminal error
    celery --app=APPNAME.celery control enable_events
    celery --app=APPNAME.celery events

    ```
## Celery beat

Notes: Redis, and the celery worker have to be running.  Run `beat` in a separate container, or on the same or diff VM.  Or run the worker with -B. See http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#starting-the-scheduler

* shortcut:  `celery --app=project.celery worker --loglevel=INFO -B`
* or run in two containers:

    celery --app=project.celery worker --loglevel=INFO
    celery --app=project.celery beat --loglevel=INFO

##### vim: ai et ts=4 sw=4 sts=4 nu
