# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class NotificationManager(models.Manager):
    def save_notification_or_update_similar(self, notification):
        """
            Make sure that notifications are unique
            and the timestamp correspond to the last time
            the event has occurred
            No need to notify on your one actions
            example: if I liked my own post no need to notify me
        """
        if notification.actor != notification.target:
            query = Notification.objects.filter(actor=notification.actor,
                                                target=notification.target,
                                                verb=notification.verb,
                                                url=notification.url)
            if query.exists():
                similar = query.first()
                similar.timestamp = timezone.now()
                similar.is_read = False
                similar.save()
                return similar
            else:
                notification.save()
                return notification
        else:
            return self


class Notification(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='notifications_actor')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                               related_name='notifications_target')
    # The object that caused the notification
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    verb = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    url = models.URLField(max_length=100, null=True)
    objects = NotificationManager()

    def __str__(self):
        return str(self.actor) + ' made an action on ' + str(self.content_type) + ' [' + str(
            self.content_object) + '] of ' + str(self.target)

    class Meta:
        ordering = ['-timestamp']

    def get_read_notification_url(self):
        return reverse('notifications-api:update', kwargs={'pk': self.id})


from django.db.models.signals import m2m_changed
from reviews.models import Review


def notify(verb, redirect_to_actor_profile=False):
    def notify_func(sender, instance, action, *args, **kwargs):
        if action == 'post_add':
            actor_id = [id for id in kwargs['pk_set']][0]
            actor = User.objects.get(id=actor_id)
            target = instance.user
            print(instance.get_absolute_url(), '#################################')
            try:
                if redirect_to_actor_profile:
                    url = actor.profile.get_absolute_url()
                else:
                    url = instance.get_absolute_url()
            except:
                url = None
            notification = Notification(actor=actor, target=target, content_object=instance, verb=verb, url=url)
            Notification.objects.save_notification_or_update_similar(notification)

    return notify_func


# Here you can add register notification on any m2m field you want
# By calling notify with the verb that you want (this will return a method)
# pass the methods that you created with notify to m2m_changed.connect and the sender must be the m2m field with .through
# this would work all the time as long as you provide get_absolute_url on the target
# for example
notify_on_up_vote = notify(verb='up voted your review')
m2m_changed.connect(notify_on_up_vote, sender=Review.up_votes.through)

notify_on_down_vote = notify(verb='down voted your review')
m2m_changed.connect(notify_on_down_vote, sender=Review.down_votes.through)

