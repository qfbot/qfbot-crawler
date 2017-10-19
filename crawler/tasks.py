from __future__ import absolute_import
from .celery import qfbot
from .dispatcher import Boot

import logging
logging.basicConfig()


@qfbot.task
def test_task(project_name):
    """Spider tasks"""

    # TODO: project should be a spider instance
    project = ""
    logging.error(project)
    if project:
        dispatch = Boot(project)
        dispatch.start()
        dispatch.join()
