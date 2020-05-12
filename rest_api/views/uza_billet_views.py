from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import login as auth_login
#from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import status
from core_app.models import Address
from rest_api.serializers.core_app import AddressSerializer
from rest_api.serializers.uza_billet import BusinessEntitySerializer
from uza_billet.models import BusinessEntity
from uza_billet.utils import UzaBilletFormDataProcessing
import sys, traceback


#class CreateRetrieveBusiness(ListCreateAPIView):
#    serializer_class = BusinessEntitySerializer()
#    queryset = BusinessEntity.objects.all()

class BusinessView(APIView):
    queryset = User.objects.none()
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    
    def post(self, request):
        print("IN BUSINESS VIEW POST")
        address_data = {
            "street": request.POST.get("street"),
            "select_province": request.POST.get("select_province"),
            "select_city": request.POST.get("select_city"),
            "select_commune": request.POST.get("select_commune")
        }
        print(request.POST)
        user_admin_data = {
            "first_name": request.POST.get("first_name", ""),
            "last_name": request.POST.get("last_name", ""),
            "email": request.POST.get("admin_email", ""),
            "username": request.POST.get("username", ""),
            "password": request.POST.get("password", "")
        }
        if not user_admin_data.get("username", ""):
            user_admin_data["username"] = "{}_{}".format(
                                       user_admin_data["first_name"],
                                       user_admin_data["last_name"])
        user_admin_data["is_active"] = True    
        print("PRINTING USER ADMIN DATA")
        print(user_admin_data)
        business_data = {
            "business_name": request.POST.get("business_name", ""),
            "identification_number": request.POST.get(
                                        "identification_number", ""),
            "business_email": request.POST.get("business_email", ""),
            "business_phone_number": request.POST.get(
                                        "business_phone_number", "")
        }
        team_member_data = {
            "month_birth": request.POST.get("month_birth", ""),
            "year_birth": request.POST.get("year_birth", ""),
            "admin_phone_number": request.POST.get("admin_phone_number", "")    
        }
        data_processing = UzaBilletFormDataProcessing()
        try:
            admin_result = data_processing.save_user_admin(**user_admin_data)
        except Exception:
            admin_result = {}
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        print("ADMIN RESULT AFTER SAVED")
        print(admin_result)

        admin_success = admin_result.get("success", False)
        admin_user = admin_result.get("data", None)
        address_result = {"success": False, "data": None}
        business_result = {"success": False, "data": None}
        business_team_result = {"success": False, "data": None}

        print("PRINTING SUCCESS AND ADMIN_USER")
        print("{} {}".format(admin_success, admin_user))

        if admin_success:
            #LOGIN ADMIN AFTER FULL PROCESS IS DONE
            #auth_login(request, admin_user)
            #admin_user.user_permissions.add("core_app.add_address",
            #                                "uza_billet.add_businessentity",
            #                                "uza_billet.add_businessteam")
            address_result = data_processing.save_address(**address_data)
            print("PRINTING ADDRESS SAVED RESULT")
            print(address_result)
            
            address = address_result.get("data", None)
            more_data = {"admin_user": admin_user, "address": address}
            business_result = data_processing.save_business(
                                    more_data=more_data, **business_data)
            print("PRINTING BUSINESS SAVED RESULT")
            print(business_result)

        business_success = business_result.get("success", False)
        if business_success and admin_success:
            business_entity = business_result.get("data")
            more_data = {"team_lead": admin_user,
                        "business_entity": business_entity}
            business_team_result = data_processing.save_business_team(
                                                        more_data=more_data)
            print("PRINTING BUSINESS TEAM SAVED RESULT")
            print(business_team_result)
        else:
            business_entity = None

        business_team_success = business_team_result.get("success", False)
        if business_team_success and business_entity:
            business_team = business_team_result.get("data", None)
            more_data = {"auth_user": admin_user,
                        "business_team": business_team}
            team_member_data["is_active"] = True
            team_member_data["is_team_admin"] = True
            team_member_result = data_processing.save_team_member(
                                    more_data=more_data, **team_member_data)
            print("PRINTING TEAM MEMBER")
            print(team_member_result)   

        if admin_success:
            return Response({"admin_user":admin_user},
                                status=status.HTTP_201_CREATED,
                                template_name="uza_billet/index.html")
        else:
            return Response({"admin_user":admin_user},
                                status=status.HTTP_400_BAD_REQUEST,
                                template_name="uza_billet/index.html")    

    def get(self, request):
        data = {}
        return Response(data, template_name="uza_billet/create_business.html")


class LoginView(APIView):
    queryset = User.objects.none()

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        data = {}
        return Response(data, template_name="uza_billet/login.html")