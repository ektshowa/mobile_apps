from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from core_app.models import Address
from rest_api.serializers.address import AddressSerializer
import sys, traceback
