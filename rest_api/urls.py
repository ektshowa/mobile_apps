from django.urls import path, include
from .views.core_app_views import RegionListAPIView , \
                                    CityListAPIView, \
                                    CommuneListAPIView
from .views.uza_billet_views import BusinessView, LoginView


app_name = "rest_api"
urlpatterns = [
    path('regions/', RegionListAPIView.as_view(), name="regions"),
    path('cities/', CityListAPIView.as_view(), name="cities"),
    path('communes/', CommuneListAPIView.as_view(), name="communes"),
    path('login/', LoginView.as_view(), name="login"),
    path('business_entities/', BusinessView.as_view(),
                                            name="business_entities"),
]