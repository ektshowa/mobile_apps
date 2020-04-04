from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from .abstract_models import AbstractImage, AbstractNameFieldsModel, \
                            AbstractTimeStampedModel


class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    commune = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True,
                                default="R.D. Congo")


class ImageFile(AbstractImage):
    pass


class Country(AbstractTimeStampedModel):
    english_name = models.CharField(_("Nom Anglais"), max_length=100,
                                        blank=True, null=True)
    french_name = models.CharField(_("Nom Français"), max_length=100,
                                        blank=True, null=True)
    local_name = models.CharField(_("Nom Locale"), max_length=100,
                                        blank=True, null=True)
    code = models.CharField(_("Code"), max_length=20,
                                        blank=True, null=True)
    region = models.CharField(_("Region du Globe"), max_length=100,
                                        blank=True, null=True)
    continent = models.CharField(_("Continent"), max_length=50,
                                        blank=True, null=True)

    def __repr__(self):
        return "Nom du Pays: %s" % self.english_name

    def __str__(self):
        return self.code + " - " + self.english_name

    class Meta:
        verbose_name = _("Pays")
        verbose_name_plural = _("Pays")


class Region(AbstractTimeStampedModel, AbstractNameFieldsModel):
    country = models.ForeignKey(Country,
                                related_name="regions_of_country",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Province"),
                                blank=True)
    is_active = models.BooleanField(_("En attente d'activation"), default=False)

    def __repr__(self):
        return "Region: %s - %s" % (self.code, self.name)

    def __str__(self):
        return self.code + " " + self.name

    def _get_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(Region, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Province")


class City(AbstractTimeStampedModel, AbstractNameFieldsModel):
    country = models.ForeignKey(Country,
                                related_name="cities_of_country",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Pays"),
                                blank=True)
    region = models.ForeignKey(Region,
                                related_name="cities_of_region",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Province"),
                                blank=True)
    city_type = models.CharField(_("Ville ou District"),
                            max_length=50,
                            blank=True)
    is_active = models.BooleanField(_("En attente d'activation"), default=False)

    def __repr__(self):
        return "City: %s - %s" % (self.code, self.name)

    def __str__(self):
        return self.code + " " + self.name

    def _get_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(City, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Ville")


class Commune(AbstractTimeStampedModel, AbstractNameFieldsModel):
    city = models.ForeignKey(City,
                            related_name="communes_of_city",
                            on_delete=models.CASCADE,
                            db_index=True,
                            verbose_name=_("Ville"),
                            blank=True)
    is_active = models.BooleanField(_("En attente d'activation"), default=False)

    def __repr__(self):
        return "Commune: %s - %s" % (self.code, self.name)

    def __str__(self):
        return self.code + " " + self.name

    def _get_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(Commune, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Commune")



