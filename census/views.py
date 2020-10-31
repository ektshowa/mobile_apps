from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.template.response import TemplateResponse
from .queries_utils import ModelsQueries


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
