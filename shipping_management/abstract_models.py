from django.db import models
from django.utils.text import slugify


class AbstractTimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class AbstractShipMaster(AbstractTimeStampedModel):
    phone_number = models.CharField("Téléphone", blank=True, null=True,
                                    max_length=20)

    class Meta:
        abstract = True


    