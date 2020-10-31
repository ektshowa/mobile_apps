# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from census.queries_utils import ModelsQueries
import re
import sys
import traceback

from census.models import Province, City, Commune, Address, RuralAddress


def is_valid_email(email):
    regex_string = "^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$"
    if email:
        return bool(re.match(regex_string, email))
    else:
        return False


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255)
    username = "{}_{}".format(first_name, last_name)
    password = serializers.CharField(max_length=255)
    password_confirm = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=False)

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("Last Name cannot be null")
        return value

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First Name cannot be null")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password cannot be null")
        return value

    def validate_password_confirm(self, value):
        if not value:
            raise serializers.ValidationError("Password confirm cannot be null")
        return value

    def validate_username(self, value):
        if not value:
            try:
                value = "{}_{}".format(self.first_name, self.last_name)
            except Exception:
                pass
        return value

    #def validate_is_active(self, value):
    #    if not value or not isinstance(value, bool):
    #        raise serializers.ValidationError("is_active should be boolean")
    #    return value

    def validate_email(self, value):
        if not is_valid_email(value):
            raise serializers.ValidationError("email is not valid email address")
        return value

    def email_is_unique(self, email=email):
        is_unique = ModelsQueries.check_is_email_unique(email=email)
        return is_unique

    def username_is_unique(self, username=username):
        is_unique = ModelsQueries.check_is_username_unique(username=username)
        return is_unique

    def create_username_from_existing(self, username):
        name_parts = username.split("_")
        size = len(name_parts)
        result = None
        try:
            last_part = name_parts[size - 1]
        except Exception:
            last_part = None
        if last_part and last_part.isdigit():
            last_part = ++int(last_part)
            if last_part < 10:
                last_part = "0{}".format(str(last_part))
            else:
                last_part = str(last_part)
            result = "{}_{}".format(username, last_part)
        return result

    def passwords_are_matching(self, password1=None, password2=None):
        if password1 and password2:
            return password1 == password2
        else:
            return False

    def save(self):
        print("IN SAVE USER METHOD")
        print(self.validated_data)

        err_codes = []
        email = self.validated_data.get("email")
        first_name = self.validated_data.get("first_name")
        last_name = self.validated_data.get("last_name")
        username = "{}_{}".format(first_name, last_name)

        is_email_unique = self.email_is_unique(email=email)
        if not is_email_unique:
            err_codes.append(4)
        is_username_unique = self.username_is_unique(username=username)
        new_username = None
        if not is_username_unique:
            new_username = self.create_username_from_existing(username)
            if not new_username:
                err_codes.append(8)
        password = self.validated_data.get("password")
        password_confirm = self.validated_data.get("password_confirm")
        is_password_match = self.passwords_are_matching(
                                password1=password, password2=password_confirm)
        if not is_password_match:
            err_codes.append(15)
        if err_codes:
            return {"success": False, "err_codes": err_codes}

        try:
            user = User()
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if not new_username:
                user.username = username
            else:
                user.username = new_username
            user.password = password
            user.is_active = False
            print("USER BEFORE SAVE")
            print(user.__dict__)
            user.set_password(password)
            user.save()
        except Exception:
            user = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        if user:
            result = {"success": True, "data": user}
        else:
            result = {"success": False, "err_codes": [7]}

        return result


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('pk', 'name', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'country')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'country')


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(required=False, read_only=True)

    class Meta:
        model = City
        fields = ('pk', 'name', 'slug', 'description', 'is_active', 'city_type',
                    'province', 'created_date', 'modified_date', 'country')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'is_active',
                    'province', 'created_date', 'modified_date', 'country',
                    'city_type')


class CommuneSerializer(serializers.ModelSerializer):
    city = CitySerializer(required=False, read_only=True)

    class Meta:
        model = Commune
        fields = ('pk', 'name', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'city')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'city')


class AddressSerializer(serializers.Serializer):
    province = ProvinceSerializer(required=False)
    city = CitySerializer(required=False)
    commune = CommuneSerializer(required=False)
    street = serializers.CharField(max_length=255)
    house_num = serializers.CharField(max_length=255)
    neighborhood = serializers.CharField(max_length=255)

    def validate_street(self, value):
        if not value:
            raise serializers.ValidationError("street cannot be null")
        return value

    def validate_house_num(self, value):
        if not value:
            raise serializers.ValidationError("house_num cannot be null")
        return value

    def validate_neighborhood(self, value):
        if not value:
            raise serializers.ValidationError("neighborhood cannot be null")
        return value

    def save(self, more_data={}):
        print("IN SAVE ADDRESS METHOD")
        print(self.validated_data)

        street = self.validated_data.get("street", None)
        house_num = self.validated_data.get("house_num", None)
        neighborhood = self.validated_data.get("neighborhood", None)
        commune = more_data.get("commune", None)
        city = more_data.get("city", None)
        province = more_data.get("province", None)

        print("PRINTING SELF PROVINCE")
        print(self.data)

        try:
            address = Address()
            address.street = street
            address.house_num = house_num
            address.neighborhood = neighborhood
            address.province = province
            address.city = city
            address.commune = commune
            print("IN BEFORE SAVE ADDRESS")
            address.save()
        except Exception:
            address = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        if address:
            return address
        else:
            return None


class RuralAddressSerializer(serializers.Serializer):
    province = ProvinceSerializer(required=False)

    def validate_village_name(self, value):
        if not value:
            raise serializers.ValidationError("village_name cannot be null")
        return value

    def validate_sector(self, value):
        if not value:
            raise serializers.ValidationError("sector cannot be null")
        return value

    def validate_district(self, value):
        if not value:
            raise serializers.ValidationError("district cannot be null")
        return value

    def validate_territory(self, value):
        if not value:
            raise serializers.ValidationError("sector cannot be null")
        return value

    def save(self, province=None):
        print("IN SAVE RURAL ADDRESS METHOD")
        print(self.validated_data)

        village_name = self.validated_data.get("village_name")
        sector = self.validated_data.get("sector")
        territory = self.validated_data.get("territory")
        district = self.validated_data.get("district")

        print("PRINTING SELF RURAL ADDRESS")
        print(self.data)

        try:
            rural_address = RuralAddress()
            rural_address.village_name = village_name
            rural_address.sector = sector
            rural_address.territory = territory
            rural_address.district = district
            rural_address.province = province
            print("IN BEFORE SAVE RURAL ADDRESS")
            rural_address.save()
        except Exception:
            rural_address = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        return rural_address