from django.db import models
from django.contrib.auth.models import User


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mark_deleted_as_watched = models.BooleanField(null=True)
    delete_watched = models.BooleanField(null=True)
    auto_download = models.BooleanField(null=True)
    download_global_limit = models.IntegerField(null=True)
    download_subscription_limit = models.IntegerField(null=True)
    download_order = models.TextField(null=True)
    download_path = models.TextField(null=True)
    download_file_pattern = models.TextField(null=True)
    download_format = models.TextField(null=True)
    download_subtitles = models.BooleanField(null=True)
    download_autogenerated_subtitles = models.BooleanField(null=True)
    download_subtitles_all = models.BooleanField(null=True)
    download_subtitles_langs = models.TextField(null=True)
    download_subtitles_format = models.TextField(null=True)

    @staticmethod
    def find_by_user(user: User):
        result = UserSettings.objects.filter(user=user)
        if len(result) > 0:
            return result.first()
        return None

    def __str__(self):
        return str(self.user)

    def to_dict(self):
        ret = {}

        if self.mark_deleted_as_watched is not None:
            ret['MarkDeletedAsWatched'] = self.mark_deleted_as_watched
        if self.delete_watched is not None:
            ret['DeleteWatched'] = self.delete_watched
        if self.auto_download is not None:
            ret['AutoDownload'] = self.auto_download
        if self.download_global_limit is not None:
            ret['DownloadGlobalLimit'] = self.download_global_limit
        if self.download_subscription_limit is not None:
            ret['DownloadSubscriptionLimit'] = self.download_subscription_limit
        if self.download_order is not None:
            ret['DownloadOrder'] = self.download_order
        if self.download_path is not None:
            ret['DownloadPath'] = self.download_path
        if self.download_file_pattern is not None:
            ret['DownloadFilePattern'] = self.download_file_pattern
        if self.download_format is not None:
            ret['DownloadFormat'] = self.download_format
        if self.download_subtitles is not None:
            ret['DownloadSubtitles'] = self.download_subtitles
        if self.download_autogenerated_subtitles is not None:
            ret['DownloadAutogeneratedSubtitles'] = self.download_autogenerated_subtitles
        if self.download_subtitles_all is not None:
            ret['DownloadSubtitlesAll'] = self.download_subtitles_all
        if self.download_subtitles_langs is not None:
            ret['DownloadSubtitlesLangs'] = self.download_subtitles_langs
        if self.download_subtitles_format is not None:
            ret['DownloadSubtitlesFormat'] = self.download_subtitles_format

        return ret


class SubscriptionFolder(models.Model):
    name = models.TextField(null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Channel(models.Model):
    channel_id = models.TextField(null=False, unique=True)
    username = models.TextField(null=True, unique=True)
    custom_url = models.TextField(null=True, unique=True)
    name = models.TextField()
    description = models.TextField()
    icon_default = models.TextField()
    icon_best = models.TextField()
    upload_playlist_id = models.TextField()

    @staticmethod
    def find_by_channel_id(channel_id):
        result = Channel.objects.filter(channel_id=channel_id)
        if len(result) > 0:
            return result.first()
        return None

    @staticmethod
    def find_by_username(username):
        result = Channel.objects.filter(username=username)
        if len(result) > 0:
            return result.first()
        return None

    @staticmethod
    def find_by_custom_url(custom_url):
        result = Channel.objects.filter(custom_url=custom_url)
        if len(result) > 0:
            return result.first()
        return None

    def __str__(self):
        return self.name


class Subscription(models.Model):
    name = models.TextField(null=False)
    parent_folder = models.ForeignKey(SubscriptionFolder, on_delete=models.SET_NULL, null=True, blank=True)
    playlist_id = models.TextField(null=False, unique=True)
    description = models.TextField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    icon_default = models.TextField()
    icon_best = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # overrides
    auto_download = models.BooleanField(null=True)
    download_limit = models.IntegerField(null=True)
    download_order = models.TextField(null=True)
    manager_delete_after_watched = models.BooleanField(null=True)

    def __str__(self):
        return self.name


class Video(models.Model):
    video_id = models.TextField(null=False)
    name = models.TextField(null=False)
    description = models.TextField()
    watched = models.BooleanField(default=False, null=False)
    downloaded_path = models.TextField(null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    playlist_index = models.IntegerField(null=False)
    publish_date = models.DateTimeField(null=False)
    icon_default = models.TextField()
    icon_best = models.TextField()

    def __str__(self):
        return self.name