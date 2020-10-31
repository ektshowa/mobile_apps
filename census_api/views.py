from django.shortcuts import get_object_or_404
#from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from .serializers.core import ProvinceSerializer, CitySerializer,\
                            CommuneSerializer
from .serializers.census import ReligionCodeSerializer, \
                            ResidentialSituationCodeSerializer, \
                            HeadHouseholdLinkCodeSerializer, \
                            HandicapTypeCodeSerializer, \
                            OccupationStatusCodeSerializer, \
                            OccupationSituationCodeSerializer, \
                            MarritalStatusCodeSerializer, \
                            MarriageTypeCodeSerializer, \
                            CensusTeamSerializer
from census.models import Province, City, CensusAgent
from census.queries_utils import ModelsQueries
from census.utils import CensusAgentFormDataProcessing, ExtendedEncoder
import sys
import traceback


def authenticate(username=None, password=None):
    result = None
    user = ModelsQueries.get_user_by_username(username)
    is_active = False
    try:
        is_active = user.is_active
    except Exception:
        pass
    print("AUTHENTICATE USER")
    print(user)
    if not user or not is_active:
        return None
    pwd_is_valid = check_password(password, user.password)
    result = user if pwd_is_valid else None
    return result


class ProvinceListAPIView(ListAPIView):
    serializer_class = ProvinceSerializer
    queryset = ModelsQueries.get_all_provinces()
    #permission_classes = [permissions.AllowAny]

    def list(self, request):
        print("IN PROVINCE LIST VIEW")
        queryset = self.get_queryset()
        #print("PRINTING QUERYSET")
        #print(queryset)
        serializer = ProvinceSerializer(queryset, many=True)
        print("PRINTING SERIALIZER DATA")
        #print(serializer.data)
        return Response(serializer.data,
                        headers={"Access-Control-Allow-Origin":"*"})


class CityListAPIView(ListAPIView):
    serializer_class = CitySerializer
    queryset = ModelsQueries.get_all_cities()

    def list(self, request):
        province = None
        try:
            province = get_object_or_404(Province,
                                    id=request.GET.get('province_id'))
        except Exception:
            province = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        try:
            queryset = self.get_queryset().filter(province=province)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data,
                                headers={"Access-Control-Allow-Origin":"*"})


class CommuneListAPIView(ListAPIView):
    serializer_class = CommuneSerializer
    queryset = ModelsQueries.get_all_communes()

    def list(self, request):
        city = None
        try:
            city = get_object_or_404(City,
                                    id=request.GET.get('city_id'))
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        try:
            queryset = self.get_queryset().filter(city=city)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ResidentialSituationCodeListAPIView(ListAPIView):
    serializer_class = ResidentialSituationCodeSerializer
    queryset = ModelsQueries.get_all_residentialSituationCode()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class HeadHouseholdLinkCodeListAPIView(ListAPIView):
    serializer_class = HeadHouseholdLinkCodeSerializer
    queryset = ModelsQueries.get_all_headHouseholdLinkCode()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ReligionCodeListAPIView(ListAPIView):
    serializer_class = ReligionCodeSerializer
    queryset = ModelsQueries.get_all_religionCode()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class HandicapTypeCodeListAPIView(ListAPIView):
    serializer_class = HandicapTypeCodeSerializer
    queryset = ModelsQueries.get_all_handicapTypeCode()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class OccupationStatusCodeListAPIView(ListAPIView):
    serializer_class = OccupationStatusCodeSerializer
    queryset = ModelsQueries.get_all_occupationStatusCode()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class OccupationSituationCodeListAPIView(ListAPIView):
    serializer_class = OccupationSituationCodeSerializer
    queryset = ModelsQueries.get_all_occupationSituationCode()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class MarritalStatusCodeListAPIView(ListAPIView):
    serializer_class = MarritalStatusCodeSerializer
    queryset = ModelsQueries.get_all_marritalStatusCode()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class MarriageTypeCodeListAPIView(ListAPIView):
    serializer_class = MarriageTypeCodeSerializer
    queryset = ModelsQueries.get_all_marriageTypeCode()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CensusTeamListAPIView(ListAPIView):
    serializer_class = CensusTeamSerializer

    def get_queryset(self, **kwargs):
        input_fields = {}
        if kwargs is not None:
            items = kwargs.items()
            for item in items:
                input_fields[item[0]] = item[1]
        province_id = input_fields.get("province_id", "")
        city_id = input_fields.get("city_id", "")
        commune_id = input_fields.get("commune_id", "")
        territory = input_fields.get("territory", "")
        census_teams = None
        if province_id and city_id and commune_id:
            census_teams = \
                ModelsQueries.get_census_team_by_province_city_commune(
                                    province_id=province_id,
                                    city_id=city_id,
                                    commune_id=commune_id)
        elif province_id and territory:
            census_teams = ModelsQueries.get_census_team_by_province_territory(
                                    province_id=province_id,
                                    territory=territory)
        return census_teams

    def list(self, request):
        province_id = request.GET.get("province_id", "")
        city_id = request.GET.get("city_id", "")
        commune_id = request.GET.get("commune_id", "")
        territory = request.GET.get("territory", "")
        kwargs = {"province_id": province_id,
                    "city_id": city_id,
                    "commune_id": commune_id,
                    "territory": territory}
        queryset = self.get_queryset(**kwargs)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data,
                                headers={"Access-Control-Allow-Origin": "*"})


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                            context={'request': request})
        print("AUTHTOKEN SERIALIZER")
        print(serializer.__dict__)
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                print("AUTHTOKEN")
                print(user)
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {'token': token.key,
                    'user_id': user.pk,
                    'email': user.email},
                    headers={"Access-Control-Allow-Origin": "*"}
                )
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        return Response(
                    {'token': "",
                    'user_id': "",
                    'email': ""},
                    headers={"Access-Control-Allow-Origin": "*"}
                )


