# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ProvinceListAPIView, CityListAPIView, CommuneListAPIView, \
                ResidentialSituationCodeListAPIView, HouseholdRecordAPIView, \
                HeadHouseholdLinkCodeListAPIView, ReligionCodeListAPIView, \
                HandicapTypeCodeListAPIView, MarriageTypeCodeListAPIView, \
                OccupationStatusCodeListAPIView, MarritalStatusCodeListAPIView,\
                OccupationSituationCodeListAPIView, CensusAgentAPIView, \
                CensusTeamListAPIView, LoginAPIView, LogoutAPIView, \
                ManageCensusAgentView


app_name = "census_api"
urlpatterns = [
    path('provinces/', ProvinceListAPIView.as_view(), name="provinces"),
    path('cities/', CityListAPIView.as_view(), name="cities"),
    path('communes/', CommuneListAPIView.as_view(), name="communes"),
    path('resident_situation_codes/',
            ResidentialSituationCodeListAPIView.as_view(),
            name="resident_situation_codes"),
    path('head_household_links/',
            HeadHouseholdLinkCodeListAPIView.as_view(),
            name="head_household_links"),
    path('religion_codes/', ReligionCodeListAPIView.as_view(),
            name="religion_codes"),
    path('handicap_type_codes/', HandicapTypeCodeListAPIView.as_view(),
            name="handicap_type_codes"),
    path('marriage_type_codes/', MarriageTypeCodeListAPIView.as_view(),
            name="marriage_type_codes"),
    path('occup_status_codes/', OccupationStatusCodeListAPIView.as_view(),
            name="occup_status_codes"),
    path('marrital_status_codes/', MarritalStatusCodeListAPIView.as_view(),
            name="marrital_status_codes"),
    path('occup_situation_codes/',
            OccupationSituationCodeListAPIView.as_view(),
            name="occup_situation_codes"),
    path('census_agents/', CensusAgentAPIView.as_view(), name='census_agents'),
    path('census_agents_management/', ManageCensusAgentView.as_view(),
            name="census_agents_management"),
    path('census_teams/', CensusTeamListAPIView.as_view(), name='census_teams'),
    path('census_household_records/', HouseholdRecordAPIView.as_view(),
            name='census_household_records'),
    path('sign_in/', LoginAPIView.as_view(), name='login'),
    path('sign_out/', LogoutAPIView.as_view(), name='logout'),
    path('api_token_auth/', obtain_auth_token, name='api_token_auth')
]
