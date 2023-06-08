from django.db import models
from django.contrib.auth.models import User


class WebsiteUser(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.username


class SaleAd(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_retired = models.BooleanField(default=False)
    date_retired = models.DateTimeField(default=None, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(default=None, null=True, blank=True)
    author = models.ForeignKey(WebsiteUser, related_name='saleads', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.title


class Illustration(models.Model):
    filename = models.CharField(max_length=200)
    salead = models.ForeignKey(SaleAd, related_name='illustrations', on_delete=models.CASCADE)

    def __str__(self):
        return self.filename