class LoginAPIView(APIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    #permission_classes = (IsAuthenticated,)

    def post(self, request):
        print("LOGIN VIEW USER")
        print(request.user)

        if request.user.is_authenticated:
            print("USER AUTHENTICATED")
            return JsonResponse({"data": None, "err_code": 17})

        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        print("USERNAME AND PASSWORD")
        print("username: %s password: %s" % (username, password))
        user = authenticate(username=username, password=password)
        err_code = ""

        if user is None:
            err_code = 1
            data = None
        elif not user.is_active:
            err_code = 16
            data = None
        else:
            login(request, user)
            data = user
        if data:
            data = json.dumps(data, cls=ExtendedEncoder)

        #return JsonResponse(data, encoder=ExtendedEncoder)
        return JsonResponse({"data": data, "err_code": err_code})

    def get(self, request):
        data = {}
        return Response(data,
                    template_name="census/sign-in.html")


class LogoutAPIView(APIView):
    renderer_classes = [JSONRenderer, ]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request.user.auth_token.delete()
        print("USER DECONNECTION")
        return JsonResponse({"data": True})


class CensusAgentAPIView(APIView):
    queryset = CensusAgent.objects.none()
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def get(self, request):
        data = {}
        return Response(data,
                    template_name="census/census-agent-sign-up.html")

    def post(self, request):
        print("CENSUS AGENT VIEW")
        print(request.POST)
        address_type = request.POST.get("zone_type")[0]
        census_agent_data = {
            "phone_number_1": request.POST.get("phone_number_1"),
            "phone_number_2": request.POST.get("phone_number_2"),
            "is_manager": request.POST.get("is_manager", False)
        }
        agent_user = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
            "password_confirm": request.POST.get("password_confirm")
        }
        if address_type == "zone_type_rural":
            address_data = {
                "address_type": address_type,
                "select_province": request.POST.get("select_province"),
                "district": request.POST.get("district"),
                "territory": request.POST.get("territory"),
                "sector": request.POST.get("sector"),
                "village_name": request.POST.get("village_name")
            }
        else:
            address_data = {
                "address_type": address_type,
                "select_province": request.POST.get("select_province"),
                "select_city": request.POST.get("select_city"),
                "select_commune": request.POST.get("select_commune"),
                "street": request.POST.get("street"),
                "house_num": request.POST.get("house_num"),
                "neighborhood": request.POST.get("neighborhood")
            }

        data_processing = CensusAgentFormDataProcessing()

        try:
            address_result = data_processing.save_address(**address_data)
        except Exception:
            address_result = {"success": False, "data": None}
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        print("PRINTING ADDRESS SAVED RESULT")
        print(address_result)

        address = address_result.get("data", None)
        try:
            user_agent_result = data_processing.save_agent_user(**agent_user)
        except Exception:
            user_agent_result = {"success": False, "data": None}
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        can_create_agent = False
        census_team_id = request.POST.get("census_team", None)
        if not census_team_id:
            census_team_id = request.POST.get("hidden_team", None)
        try:
            census_team = int(census_team_id)
        except Exception:
            census_team = None
        census_team = ModelsQueries.get_census_team_by_id(id=census_team)

        can_create_agent = True if census_team else False
        address = address_result.get("data", None)
        can_create_agent = True if address else False
        auth_user = user_agent_result.get("data", None)
        can_create_agent = True if auth_user else False

        if can_create_agent:
            try:
                census_agent_result = \
                        data_processing.save_census_agent(
                                                auth_user=auth_user,
                                                census_team=census_team,
                                                address=address,
                                                **census_agent_data)
            except Exception:
                census_agent_result = {"success": False, "data": None}
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
        else:
            census_agent_result = {"success": False, "data": None}

        return JsonResponse(census_agent_result)