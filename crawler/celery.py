from __future__ import absolute_import
from datetime import timedelta
from celery import Celery
from . import settings

qfbot = Celery(
    "crawler",
    broker=settings.RQ_URL,
    backend='amqp://',
    include=["crawler.tasks"]
    )

qfbot.conf.update(
    CELERY_ROUTES={
        "crawler.tasks.spider_task": {'queue': 'celery'},
    },

    CELERYBEAT_SCHEDULE={
        "spider_crontab": {
            "task": "crawler.tasks.test_task",
            "schedule": timedelta(hours=1),
            "args": ()
        },
    }
)

if __name__ == "__main__":
    qfbot.start()
