from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, \
                                                GenericRelation
from django.contrib.contenttypes.models import ContentType
from .abstract_models import AbstractPhoneNumberFields,\
                            AbstractTimeStampedModel, AbstractNameFieldsModel
import sys
import traceback


CITY_TYPE_CHOICES = (
    ('ville', 'Ville'),
    ('district', 'District'),
)


class Province(AbstractTimeStampedModel, AbstractNameFieldsModel):
    country = models.CharField(_("Pays"), max_length=50, default="R.D. Congo")
    is_active = models.BooleanField(_("En attente d'activation?"),
                                                            default=False)

    def __repr__(self):
        return "Région: %s - %s" % (self.code, self.name)

    def __str__(self):
        return self.code + " " + self.name

    def _get_slug(self):
        return slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(Province, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Province")


class City(AbstractTimeStampedModel, AbstractNameFieldsModel):
    country = models.CharField(_("Pays"), max_length=50, default="R.D. Congo")
    province = models.ForeignKey(Province,
                                related_name="country_regions",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Province"),
                                blank=True)
    city_type = models.CharField(_("type d'entité Ville/District"),
                            max_length=50,
                            choices=CITY_TYPE_CHOICES,
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
                            related_name="city_communes",
                            on_delete=models.CASCADE,
                            db_index=True,
                            verbose_name=_("Ville/District"),
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


class ResidentialSituationCode(AbstractTimeStampedModel,
                                                    AbstractNameFieldsModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(ResidentialSituationCode, self).save(*args, **kwargs)


class HeadHouseholdLinkCode(AbstractTimeStampedModel,
                                                    AbstractNameFieldsModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(HeadHouseholdLinkCode, self).save(*args, **kwargs)


class ReligionCode(AbstractTimeStampedModel, AbstractNameFieldsModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(ReligionCode, self).save(*args, **kwargs)


class HandicapTypeCode(AbstractTimeStampedModel, AbstractNameFieldsModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(HandicapTypeCode, self).save(*args, **kwargs)


class OccupationStatusCode(AbstractTimeStampedModel, AbstractNameFieldsModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(OccupationStatusCode, self).save(*args, **kwargs)


class OccupationSituationCode(AbstractTimeStampedModel,
                                                    AbstractNameFieldsModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(OccupationSituationCode, self).save(*args, **kwargs)


class MarritalStatusCode(AbstractTimeStampedModel, AbstractNameFieldsModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(MarritalStatusCode, self).save(*args, **kwargs)


class MarriageTypeCode(AbstractTimeStampedModel, AbstractNameFieldsModel):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(MarriageTypeCode, self).save(*args, **kwargs)


class CensusTeam(AbstractTimeStampedModel, AbstractNameFieldsModel,
                                                    AbstractPhoneNumberFields):
    """address = models.ForeignKey(Address,
                                related_name="census_team_address",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Adresse"),
                                blank=True)"""
    content_type = models.ForeignKey(ContentType,
                on_delete=models.CASCADE,
                null=True,
                blank=True,
                related_name="team_object_address_type")
    object_id = models.PositiveIntegerField(
                null=True,
                blank=True,
                db_index=True)
    address_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(CensusTeam, self).save(*args, **kwargs)


class CensusAgent(AbstractTimeStampedModel, AbstractPhoneNumberFields):
    auth_user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='census_agent_user')
    """address = models.ForeignKey(Address,
                                related_name="census_agent_address",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Adresse"),
                                blank=True)"""
    census_team = models.ForeignKey(CensusTeam,
                                related_name="census_agent_team",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Équipe"),
                                blank=True)
    is_manager = models.BooleanField(_("Est Chef d'Équipe?"), default=False)
    content_type = models.ForeignKey(ContentType,
                on_delete=models.CASCADE,
                null=True,
                blank=True,
                related_name="agent_object_address_type")
    object_id = models.PositiveIntegerField(
                null=True,
                blank=True,
                db_index=True)
    address_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "Personne: %s %s" % (self.auth_user.first_name,
                                                    self.auth_user.last_name)

    def __repr__(self):
        return "Personne: %s %s" % (self.auth_user.first_name,
                                                    self.auth_user.last_name)


class HouseholdRecord(AbstractTimeStampedModel):
    is_own_filled = models.BooleanField(_("Réponse Assistée?"), default=True)
    census_agent = models.ForeignKey(CensusAgent,
                                related_name="household_record_agent",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Agent Recenceur"),
                                blank=True)
    agent_id = models.CharField(_("Agent ID"),
                                unique=True,
                                max_length=5,
                                blank=True,
                                null=True)
    filling_date = models.DateTimeField(_('Date de la Réponse'),
                                null=True,
                                blank=True)
    male_present_resident_numb = models.PositiveIntegerField(
                                _("Nombre de résidents masculin présents"),
                                blank=True,
                                null=True)
    female_present_resident_numb = models.PositiveIntegerField(
                                _("Nombre de résidents féminin présents"),
                                blank=True,
                                null=True)
    male_absent_resident_numb = models.PositiveIntegerField(
                                _("Nombre de résidents masculin absents"),
                                blank=True,
                                null=True)
    female_absent_resident_numb = models.PositiveIntegerField(
                                _("Nombre de résidents féminin absents"),
                                blank=True,
                                null=True)
    visiting_male_numb = models.PositiveIntegerField(
                                _("Nombre de visiteurs masculin"),
                                blank=True,
                                null=True)
    visiting_female_numb = models.PositiveIntegerField(
                                _("Nombre de visiteurs féminin"),
                                blank=True,
                                null=True)
    milieu_type = models.CharField(_("Urbain ou Rural"),
                                max_length=50,
                                blank=True,
                                null=True)
    content_type = models.ForeignKey(ContentType,
                on_delete=models.CASCADE,
                null=True,
                blank=True,
                related_name="household_object_address_type")
    object_id = models.PositiveIntegerField(
                null=True,
                blank=True,
                db_index=True)
    address_object = GenericForeignKey('content_type', 'object_id')

    def __repr__(self):
        "Record ID %s - Agent ID %s" % (self.id, self.census_agent.auth_user.id)

    def __str__(self):
        "Record ID %s - Agent ID %s" % (self.id, self.census_agent.auth_user.id)


class Individual(AbstractTimeStampedModel, AbstractPhoneNumberFields):
    auth_user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='individual_census_user')
    """address = models.ForeignKey(Address,
                                related_name="individual_address",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Adresse"),
                                blank=True)
    place_of_birth = models.ForeignKey(Address,
                                related_name="individual_birth_place",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Lieu de Naissance"),
                                blank=True)"""
    age = models.PositiveIntegerField(_("Age"),
                                blank=True,
                                null=True)
    date_of_birth = models.DateField(_("Date de Naissance"),
                                blank=True,
                                null=True)
    occupation = models.CharField(_("Occupation"),
                                max_length=100,
                                blank=True,
                                null=True)
    highest_diploma = models.CharField(_("Plus Haut Diplome"),
                                max_length=100,
                                blank=True,
                                null=True)
    marrital_status = models.ForeignKey(MarritalStatusCode,
                                related_name="individual_marrital_status",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Situation Matrimoniale"),
                                blank=True)
    marriage_type = models.ForeignKey(MarriageTypeCode,
                                related_name="individual_marrital_type",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Type de Mariage"),
                                blank=True)
    head_household_link = models.ForeignKey(HeadHouseholdLinkCode,
                                related_name="individual_head_household_link",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Lien avec le Chef de Ménage"),
                                blank=True)
    religion_code = models.ForeignKey(ReligionCode,
                                related_name="individual_religion_code",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Religion"),
                                blank=True)
    handicap_type_code = models.ForeignKey(HandicapTypeCode,
                                related_name="individual_handicap_code",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Type de l'handicap"),
                                blank=True)
    occupation_status_code = models.ForeignKey(OccupationStatusCode,
                            related_name="individual_occupation_status_code",
                            on_delete=models.CASCADE,
                            db_index=True,
                            verbose_name=_("Type de l'Occupation"),
                            blank=True)
    occupation_situation_code = models.ForeignKey(OccupationSituationCode,
                            related_name="individual_occupation_situation_code",
                            on_delete=models.CASCADE,
                            db_index=True,
                            verbose_name=_("Situation de l'Occupation"),
                            blank=True)
    household_record = models.ForeignKey(HouseholdRecord,
                                related_name="individual_address",
                                on_delete=models.CASCADE,
                                db_index=True,
                                verbose_name=_("Questionnaire Ménage"),
                                blank=True)
    content_type = models.ForeignKey(ContentType,
                on_delete=models.CASCADE,
                null=True,
                blank=True,
                related_name="individual_object_address_type")
    object_id = models.PositiveIntegerField(
                null=True,
                blank=True,
                db_index=True)
    address_object = GenericForeignKey('content_type', 'object_id')
    place_of_birth_type = models.ForeignKey(ContentType,
                on_delete=models.CASCADE,
                null=True,
                blank=True,
                related_name="individual_object_place_of_birth_type")
    place_of_birth_object_id = models.PositiveIntegerField(
                null=True,
                blank=True,
                db_index=True)
    place_of_birth_object = GenericForeignKey(
                            'place_of_birth_type', 'place_of_birth_object_id')

    def __str__(self):
        return "Personne: %s %s" % (self.auth_user.first_name,
                                                    self.auth_user.last_name)

    def __repr__(self):
        return "Personne: %s %s" % (self.auth_user.first_name,
                                                    self.auth_user.last_name)


class Address(models.Model):
    house_num = models.CharField(_("Numéro"), max_length=5, blank=True)
    street = models.CharField(_("Avenue"), max_length=200, blank=True)
    province = models.ForeignKey(Province,
                            related_name="province_address",
                            on_delete=models.CASCADE,
                            db_index=True,
                            verbose_name=_("Province"),
                            blank=True)
    city = models.ForeignKey(City,
                            related_name="city_address",
                            on_delete=models.CASCADE,
                            db_index=True,
                            verbose_name=_("Ville/District"),
                            blank=True)
    commune = models.ForeignKey(Commune,
                            related_name="commune_address",
                            on_delete=models.CASCADE,
                            db_index=True,
                            verbose_name=_("Commune"),
                            blank=True)
    neighborhood = models.CharField(_("Quartier"), max_length=200, blank=True)
    country = models.CharField(_("Pays"), max_length=50, default="R.D. Congo")
    census_teams = GenericRelation(CensusTeam)
    census_agents = GenericRelation(CensusAgent)
    household_records = GenericRelation(HouseholdRecord)
    individual_addresses = GenericRelation(Individual)
    """
    FOR INDIVIDUAL PLACE OF BIRTH DO THIS
    individual_places_of_birth = GenericRelation(
                        object_id_field="place_of_birth_object_id",
                        content_type_field="place_of_birth_type")
    """

    def __repr__(self):
        return "street: %s, city %s, commune: %s, region: %s" % \
                    (self.street, self.city.name,
                    self.commune.name, self.province.name)

    def __str__(self):
        return self.street + " " + self.commune.name + self.city.name + " " + \
                                                            self.province.name

    class Meta:
        verbose_name = _("Adresse")
        verbose_name_plural = _("Adresses")


class RuralAddress(AbstractTimeStampedModel):
    village_name = models.CharField(_("Village"),
                                max_length=255,
                                blank=True)
    sector = models.CharField(_("Secteur"),
                                max_length=255,
                                blank=True)
    territory = models.CharField(_("Térritoire"),
                                max_length=255,
                                blank=True)
    district = models.CharField(_("District"),
                                max_length=255,
                                blank=True)
    province = models.ForeignKey(Province,
                            related_name="province_ruraladdress",
                            on_delete=models.CASCADE,
                            db_index=True,
                            verbose_name=_("Province"),
                            blank=True)
    census_teams = GenericRelation(CensusTeam)
    census_agents = GenericRelation(CensusAgent)
    household_records = GenericRelation(HouseholdRecord)
    individual_addresses = GenericRelation(Individual)

    def __repr__(self):
        return "Village ID: %s Name: %s" % (self.id, self.village_name)

    def __str__(self):
        return "Village ID: %s Name: %s" % (self.id, self.village_name)

    class Meta:
        verbose_name = _("Adresse Milieu Rural")
        verbose_name_plural = _("Adresses Milieux Ruraux")


"""
@receiver(post_save, sender=User, dispatch_uid="create_user_auth_token")
def create_user_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            Token.objects.create(user=instance)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
"""
