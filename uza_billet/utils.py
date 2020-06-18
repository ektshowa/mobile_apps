from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login as auth_login
from django.forms import model_to_dict
from core_app.models import Address
from .models import BusinessEntity, BusinessTeam, BusinessTeamMember
from .queries_utils import ModelsQueries
from rest_api.serializers.core_app import UserSerializer, AddressSerializer
from rest_api.serializers.uza_billet import BusinessEntitySerializer, \
                                            BusinessTeamSerializer, \
                                            BusinessTeamMemberSerializer, \
                                            IndividualBuyerSerializer, \
                                            EventSerializer
import sys, traceback
import datetime


def get_data(**form_data):
    input_fields = {}
    if form_data is not None:
            items = form_data.items()
            for item in items:
                input_fields[item[0]] = item[1]
    return input_fields


class UzaBilletFormDataProcessing:

    def __init__(self, *args, **kwargs):
        pass

    ##FORM_DATA COME FROM THE FORM(FRONT END)
    ##THE ADDRESS SERIALIZSER WILL BE INITALIZE WITH
    ##THE RESULT FROM THIS METHOD. SAME WILL BE DONE FOR
    ##OTHER DATA(BUSINESS_ADMIN, BUSINESS, TEAM...)    
    def _get_address_data(self, **form_data):
        data = get_data(**form_data)
        address = {}

        if data:
            address = {"street": data.get("street", ""),
                    "region": data.get("select_province", ""),
                    "city": data.get("select_city", ""),
                    "commune": data.get("select_commune", "")}
        return address

    def _get_admin_user_data(self, **form_data):
        data = get_data(**form_data)
        business_admin = {}

        print("IN GET ADMIN USER DATA")
        print(data) 
        if data:
            #HERE CHECK DATA["USERNAME"] VALUE
            business_admin = {
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "username": data.get("username", ""),
                "email": data.get("email", ""),
                "password": data.get("password", ""),
                "is_active": data.get("is_active", False)}
        return business_admin

    def _get_auth_user_data(self, **form_data):
        data = get_data(**form_data)
        user = {}

        print("IN GET USER DATA")
        print(data) 
        if data:
            #HERE CHECK DATA["USERNAME"] VALUE
            user = {
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "username": data.get("username", ""),
                "email": data.get("email", ""),
                "password": data.get("password", ""),
                "is_active": data.get("is_active", True)}
        return user

    def _get_business_admin_data(self, admin_user, **form_data):
        data = get_data(**form_data)
        business_admin = {}
        if admin_user and not isinstance(admin_user, AnonymousUser):
            if data:
                business_admin = {
                    "admin_user": admin_user,
                    "admin_phone_number": data.get("admin_phone_number", "")
                }
        return business_admin

    def _get_business_data(self, **form_data):
        data = get_data(**form_data)
        business = {}

        if data:
            business = {
                "business_name": data.get("business_name", ""),
                "identification_number": data.get("identification_number", ""), 
                "business_email": data.get("business_email", ""),
                "business_phone_number": data.get("business_phone_number", "")}
        return business
        
    def _get_team_member_data(self, **form_data):
        data = get_data(**form_data)
        team_member = {}

        if data:
            team_member = {
                "is_active": data.get("is_active", False),
                "is_team_admin": data.get("is_team_admin", False),
                "month_birth": data.get("month_birth", ""),
                "year_birth": data.get("year_birth", ""),
                "phone_number": data.get("admin_phone_number", "")
            }
        return team_member

    def _get_individual_buyer_data(self, **form_data):
        data = get_data(**form_data)
        individual_buyer = {}

        if data:
            individual_buyer = {
                "month_birth": data.get("month_birth", ""),
                "year_birth": data.get("year_birth", ""),
                "phone_number": data.get("phone_number", "")
            }
        return individual_buyer

    def _get_event_data(self, **form_data):
        data = get_data(**form_data)
        event = {}
        if data:
            event = {
                "name": data.get("event_name", ""),
                "description": data.get("event_description", ""),
                "unit_price": data.get("price", ""),
                "sale_price": data.get("sale_price", ""),
                "event_date": data.get("date_event", None),
                "sale_from": data.get("date_sale_from", None),
                "sale_to": data.get("date_sale_to", None)
            }
        return event

    def save_user_admin(self, **form_data):
        business_admin_data = self._get_admin_user_data(**form_data)
        print("PRINTING BUSINESS ADMIN DATA")
        print(business_admin_data)
        serializer = UserSerializer(data=business_admin_data)
        print("IN SAVE USER ADMIN")
        print(serializer.__dict__)
        if serializer.is_valid(raise_exception=True):
            user_admin_saved = serializer.save()
            if user_admin_saved:
                result = {"success": True, "data": user_admin_saved}
            else:
                result = {"success": False}
        else:
            data = serializer.errors
            result = {"success": False, "data": data}
        return result

    def save_auth_user(self, **form_data):
        auth_user_data = self._get_auth_user_data(**form_data)
        print("PRINTING USER DATA")
        print(auth_user_data)
        serializer = UserSerializer(data=auth_user_data)
        if serializer.is_valid(raise_exception=True):
            auth_user_saved = serializer.save()
            if auth_user_saved:
                result = {"success": True, "data": auth_user_saved}
            else:
                result = {"success": False}
        else:
            data = serializer.errors
            result = {"success": False, "data": data}
        return result

    def save_address(self, **form_data):
        data = self._get_address_data(**form_data)
        print("PRINTING ADDRESS DATA")
        print(data)

        street = data.get("street", None)
        province_id = data.get("region", None)
        province = ModelsQueries.get_region_by_id(province_id)
        city_id = data.get("city", None)
        city = ModelsQueries.get_city_by_id(city_id)
        commune_id = data.get("commune", None)
        commune = ModelsQueries.get_commune_by_id(commune_id)

        address_data = {"street": street}
        more_data = {"region": province,
                    "city": city,
                    "commune": commune}

        serializer = AddressSerializer(data=address_data)
        print("SERIALIZER IN SAVE ADDRESS")
        print(serializer.__dict__)
        
        if serializer.is_valid():
            address_saved = serializer.save(more_data=more_data)
            if address_saved:
                result = {"success": True, "data": address_saved}
            else:
                result = {"success": False}
            print("IS VALID SERIALIZER RESULT")
            print(result)
        else:
            print("PRINT SAVE ADDRESS ERROR")
            print(serializer.errors)
            data = serializer.errors
            result = {"success": False, "data": data}
        return result
        
    def save_business(self, more_data={"admin_user":None, "address":None},
                                                                **form_data):
        data = self._get_business_data(**form_data)

        print("PRINTING BUSINESS DATA")
        print(data)

        business_name = data.get("business_name", "")
        identification_number = data.get("identification_number", "")
        business_email = data.get("business_email", "")
        business_phone_number = data.get("business_phone_number", "")

        if not business_name:
            return None

        business_data = {"business_name": business_name,
                        "identification_number": identification_number,
                        "email": business_email,
                        "phone_number": business_phone_number}
        serializer = BusinessEntitySerializer(data=business_data)
        print("SERIALIZER IN SAVE BUSINESS")
        print(serializer.__dict__)

        admin_user = more_data.get("admin_user", None)
        address = more_data.get("address", None)

        if serializer.is_valid():
            business_saved = serializer.save(
                                        admin_user=admin_user, address=address)
            if business_saved:
                result = {"success": True, "data": business_saved}
            else:
                result = {"success": False}
            print("IS VALID SERIALIZER RESULT")
            print(result)
        else:
            print("PRINT SAVE BUSINESS ERROR")
            print(serializer.errors)
            data = serializer.errors
            result = {"success": False, "data": data}
        return result

    def save_event(self, address=None, **form_data):
        data = self._get_event_data(**form_data)

        print("PRINTING EVENT DATA")
        print(data)

        name = data.get("name")
        description = data.get("description")
        unit_price = data.get("unit_price")
        sale_price = data.get("sale_price")
        event_date = data.get("event_date")
        sale_from = data.get("sale_from")
        sale_to = data.get("sale_to")

        event_date = datetime.datetime.strptime(event_date, "%d/%m/%Y").\
                                                strftime("%Y-%m-%d %H:%M:%S")
        sale_from = datetime.datetime.strptime(sale_from, "%d/%m/%Y").\
                                                strftime("%Y-%m-%d %H:%M:%S")
        sale_to = datetime.datetime.strptime(sale_to, "%d/%m/%Y").\
                                                strftime("%Y-%m-%d %H:%M:%S")

        event_data = {"name": name,
                    "description": description,
                    "unit_price": unit_price,
                    "sale_price": sale_price,
                    "event_date": event_date,
                    "sale_from": sale_from,
                    "sale_to": sale_to}
        serializer = EventSerializer(data=event_data)
        print("SERIALIZER IN SAVE EVENT")
        print(serializer.__dict__)

        if serializer.is_valid():
            event_saved = serializer.save(address=address)
            if event_saved:
                result = {"success": True, "data": event_saved}
            else:
                result = {"success": False}
            print("IS VALID SERIALIZER RESULT")
            print(result)
        else:
            print("PRINT SAVE EVENT ERROR")
            print(serializer.errors)
            data = serializer.errors
            result = {"success": False, "data": data}
        return result


    def save_business_team(self, more_data={"team_lead":None,
                                                "business_entity":None}):
        team_lead = more_data.get("team_lead", None)
        business_entity = more_data.get("business_entity", None)

        if not team_lead or not business_entity:
            return None

        team_data = {"is_active": True}
        serializer = BusinessTeamSerializer(data=team_data)
        print("SERIALIZER IN SAVE BUSINESS TEAM")
        print(serializer.__dict__)

        if serializer.is_valid():
            team_saved = serializer.save(team_lead=team_lead,
                                            business_entity=business_entity)
            if team_saved:
                result = {"success": True, "data": team_saved}
            else:
                result = {"success": False}
            print("IS VALID SERIALIZER RESULT")
            print(result)
        else:
            print("PRINT SAVE BUSINESS ERROR")
            print(serializer.errors)
            data = serializer.errors
            result = {"success": False, "data": data}
        return result

    def save_team_member(self, more_data={"auth_user":None,
                                        "business_team":None}, **form_data):
        auth_user = more_data.get("auth_user")
        business_team = more_data.get("business_team")
        if not auth_user or not business_team:
            return None

        data = self._get_team_member_data(**form_data)

        print("PRINTING TEAM MEMBER DATA")
        print(data)

        is_active = data.get("is_active", True)
        is_team_admin = data.get("is_team_admin", True)
        month_birth = data.get("month_birth", "")
        year_birth = data.get("year_birth", "")
        phone_number = data.get("phone_number", "")

        team_member_data =  {"is_active": is_active,
                            "is_team_admin": is_team_admin,
                            "month_birth": month_birth,
                            "year_birth": year_birth,
                            "phone_number": phone_number}
        serializer = BusinessTeamMemberSerializer(data=team_member_data)
        print("SERIALIZER IN SAVE TEAM MEMBER")
        print(serializer.__dict__)

        if serializer.is_valid():
            team_member_saved = serializer.save(auth_user=auth_user,
                                                business_team=business_team)
            if team_member_saved:
                result = {"success": True, "data": team_member_saved}
            else:
                result = {"success": False}
            print("IS VALID SERIALIZER RESULT")
            print(result)
        else:
            print("PRINT SAVE BUSINESS ERROR")
            print(serializer.errors)
            data = serializer.errors
            result = {"success": False, "data": data}
        return result

    def save_individual_buyer(self, more_data={"auth_user":None,
                                                "address":None}, **form_data):
        auth_user = more_data.get("auth_user")
        address = more_data.get("address")
        if not auth_user:
            return None

        data = self._get_individual_buyer_data(**form_data)

        print("PRINTING INDIVIDUAL BUYER DATA")
        print(data)

        month_birth = data.get("month_birth", "")
        year_birth = data.get("year_birth", "")
        phone_number = data.get("phone_number", "")

        individual_buyer_data = {"month_birth": month_birth,
                                "year_birth": year_birth,
                                "phone_number": phone_number}

        serializer = IndividualBuyerSerializer(data=individual_buyer_data)
        print("SERIALIZER IN SAVE INDIVIDUAL BUYER")
        print(serializer.__dict__)

        if serializer.is_valid():
            individual_buyer_saved = serializer.save(auth_user=auth_user,
                                                    address=address)
            if individual_buyer_saved:
                result = {"success": True, "data": individual_buyer_saved}
            else:
                result = {"sucess": False}
            print("IS VALID SERIALIZER RESULT")
            print(result)
        else:
            print("PRINT SAVE BUSINESS ERROR")
            print(serializer.errors)
            data = serializer.errors
            result = {"success": False, "data": data}
        return result


class SerializersQueries:
    def __init__(self):
        pass

    @staticmethod
    def get_all_events_data():
        events = ModelsQueries.get_all_events()
        data = None    
        if events:
            try:
                serializer = EventSerializer(events, many=True)
                data = serializer.data
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        return data        
        