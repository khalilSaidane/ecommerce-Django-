from django.conf import settings
from django.db import models

from reviews.models import Review


class CommentReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    childs = models.ManyToManyField('self', related_name='childs_comments', blank=True)
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return self.content
