# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from census.models import Province, City, Commune, ResidentialSituationCode, \
                        HeadHouseholdLinkCode, ReligionCode, HandicapTypeCode, \
                        OccupationStatusCode, OccupationSituationCode, \
                        MarritalStatusCode, MarriageTypeCode, CensusTeam, \
                        Address, RuralAddress

import sys
import traceback


class ModelsQueries:

    @staticmethod
    def get_all_provinces():
        provinces = Province.objects.all()
        return provinces

    @staticmethod
    def get_provinces_for_json():
        try:
            provinces = list(Province.objects.filter(is_active=1).values(
                                            "id", "name", "slug", "country"))
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            provinces = None
        return provinces

    @staticmethod
    def get_cities_of_provinces_for_json(province_id=None):
        province = None
        if province_id:
            try:
                province = Province.objects.get(id=province_id)
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        if province:
            try:
                cities = list(City.objects.filter(province=province,
                                                                is_active=1)
                                            .values("id", "name", "slug",
                                                    "city_type", "province"))
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                cities = None
        else:
            cities = None
        return cities

    @staticmethod
    def get_all_cities():
        cities = City.objects.all()
        return cities

    @staticmethod
    def get_communes_of_cities_for_json(city_id=None):
        city = None
        if city_id:
            try:
                city = City.objects.get(id=city_id)
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        if city:
            try:
                communes = list(Commune.objects.filter(city=city, is_active=1).
                                        values("id", "name", "slug", "city"))
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                communes = None
        else:
            communes = None
        return communes

    @staticmethod
    def get_all_communes():
        communes = Commune.objects.all()
        return communes

    @staticmethod
    def get_all_residentialSituationCode():
        situat_codes = ResidentialSituationCode.objects.all()
        return situat_codes

    @staticmethod
    def get_all_headHouseholdLinkCode():
        link_codes = HeadHouseholdLinkCode.objects.all()
        return link_codes

    @staticmethod
    def get_all_religionCode():
        rel_codes = ReligionCode.objects.all()
        return rel_codes

    @staticmethod
    def get_all_handicapTypeCode():
        hand_codes = HandicapTypeCode.objects.all()
        return hand_codes

    @staticmethod
    def get_all_occupationStatusCode():
        occ_codes = OccupationStatusCode.objects.all()
        return occ_codes

    @staticmethod
    def get_all_occupationSituationCode():
        occ_codes = OccupationSituationCode.objects.all()
        return occ_codes

    @staticmethod
    def get_all_marritalStatusCode():
        marr_codes = MarritalStatusCode.objects.all()
        return marr_codes

    @staticmethod
    def get_all_marriageTypeCode():
        marr_codes = MarriageTypeCode.objects.all()
        return marr_codes

    @staticmethod
    def get_province_by_id(id):
        province = None
        if not id:
            return province
        try:
            province = Province.objects.get(id=id)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return province

    @staticmethod
    def get_city_by_id(id):
        city = None
        if not id:
            return city
        try:
            city = City.objects.get(id=id)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return city

    @staticmethod
    def get_commune_by_id(id):
        commune = None
        if not id:
            return commune
        try:
            commune = Commune.objects.get(id=id)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return commune

    @staticmethod
    def get_all_census_teams():
        census_teams = None
        try:
            census_teams = CensusTeam.objects.all()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return census_teams

    @staticmethod
    def get_census_team_by_id(id):
        census_team = None
        if not id:
            return census_team
        try:
            census_team = CensusTeam.objects.get(id=id)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return census_team

    @staticmethod
    def get_census_team_by_province_territory(
                                        province_id=None, territory=None):
        census_teams = None
        try:
            province = Province.objects.get(id=province_id)
        except Exception:
            province = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        try:
            rural_addresses = RuralAddress.objects.filter(
                                province=province, territory=territory)
        except Exception:
            rural_addresses = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        try:
            address_type = ContentType.objects.get_for_model(RuralAddress)
            census_teams = CensusTeam.objects.filter(
                                address_type__pk=address_type.id,
                                object_id__in=rural_addresses)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return census_teams

    @staticmethod
    def get_census_team_by_province_city_commune(
                            province_id=None, city_id=None, commune_id=None):
        census_teams = None

        try:
            province = Province.objects.get(id=province_id)
        except Exception:
            province = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        try:
            city = City.objects.get(id=city_id)
        except Exception:
            city = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        try:
            commune = Commune.objects.get(id=commune_id)
        except Exception:
            commune = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        try:
            addresses = Address.objects.filter(province=province,
                                                city=city,
                                                commune=commune)
        except Exception:
            addresses = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        try:
            address_type = ContentType.objects.get_for_model(Address)
            census_teams = CensusTeam.objects.filter(
                                address_type__pk=address_type.id,
                                object_id__in=addresses)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return census_teams

    @staticmethod
    def check_is_email_unique(email=None):
        if not email:
            return False
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            result = True
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return result

    @staticmethod
    def check_is_username_unique(username=None):
        if not username:
            return False
        result = False
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            result = True
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return result

    @staticmethod
    def get_user_by_username(username=None):
        if not username:
            return None
        user = None
        try:
            user = User.objects.get(username=username)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return user

    @staticmethod
    def get_user_auth_token(user):
        token = None
        try:
            token, created = Token.objects.get_or_create(user=user)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return token
