# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


app_name = "census"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^web-provinces/$", views.load_provinces, name="load_provinces"),
    url(r"^web-cities-of-province/$", views.load_cities_of_province,
                                            name="load_cities_of_province"),
    url(r"^web-communes-of-city/$", views.load_communes_of_city,
                                            name="load_communes_of_city"),
    url(r"^web-censusteam-of-commune/$", views.load_census_teams,
                                            name="load_census_teams"),
]
