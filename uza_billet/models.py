from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from decimal import Decimal
from core_app.abstract_models import AbstractTimeStampedModel,\
                                    AbstractNameFieldsModel,\
                                    AbstractProfile, AbstractBusinessEntity
from core_app.models import Address, ImageFile, MoneyField
import sys, traceback


class IndividualEntity(AbstractProfile):
    auth_user = models.OneToOneField(User,
                                    related_name="individual_user",
                                    on_delete=models.CASCADE)
    address = models.ForeignKey(Address,
                                related_name="individual_address",
                                db_index=True,
                                on_delete=models.CASCADE,
                                verbose_name=_("Adresse"),
                                blank=True)
    photo = models.ForeignKey(ImageFile,
                            related_name="individual_photo",
                            db_index=True,
                            on_delete=models.CASCADE,
                            verbose_name=_("Photo"),
                            blank=True)
    is_seller = models.BooleanField(_("Compte Vendeur"),
                                default=True)
    
    class Meta:
        verbose_name = _("Compte Individuel - Acheteur ou Vendeur")
        verbose_name_plural = _("Comptes Individuels - Acheteurs ou Vendeurs")


class BusinessEntity(AbstractBusinessEntity):
    account_admin = models.OneToOneField(User,
                                        related_name="business_entity_admin",
                                        on_delete=models.CASCADE)
    address = models.ForeignKey(Address,
                                related_name="business_address",
                                db_index=True,
                                on_delete=models.CASCADE,
                                verbose_name=_("Adresse"),
                                blank=True)

    class Meta:
        verbose_name = _("Compte Entreprise")
        verbose_name_plural = _("Comptes Entreprises")


class BusinessTeam(AbstractTimeStampedModel):
    business_entity = models.OneToOneField(BusinessEntity,
                                        on_delete=models.CASCADE,
                                        related_name="business_team_entity")
    team_lead = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    related_name="user_team_lead")
    is_active = models.BooleanField(_("Équipe Active"), default=True)

    def __repr__(self):
        return "Équipe: %s - %s" % (self.business_entity.id,
                                    self.business_entity.business_name)

    def __str__(self):
        return "Équipe: %s - %s" % (self.business_entity.id,
                                    self.business_entity.business_name)

    class Meta:
        verbose_name = _("Équipe")
        verbose_name_plural = _("Équipes")


class BusinessTeamMember(AbstractProfile):
    auth_user = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    related_name="team_member_user")
    business_team = models.ForeignKey(BusinessTeam,
                                    related_name="team_member_business",
                                    db_index=True,
                                    on_delete=models.CASCADE,
                                    verbose_name = _("Équipe"),
                                    blank=True,
                                    null=True)
    is_active = models.BooleanField(_("Équipe Active"), default=True)   
    is_team_admin = models.BooleanField(_("Compte Administrateur"),
                                    default=True)

    def __repr__(self):
        return "Membre: %s %s" % (self.auth_user.first_name,
                                    self.auth_user.last_name)

    def __str__(self):
        return "Membre: %s %s" % (self.auth_user.first_name,
                                    self.auth_user.last_name)

    class Meta:
        verbose_name = _("Membre Équipe")
        verbose_name_plural = _("Membres Équipes")

    
class IndividualBuyer(AbstractProfile):
    auth_user = models.OneToOneField(User,
                                    on_delete=models.CASCADE,
                                    related_name="individual_buyer_user")
    address = models.ForeignKey(Address,
                                related_name="individual_buyer_address",
                                db_index=True,
                                on_delete=models.CASCADE,
                                verbose_name=_("Adresse"),
                                blank=True)
    
    def __repr__(self):
        return "Acheteur: %s %s" % (self.auth_user.first_name,
                                    self.auth_user.last_name)

    def __str__(self):
        return "Acheteur: %s %s" % (self.auth_user.first_name,
                                    self.auth_user.last_name)

    class Meta:
        verbose_name = _("Acheteur")
        verbose_name_plural = _("Acheteurs")


class Event(AbstractTimeStampedModel, AbstractNameFieldsModel):
    address = models.ForeignKey(Address,
                                related_name="event_address",
                                db_index=True,
                                on_delete=models.CASCADE,
                                verbose_name=_("Adresse"),
                                blank=True)
    unit_price = MoneyField("Prix",
                            null=True,
                            blank=True)
    sale_price = MoneyField("Prix Promotionel",
                            null=True,
                            blank=True)
    sale_from = models.DateTimeField("Date Debut Promotion",
                            null=True,
                            blank=True)
    sale_to = models.DateTimeField("Date Fin Promotion",
                            null=True,
                            blank=True)
    event_date = models.DateTimeField("Date de l'evenement",
                                    null=True,
                                    blank=True)

    def __repr__(self):
        return "Ticket: %s - %s" % (self.id, self.name)

    def __str__(self):
        return "Ticket: %s - %s" % (self.id, self.name)

    def on_sale(self):
        n = now()
        valid_from = self.sale_from is None or self.sale_from < n
        valid_to = self.sale_to is None or self.sale_to > n
        return self.sale_price is not None and valid_from and valid_to

    def has_price(self):
        return self.on_sale() or self.price is not None

    def price(self):
        if self.on_sale():
            return self.sale_price
        elif self.has_price():
            return self.unit_price
        return Decimal("0")   
