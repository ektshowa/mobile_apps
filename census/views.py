import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET
from django.template.response import TemplateResponse
from .queries_utils import ModelsQueries
from .utils import ExtendedEncoder


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


def index(request, template="census/index.html", extra_context=None):
    return TemplateResponse(request, template)


@require_GET
def load_provinces(request):
    # Getting regions for the default country
    provinces = ModelsQueries.get_provinces_for_json()
    if not provinces:
        provinces = []
    return JsonResponse(provinces, safe=False)


@require_GET
def load_cities_of_province(request):
    province_id = request.GET.get("province_id")
    cities = ModelsQueries.get_cities_of_provinces_for_json(
                                                        province_id=province_id)
    if not cities:
        cities = []
    return JsonResponse(cities, safe=False)


@require_GET
def load_communes_of_city(request):
    city_id = request.GET.get("city_id")
    communes = ModelsQueries.get_communes_of_cities_for_json(city_id=city_id)
    if not communes:
        communes = []
    return JsonResponse(communes, safe=False)


@require_GET
def load_census_teams(request):
    province_id = request.GET.get("province_id")
    city_id = request.GET.get("city_id")
    commune_id = request.GET.get("commune_id")
    census_teams = ModelsQueries.get_census_team_by_province_city_commune(
                        province_id=province_id,
                        city_id=city_id,
                        commune_id=commune_id)
    print("PRINTING CENSUS_TEAMS")
    print(census_teams)
    if not census_teams:
        census_teams = []
    return JsonResponse(census_teams, safe=False)


@csrf_protect
def login_view(request):
    print("LOGIN VIEW USER")
    print(request.user)

    if request.user.is_authenticated:
        print("USER AUTHENTICATED")
        data = json.dumps(request.user, cls=ExtendedEncoder)
        return JsonResponse({"data": data, "err_code": 17})

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


def logout_view(request):
    logout(request)
    print("USER DECONNECTION")
    return JsonResponse({"data": True})




"""
def load_cities_of_region(request):
    region_id = request.POST.get("id")
    region = CoreModelsQueries.get_region_from_id(region_id)
    cities = CoreModelsQueries.get_cities_of_region_country(region=region)
    if not cities:
        cities = {"id": ""}
    return JsonResponse(cities, safe=False)


def load_communes_of_city(request):
    city_id = request.POST.get("id")
    city = CoreModelsQueries.get_city_from_id(city_id)
    communes = CoreModelsQueries.get_communes_of_city(city)
    if not communes:
        communes = {"id": ""}
    return JsonResponse(communes, safe=False)
"""
