from django.db import models
from django.conf import settings
from products.models import Product


class CartProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ['-timestamp']
