from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, \
                                    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from core_app.models import Country, Region, City, Commune
from rest_api.serializers.core_app import RegionSerializer, CountrySerializer,\
                                        CitySerializer, CommuneSerializer
import sys, traceback


class RegionListAPIView(ListAPIView):
    """
        API View to list Regions
    """
    serializer_class = RegionSerializer
    queryset = Region.objects.all()

    def list(self, request):
        print("IN LIST REGIONS VIEW")
        country = None
        try:
            country = get_object_or_404(Country,
                                            french_name="D.R. CONGO")
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
                        
        queryset = self.get_queryset().filter(country=country)
        serializer = RegionSerializer(queryset, many=True)
        return Response(serializer.data)
        


class CityListAPIView(ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def list(self, request):
        print("IN LIST CITIES")
        country = None
        region = None
        try:
            country = get_object_or_404(Country,
                                            french_name="D.R. CONGO")
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        try:
            region = get_object_or_404(Region,
                                id=request.GET.get('province_id'))
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        queryset = self.get_queryset().filter(country=country,
                                                region=region)
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data)


class CommuneListAPIView(ListAPIView):
    serializer_class = CommuneSerializer
    queryset = Commune.objects.all()

    def list(self, request):
        print("IN LIST COMMUNES")
        city = None
        try:
            city = get_object_or_404(City,
                                id=request.GET.get('city_id'))
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        
        queryset = self.get_queryset().filter(city=city)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

         
        

