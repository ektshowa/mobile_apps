from rest_framework import serializers

from core_app.models import Country, Region, City, Commune, Address


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('pk', 'english_name', 'french_name', 'local_name', 'region',
                    'continent', 'code', 'created_date', 'modified_date')


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(required=False, read_only=True)

    class Meta:
        model = Region
        fields = ('pk', 'name', 'code', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'country')


class CitySerializer(serializers.ModelSerializer):
    country =  CountrySerializer(required=False, read_only=True)
    region = RegionSerializer(required=False, read_only=True)

    class Meta:
        model = City
        fields = ('pk', 'name', 'code', 'slug', 'description', 'is_active',
                    'city_type', 'created_date', 'modified_date', 'country',
                    'region')


class CommuneSerializer(serializers.ModelSerializer):
    city = CitySerializer(required=False, read_only=True)

    class Meta:
        model = Commune
        fields = ('pk', 'name', 'code', 'slug', 'description', 'is_active',
                    'created_date', 'modified_date', 'city')


class AddressSerializer(serializers.ModelSerializer):
    region = RegionSerializer(required=False, read_only=True)
    city = CitySerializer(required=False, read_only=True)
    commune = CommuneSerializer(required=False, read_only=True)

    class Meta:
        model = Address
        fields = ('pk', 'region', 'city', 'commune', 'street')

