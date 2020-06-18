from django.contrib.auth.models import User
from core_app.models import Address, Region, City, Commune, Country
from .models import BusinessEntity, BusinessTeam, BusinessTeamMember,\
                                IndividualEntity, Event
import sys, traceback


class ModelsQueries:

    def __init__(self):
        pass

    @staticmethod
    def get_address_by_id(id):
        address = None
        if not id:
            return address
        try:
            address = Address.objects.get(id=id)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        return address

    @staticmethod
    def get_region_by_id(id):
        region = None
        if not id:
            return region
        try:
            region = Region.objects.get(id=id)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return region

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
    def get_country_by_id(id):
        country = None
        if not id:
            return country
        try:
            country = Country.objects.get(id=id)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return country

    @staticmethod
    def get_default_country():
        country = None
        try:
            country = Country.objects.get(english_name="D.R. Congo")
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return country

    @staticmethod
    def get_all_events():
        events = None
        try:
            events = Event.objects.all()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return events
        
        
        

        
        


