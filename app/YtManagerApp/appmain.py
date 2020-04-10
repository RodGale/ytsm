import logging
import logging.handlers
import os
import sys

from django.conf import settings as dj_settings

from YtManagerApp.scheduler.jobs.synchronize_job import SynchronizeJob
from YtManagerApp.services import Services
from django.db.utils import OperationalError


def __initialize_logger():
    log_dir = os.path.join(dj_settings.DATA_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, "log.log"),
        maxBytes=1024 * 1024,
        backupCount=5
    )
    file_handler.setLevel(dj_settings.LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(dj_settings.LOG_FORMAT))
    logging.root.addHandler(file_handler)
    logging.root.setLevel(dj_settings.LOG_LEVEL)

    if dj_settings.DEBUG:
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter(dj_settings.CONSOLE_LOG_FORMAT))
        logging.root.addHandler(console_handler)


def main():
    __initialize_logger()

    try:
        if Services.appConfig.initialized:
            Services.scheduler.initialize()
            SynchronizeJob.schedule_global_job()
    except OperationalError:
        # Settings table is not created when running migrate or makemigrations;
        # Just don't do anything in this case.
        pass

    logging.info('Initialization complete.')
