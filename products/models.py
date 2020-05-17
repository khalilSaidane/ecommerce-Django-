from django.db import models
from django.conf import settings
from django.urls import reverse


def upload_product_image(instance, filename):
    return "products/{filename}".format(filename=filename)


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField()
    image = models.ImageField(upload_to=upload_product_image)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'id': self.id})
