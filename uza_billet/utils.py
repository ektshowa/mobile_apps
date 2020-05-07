from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login as auth_login
from django.forms import model_to_dict
from core_app.models import Address
from .models import BusinessEntity, BusinessTeam, BusinessTeamMember
from .queries_utils import ModelsQueries
from rest_api.serializers.core_app import UserSerializer, AddressSerializer
from rest_api.serializers.uza_billet import BusinessEntitySerializer, \
                                            BusinessTeamSerializer, \
                                            BusinessTeamMemberSerializer
import sys, traceback


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
                "phone_number": data.get("phone_number", "")
            }
        return team_member

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

        



        """
        business_entity = BusinessEntity()
        try:
            business_entity.address = address
            business_entity.account_admin = user_admin
            business_entity.business_name = business_name
            business_entity.business_email = business_email
            business_entity.business_phone_number = business_phone_number
            business_entity.identification_number = identification_number
            business_entity.save()
            result["business_entity"] = business_entity
        except Exception:
            business_entity = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        
        if not business_entity:
            return result

        business_team = BusinessTeam()
        try:
            business_team.business_entity = business_entity
            business_team.team_lead = user_admin
            business_team.is_active = True
            business_team.save()
            result["business_team"] = business_team
        except Exception:
            business_team = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        if not business_team:
            return result
            
        team_member = BusinessTeamMember()
        try:
            team_member.auth_user = user_admin
            team_member.business_team = business_team
            team_member.is_active = True
            team_member.is_team_admin = True
            team_member.phone_number = admin_email.get("admin_phone_number", "")
            team_member.save()
            result["team_member_admin"] = team_member
        except Exception:
            team_member = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        return result"""
        