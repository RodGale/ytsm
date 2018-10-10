import logging
import os
import os.path
from shutil import copyfile

from django.conf import settings
from django.contrib.auth.models import User

from .models import UserSettings
from .utils.customconfigparser import ConfigParserWithEnv


class AppConfig(object):
    __SETTINGS_FILE = 'config.ini'
    __LOG_FILE = 'log.log'

    DEFAULT_SETTINGS = {
        'global': {
            'YouTubeApiKey': 'AIzaSyBabzE4Bup77WexdLMa9rN9z-wJidEfNX8',
            'SynchronizationSchedule': '0 * * * * *',
            'SchedulerConcurrency': '2',
        },
        'user': {
            'MarkDeletedAsWatched': 'True',
            'DeleteWatched': 'True',
            'AutoDownload': 'True',
            'DownloadMaxAttempts': '3',
            'DownloadGlobalLimit': '',
            'DownloadSubscriptionLimit': '5',
            'DownloadOrder': 'playlist_index',
            'DownloadPath': '${env:USERPROFILE}${env:HOME}/Downloads',
            'DownloadFilePattern': '${channel}/${playlist}/S01E${playlist_index} - ${title} [${id}]',
            'DownloadFormat': 'bestvideo+bestaudio',
            'DownloadSubtitles': 'True',
            'DownloadAutogeneratedSubtitles': 'False',
            'DownloadSubtitlesAll': 'False',
            'DownloadSubtitlesLangs': 'en,ro',
            'DownloadSubtitlesFormat': '',
        }
    }

    def __init__(self):
        self.log_path = os.path.join(settings.BASE_DIR, 'config', AppConfig.__LOG_FILE)
        self.settings_path = os.path.join(settings.BASE_DIR, 'config', AppConfig.__SETTINGS_FILE)

        self.settings = ConfigParserWithEnv(defaults=AppConfig.DEFAULT_SETTINGS, allow_no_value=True)
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r') as f:
                self.settings.read_file(f)

    def save_settings(self):
        if os.path.exists(self.settings_path):
            # Create a backup
            copyfile(self.settings_path, self.settings_path + ".backup")
        else:
            # Ensure directory exists
            settings_dir = os.path.dirname(self.settings_path)
            os.makedirs(settings_dir, exist_ok=True)

        with open(self.settings_path, 'w') as f:
            self.settings.write(f)

    def get_user_config(self, user: User) -> ConfigParserWithEnv:
        user_settings = UserSettings.find_by_user(user)
        if user_settings is not None:
            user_config = ConfigParserWithEnv(defaults=self.settings, allow_no_value=True)
            user_config.read_dict({
                'user': user_settings.to_dict()
            })
            return user_config

        return settings


instance: AppConfig = None


def __initialize_logger():
    # Parse log level
    log_level_str = instance.settings.get('global', 'LogLevel', fallback='INFO')
    levels = {
        'NOTSET': logging.NOTSET,
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    if log_level_str.upper() not in levels:
        log_level_str = 'INFO'

    # Init
    logging.basicConfig(filename=instance.log_path, level=levels[log_level_str])


def initialize_config():
    global instance
    instance = AppConfig()

    # Load settings
    instance.load_settings()

    # Initialize logger
    __initialize_logger()
    logging.info('Application started!')
