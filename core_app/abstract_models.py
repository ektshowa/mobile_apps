from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

BIRTH_MONTHS_CHOICE = tuple([(str(i), str(i)) for i in range(1, 13)])
YEAR_MONTHS_CHOICE = tuple([(str(i), str(i)) for i in range(1930, 2007)])


class AbstractTimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True,
                                                            null=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True,
                                                            null=True)

    class Meta:
        abstract = True


class AbstractBusinessEntity(AbstractTimeStampedModel):
    business_name = models.CharField(max_length=100, blank=True, null=True)
    identification_number = models.CharField(max_length=50, blank=True,
                                                                null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    class Meta:
        abstract = True


class AbstractProfile(AbstractTimeStampedModel):
    month_birth = models.CharField(_("Mois"),
                                    choices=BIRTH_MONTHS_CHOICE,
                                    blank=True,
                                    null=True,
                                    max_length=2)
    year_birth = models.CharField(_("Année"),
                                    choices=YEAR_MONTHS_CHOICE,
                                    blank=True,
                                    null=True,
                                    max_length=4)
    phone_number = PhoneNumberField(blank=True, null=True)

    @property
    def birth_month_year(self):
        return "{}-{}".format(self.month_birth, self.year_birth)

    class Meta:
        abstract = True


class AbstractImage(AbstractTimeStampedModel):
    image_content = models.ImageField(
        _("Image"),
        upload_to="uploads/uza_ticket/images",
        max_length=255,
        blank=True, null=True)

    class Meta:
        abstract = True


class AbstractFile(AbstractTimeStampedModel):
    file_content = models.FileField(
        _("Fichier"),
        upload_to=settings.UZA_TICKET_IMAGES_UPLOAD_FOLDER,
        max_length=255,
        blank=True, null=True)
    
    class Meta:
        abstract = True

