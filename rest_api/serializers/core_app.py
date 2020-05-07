from django.contrib.auth.models import User
from rest_framework import serializers
import re
import sys, traceback

from uza_billet.queries_utils import ModelsQueries


from core_app.models import Country, Region, City, Commune, Address


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
    is_active = serializers.BooleanField(default=False)
        
        
    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError("First Name cannot be null")
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError("Last Name cannot be null")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password cannot be empty")
        return value

    def validate_username(self, value):
        if not value:
            try:
                value = "{}_{}".format(self.first_name, self.last_name)
            except Exception:
                pass
        return value

    def validate_is_active(self, value):
        if not value or not isinstance(value, bool):
            raise serializers.ValidationError("is_active should be boolean")
        return

    def validate_email(self, value):
        if not is_valid_email(value):
            raise serializers.ValidationError("email is not valid email address")
        return value 

    def save(self):
        print("IN SAVE USER METHOD")
        print(self.validated_data)
        
        try:
            user = User()
            user.first_name = self.validated_data.get("first_name")
            user.last_name = self.validated_data.get("last_name")
            user.email = self.validated_data.get("email")
            username = "{}_{}".format(user.first_name, user.last_name)
            user.username = self.validated_data.get("username", username)
            user.password = self.validated_data.get("password")
            #user.is_active = self.validated_data.get("is_active", True)
            user.is_active = True
            print("USER ADMIN BEFORE SAVE")
            print(user.__dict__)
            user.save()
        except Exception:
            user = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        if user:
            return user
        else:
            return None
        
    

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('pk', 'english_name', 'french_name', 'local_name', 'region',
                    'continent', 'code', 'created_date', 'modified_date')
        read_only_fields = (
                'pk', 'english_name', 'french_name', 'local_name', 'region',
                    'continent', 'code', 'created_date', 'modified_date')


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(required=False, read_only=True)

    class Meta:
        model = Region
        fields = ('pk', 'name', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'country')
        read_only_fields = (
                'pk', 'name', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'country')


class CitySerializer(serializers.ModelSerializer):
    country =  CountrySerializer(required=False, read_only=True)
    region = RegionSerializer(required=False, read_only=True)

    class Meta:
        model = City
        fields = ('pk', 'name', 'slug', 'description', 'is_active',
                    'city_type', 'created_date', 'modified_date', 'country',
                    'region')
        read_only_fields = (
                'pk', 'name', 'slug', 'description', 'is_active',
                    'city_type', 'created_date', 'modified_date', 'country',
                    'region')


class CommuneSerializer(serializers.ModelSerializer):
    city = CitySerializer(required=False, read_only=True)

    class Meta:
        model = Commune
        fields = ('pk', 'name', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'city')
        read_only_fields = (
                'pk', 'name', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'city')


class AddressSerializer(serializers.Serializer):
    region = RegionSerializer(required=False)
    city = CitySerializer(required=False)
    commune = CommuneSerializer(required=False)
    street = serializers.CharField(max_length=255)

    """
    def validate_region(self, value):
        return value

    def validate_city(self, value):
        return value

    def validate_commune(self, value):
        return value"""

    def validate_street(self, value):
        if not value:
            raise serializers.ValidationError("Street cannot be null")
        return value    

    def save(self, more_data={}):
        print("IN SAVE ADDRESS METHOD")
        print(self.validated_data)

        street = self.validated_data.get("street", None)
        province = more_data.get("region", None)
        city = more_data.get("city", None)
        commune = more_data.get("commune", None)

        print("PRINTING SELF REGION")
        print(self.data)
        
        try:
            address = Address()
            address.street = street
            address.region = province
            address.city = city
            address.commune = commune
            print("IN BEORE SAVE ADDRESS")
            address.save()
        except Exception:
            address = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        if address:
            return address
        else:
            return None














        
        

        
