from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from core_app.abstract_models import AbstractTimeStampedModel,\
                                    AbstractProfile, AbstractBusinessEntity
from core_app.models import Address, ImageFile
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

    

