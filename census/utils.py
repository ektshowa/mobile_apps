# -*- coding: utf-8 -*-
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from census_api.serializers.core import AddressSerializer, UserSerializer, \
                                RuralAddress
from census_api.serializers.census import CensusAgentSerializer
from .models import Address
from .queries_utils import ModelsQueries

import sys, traceback
import datetime


def get_data(**form_data):
    input_fields = {}
    if form_data is not None:
        items = form_data.items()
        for item in items:
            input_fields[item[0]] = item[1]
    return input_fields


class ExtendedEncoder(DjangoJSONEncoder):

    def default(self, o):

        if isinstance(o, Model):
            return model_to_dict(o)

        return super().default(o)


class CensusAgentFormDataProcessing:

    def __init__(self):
        pass

    def _get_address_data(self, **form_data):
        data = get_data(**form_data)
        address = {}

        if data:
            address_type = data.get("zone_type", "")
            if not address_type or address_type == "zone_type_urban":
                address = {
                        "zone_type": "zone_type_urban",
                        "select_province": data.get("select_province", ""),
                        "select_city": data.get("select_city", ""),
                        "select_commune": data.get("select_commune", ""),
                        "neighborhood": data.get("neighborhood", ""),
                        "street": data.get("street", ""),
                        "house_num": data.get("house_num", "")}
            elif address_type == "zone_type_rural":
                address = {
                        "zone_type": address_type,
                        "select_province": data.get("select_province", ""),
                        "district": data.get("district", ""),
                        "territory": data.get("territory", ""),
                        "sector": data.get("sector", ""),
                        "village_name": data.get("village_name", "")}
        return address

    def _get_agent_user_data(self, **form_data):
        data = get_data(**form_data)
        user_agent = {}

        print("IN GET USER AGENT DATA")
        print(data)
        if data:
            user_agent = {
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
                "username": data.get("username", ""),
                "email": data.get("email", ""),
                "password": data.get("password", ""),
                "password_confirm": data.get("password_confirm", ""),
                "is_active": False}
        return user_agent

    def _get_agent_data(self, **form_data):
        data = get_data(**form_data)
        agent = {}

        print("IN GET AGENT DATA")
        print(data)
        if data:
            agent = {
                "census_team": data.get("census_team", ""),
                "phone_number_1": data.get("phone_number_1", ""),
                "phone_number_2": data.get("phone_number_2", ""),
                "address_type": data.get("address_type", "")}
        return agent

    def save_address(self, **form_data):
        data = self._get_address_data(**form_data)
        print("PRINTING ADDRESS DATA")
        print(data)

        address_saved = None
        address_type = data.get("zone_type", "")
        print("PRINTING ADDRESS TYPE")
        print(address_type)
        province_id = data.get("select_province", "")
        province = ModelsQueries.get_province_by_id(province_id)
        if address_type == "zone_type_urban":
            city_id = data.get("select_city", "")
            city = ModelsQueries.get_city_by_id(city_id)
            commune_id = data.get("select_commune", "")
            commune = ModelsQueries.get_commune_by_id(commune_id)
            neighborhood = data.get("neighborhood", "")
            street = data.get("street", "")
            house_num = data.get("house_num", "")

            address_data = {"neighborhood": neighborhood,
                            "street": street,
                            "house_num": house_num}
            more_data = {"province": province,
                        "city": city,
                        "commune": commune}
            serializer = AddressSerializer(data=address_data)
            print("SERIALIZER IN SAVE ADDRESS")
            print(serializer.__dict__)

            if serializer.is_valid():
                address_saved = serializer.save(more_data=more_data)
            else:
                print("PRINT SAVE ADDRESS ERROR")
                print(serializer.errors)
                data = serializer.errors
                result = {"success": False, "data": data}

        elif address_type == "zone_type_rural":
            village_name = data.get("village_name", "")
            sector = data.get("sector", "")
            territory = data.get("territory", "")
            district = data.get("district", "")

            address_data = {"village_name": village_name,
                            "sector": sector,
                            "territory": territory,
                            "district": district}
            serializer = RuralAddress(data=address_data)
            print("SERIALIZER IN SAVE RURAL ADDRESS")
            print(serializer.__dict__)

            if serializer.is_valid():
                address_saved = serializer.save(province=province)
            else:
                print("PRINT SAVE ADDRESS ERROR")
                print(serializer.errors)
                data = serializer.errors
                result = {"success": False, "data": data}

        if address_saved:
            result = {"success": True, "data": address_saved}
        else:
            result = {"success": False}
        print("IS VALID SERIALIZER RESULT")
        print(result)

        return result

    def save_agent_user(self, **form_data):
        user_agent_data = self._get_agent_user_data(**form_data)
        print("PRINTING AGENT USER DATA")
        print(user_agent_data)
        serializer = UserSerializer(data=user_agent_data)
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
        else:
            print("AGENT USER ERRORS")
            print(serializer.errors)
            result = {"success": False, "err_codes": [7]}
        return result

    def save_census_agent(self, auth_user=None, census_team=None,
                                                address=None, **form_data):
        data = self._get_agent_data(**form_data)

        print("PRINTING CENSUS AGENT DATA")
        print(data)

        phone_number_1 = data.get("phone_number_1", "")
        phone_number_2 = data.get("phone_number_2", "")
        is_manager = data.get("is_manager", False)
        agent_data = {
            "phone_number_1": phone_number_1,
            "phone_number_2": phone_number_2,
            "is_manager": is_manager}
        serializer = CensusAgentSerializer(data=agent_data)
        print("SERIALIZER IN SAVE CENSUS AGENT")
        print(serializer.__dict__)

        if serializer.is_valid():
            agent_saved = serializer.save(
                                        auth_user=auth_user,
                                        address=address,
                                        census_team=census_team)
            if agent_saved:
                user_auth_token = ModelsQueries.get_user_auth_token(auth_user)
                result_data = {"id": agent_saved.id,
                        "first_name": agent_saved.auth_user.first_name,
                        "last_name": agent_saved.auth_user.last_name,
                        "username": agent_saved.auth_user.username,
                        "phone_number": agent_saved.phone_number_1,
                        "census_team": agent_saved.census_team.id,
                        "auth_token": user_auth_token.key
                    }
                result = {"success": True, "data": result_data}
            else:
                result = {"success": False}
            print("IS VALID SERIALIZER RESULT")
            print(result)
        else:
            print("PRINT SAVE AGENT ERROR")
            print(serializer.errors)
            data = serializer.errors
            result = {"success": False, "data": data}
        return result
