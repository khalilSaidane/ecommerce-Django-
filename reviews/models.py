from django.conf import settings
from django.db import models
from django.urls import reverse

from products.models import Product


class ReviewManager(models.Manager):

    def toggle_up_vote(self, user, review_id):
        review = Review.objects.get(id=review_id)
        updated = False
        up_voted = False
        if user in review.up_votes.all():
            review.up_votes.remove(user)
            up_voted = False
        else:
            review.up_votes.add(user)
            up_voted = True
            if user in review.down_votes.all():
                review.down_votes.remove(user)
        updated = True
        return review

    def toggle_down_vote(self, user, review_id):
        review = Review.objects.get(id=review_id)
        if user in review.down_votes.all():
            review.down_votes.remove(user)
        else:
            review.down_votes.add(user)
            if user in review.up_votes.all():
                review.up_votes.remove(user)
        return review


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=350)
    rate = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    up_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='reviews_up_votes')
    down_votes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='reviews_down_votes')
    objects = ReviewManager()  # this will add the manager to objects

    def get_absolute_url(self):
        return reverse('reviews:detail', kwargs={'review_id': self.id})

    def __str__(self):
        return 'on '+str(self.product.name)+' with rate '+str(self.rate)

    class Meta:
        ordering = ['-timestamp']
