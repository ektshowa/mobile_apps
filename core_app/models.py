from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .abstract_models import AbstractImage


class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    commune = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True,
                                default="R.D. Congo")

class ImageFile(AbstractImage):
    pass


