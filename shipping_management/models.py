from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from .abstract_models import AbstractShipMaster, AbstractTimeStampedModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation



class Country(AbstractTimeStampedModel):
    english_name = models.CharField(_("Nom Anglais"), max_length=100)
    french_name = models.CharField(_("Nom Français"), max_length=100)
    local_name = models.CharField(_("Nom Locale"), max_length=100)
    code = models.CharField(_("Code"), max_length=20)
    region = models.CharField(_("Region du Globe"), max_length=100)
    continent = models.CharField(_("Continent"), max_length=50)

    def __repr__(self):
        return "Nom du Pays: %s" % self.french_name

    def __str__(self):
        return self.code + " - " + self.french_name

    class Meta:
        verbose_name = _("Pays")
        verbose_name_plural = _("Pays")


class Address(models.Model):
    street = models.CharField(_("Avenue"), max_length=200, blank=True)
    city = models.CharField(_("Ville"), max_length=50, blank=True)
    commune = models.CharField(_("Commune"), max_length=50, blank=True)
    region = models.CharField(_("Province"), max_length=50, blank=True)
    country = models.CharField(_("Pays"), max_length=50, default="R.D. Congo")

    def __repr__(self):
        return "street: %s, city %s, commune: %s, region: %s" % \
                    (self.street, self.city,
                    self.commune, self.region)

    def __str__(self):
        return self.street + " " + self.commune + self.city + " " + self.region

    class Meta:
        verbose_name = _("Adresse")
        verbose_name_plural = _("Adresses")



class ShipmentDestinataire(AbstractTimeStampedModel):
    auth_user = models.OneToOneField(User,
                                    primary_key=True,
                                    on_delete=models.CASCADE,
                                    related_name="destinataire_user")
    phone_number = models.CharField("Téléphone", blank=True, null=True,
                                    max_length=20)

    def __str__(self):
        return "ID: %s, Name: %s %s" % (self.auth_user.id,
                                        self.auth_user.first_name,
                                        self.auth_user.last_name)

    def __repr__(self):
        return "ID: %s, Name: %s %s" % (self.auth_user.id,
                                        self.auth_user.first_name,
                                        self.auth_user.last_name)


class ShipmentOwner(AbstractTimeStampedModel):
    auth_user = models.OneToOneField(User,
                                    primary_key=True,
                                    on_delete=models.CASCADE,
                                    related_name="ship_owner_user")
    phone_number = models.CharField("Téléphone", blank=True, null=True,
                                    max_length=20)

    def __str__(self):
        return "ID: %s, Name: %s %s" % (self.auth_user.id,
                                        self.auth_user.first_name,
                                        self.auth_user.last_name)

    def __repr__(self):
        return "ID: %s, Name: %s %s" % (self.auth_user.id,
                                        self.auth_user.first_name,
                                        self.auth_user.last_name)


class Shipment(AbstractTimeStampedModel):
    description = models.CharField("Description", blank=True, null=True,
                                    max_length=300)
    owner = models.ForeignKey(ShipmentOwner,
                            related_name="shipment_shipment_owner",
                            blank=True,
                            null=True,
                            db_index=True,
                            on_delete=models.CASCADE)
    date_registered = models.DateField("Date d'Enregistrement",
                            blank=True,
                            null=True)

    def __str__(self):
        return "Owner ID: %s, Date registered: %s" % (self.owner.auth_user.id,
                                                    self.date_registered)

    def __repr__(self):
        return "Owner ID: %s, Date registered: %s" % (self.owner.auth_user.id,
                                                    self.date_registered)


class ShippingMovement(AbstractTimeStampedModel):
    shipment = models.ForeignKey(Shipment,
                                related_name="shipping_movement_shipment",
                                blank=True,
                                null=True,
                                db_index=True,
                                on_delete=models.CASCADE)
    destinataire = models.ForeignKey(ShipmentDestinataire,
                                related_name="shipping_movement_destinataire",
                                blank=True,
                                null=True,
                                db_index=True,
                                on_delete=models.CASCADE)
    shipping_date = models.DateField("Date de Départ",
                                    blank=True,
                                    null=True)
    arrival_date = models.DateField("Date d'Arrivée",
                                    blank=True,
                                    null=True)
    point_of_shipping = models.CharField("Point de Départ",
                                        blank=True,
                                        null=True,
                                        max_length=200)
    point_of_arrival = models.CharField("Point d'Arrivée",
                                        blank=True,
                                        null=True,
                                        max_length=200)
    content_type = models.ForeignKey(ContentType,
                null=True,
                blank=True,
                related_name="object_content_type",
                on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(
                null=True,
                blank=True,
                db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')   
    
    def __str__(self):
        return "Shipment Owner: %s, Sipping Date: %s" % \
                                            (self.shipment.owner.id,
                                            self.shipping_date)

    def __repr__(self):
        return "Shipment Owner: %s, Sipping Date: %s" % \
                                            (self.shipment.owner.id,
                                            self.shipping_date)


class IndividualShipMaster(AbstractShipMaster):
    auth_user = models.OneToOneField(User,
                                    primary_key=True,
                                    on_delete=models.CASCADE,
                                    related_name="ind_ship_master_user")       
    locations = models.ForeignKey(Address,
                                related_name="ind_ship_master_location",
                                blank=True,
                                null=True,
                                db_index=True,
                                on_delete=models.CASCADE,
                                verbose_name="Dépôts")
    shipping_movements = GenericRelation(ShippingMovement)
    
    def __str__(self):
        return "ID: %s, Name: %s %s" % (self.auth_user.id,
                                        self.auth_user.first_name,
                                        self.auth_user.last_name)

    def __repr__(self):
        return "ID: %s, Name: %s %s" % (self.auth_user.id,
                                        self.auth_user.first_name,
                                        self.auth_user.last_name)


class BusinessShipMaster(AbstractShipMaster):
    auth_user = models.OneToOneField(User,
                                    primary_key=True,
                                    on_delete=models.CASCADE,
                                    related_name="bus_ship_master_user")
    business_name = models.CharField("Nom de l'entreprise",
                                    blank=True,
                                    null=True,
                                    max_length=100)
    locations = models.ForeignKey(Address,
                                related_name="bus_ship_master_location",
                                blank=True,
                                null=True,
                                db_index=True,
                                on_delete=models.CASCADE,
                                verbose_name="Dépôts")
    shipping_movements = GenericRelation(ShippingMovement)

    def __str__(self):
        return "ID: %s, Business Name: %s" % (self.auth_user.id, 
                                                self.auth_user.business_name)

    def __repr__(self):
        return "ID: %s, Business Name: %s" % (self.auth_user.id, 
                                                self.auth_user.business_name)

