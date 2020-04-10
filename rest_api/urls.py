from django.urls import path, include
from .views.core_app_views import RegionListAPIView , \
                                    CityListAPIView, \
                                    CommuneListAPIView


app_name = "rest_api"
urlpatterns = [
    path('regions/', RegionListAPIView.as_view(), name="regions"),
    path('cities/', CityListAPIView.as_view(), name="cities"),
    path('communes/', CommuneListAPIView.as_view(), name="communes"),
]