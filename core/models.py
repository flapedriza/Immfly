import os
import uuid

from decimal import Decimal

from django.db import models
from jsonfield import JSONField


def get_default_channel():
    return Channel.objects.get_or_create(title='deleted', picture='channel_files/deleted.jpg')


class Channel(models.Model):
    def image_path(self, filename: str) -> str:
        """
        Generates the file path to store the image
        :param filename: name of the image file
        :return: path where the image will be stored
        """
        ext = filename.split('.')[-1]
        file = 'header_image.' + ext
        return os.path.join('channel_files/' + self.title, file)

    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    language = models.CharField(max_length=2, null=False, blank=False, default='ES')
    picture = models.ImageField(null=False, blank=False, upload_to=image_path)
    parent_channel = models.ForeignKey(
        'self',
        on_delete=models.SET(get_default_channel),
        related_name='subchannels',
        null=True,
        blank=True

    )

    def __str__(self):
        return self.title


class Content(models.Model):
    def content_path(self, filename: str) -> str:
        """
        Generates the file path to store the content
        :param filename: name of the content file
        :return: path where the content will be stored
        """
        ext = filename.split('.')[-1]
        name = uuid.uuid4().hex + '.' + ext
        return os.path.join('channel_files/' + self.channel.title + '/content', name)

    title = models.CharField(max_length=50, null=False, blank=False, unique=True)
    metadata = JSONField()
    channel = models.ForeignKey(
        Channel,
        on_delete=models.SET(get_default_channel),
        null=False,
        default=get_default_channel
    )
    file = models.FileField(null=False, blank=False, upload_to=content_path)

    def save(self, **kwargs):
        super(Content, self).save(**kwargs)
        rating = Rating.objects.create(content=self)
        rating.save()

    def __str__(self):
        return self.title


class Rating(models.Model):
    total = models.PositiveIntegerField(default=0)
    count = models.PositiveIntegerField(default=0)
    average = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal(0.0))
    content = models.OneToOneField(Content, on_delete=models.CASCADE)

    def __str__(self):
        return self.content.title + ' content rating: ' + str(self.average)
