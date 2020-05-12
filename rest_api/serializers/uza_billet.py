from rest_framework import serializers
from uza_billet.models import BusinessEntity, BusinessTeam, BusinessTeamMember,\
                                IndividualEntity
from .core_app import UserSerializer, AddressSerializer, is_valid_email
import sys, traceback


class BusinessEntitySerializer(serializers.Serializer):
    account_admin = UserSerializer(required=False)
    address = AddressSerializer(required=False)

    business_name = serializers.CharField(max_length=100)
    identification_number = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=30)
    ##SET THESE FIELDS REQUIRED=FALSE, THEN UNCOMMENT
    #created_date = serializers.DateTimeField()
    #modified_date = serializers.DateTimeField()

    def validate_business_name(self, value):
        if not value:
            raise serializers.ValidationError("Business Name cannot be null")
        return value

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone Number cannot be null")
        return value

    def validate_identification_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone Number cannot be null")
        return value

    def validate_email(self, value):
        if not is_valid_email(value):
            raise serializers.ValidationError(
                                        "email is not a valid email address")
        return value

    def save(self, admin_user=None, address=None):
        if not admin_user:
            return None

        print("IN SAVE BUSINESS METHOD")
        print(self.validated_data)

        business_name = self.validated_data.get("business_name", "")
        identification_number = self.validated_data.get(
                                        "identification_number", "")
        email = self.validated_data.get("email", "")
        phone_number = self.validated_data.get("phone_number", "")

        print("PRINTING SELF BUSINESS DATA")
        print(self.data)

        try:
            business_entity = BusinessEntity()
            business_entity.business_name = business_name
            business_entity.identification_number = identification_number
            business_entity.email = email
            business_entity.phone_number = phone_number
            business_entity.account_admin = admin_user
            business_entity.address = address
            print("IN BEFORE SAVE BUSINESS")
            print(business_entity)
            business_entity.save()
        except Exception:
            business_entity = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return business_entity
        

class BusinessTeamSerializer(serializers.Serializer):
    team_lead = UserSerializer(required=False)
    business_entity = BusinessEntitySerializer(required=False)

    is_active = serializers.BooleanField()
    ##SET THESE FIELDS REQUIRED=FALSE, THEN UNCOMMENT
    #created_date = serializers.DateTimeField()
    #modified_date = serializers.DateTimeField()

    def validate_is_active(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_activate should be boolean")
        return value

    def save(self, team_lead=None, business_entity=None):
        if not team_lead or not business_entity:
            return None

        print("IN SAVE BUSINESSTEAM")
        print(self.validated_data)

        is_active = self.validated_data.get("is_active", False)

        print("PRINTING SELF BUSINESSTEAM")
        print(self.data)

        try:
            business_team = BusinessTeam()
            business_team.team_lead = team_lead
            business_team.business_entity = business_entity
            business_team.is_active = is_active
            print("IN BEFORE BUSINESS TEAM SAVE")
            print(business_team.__dict__)
            business_team.save()
        except Exception:
            business_team = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return business_team
                

class BusinessTeamMemberSerializer(serializers.Serializer):
    auth_user = UserSerializer(required=False)
    business_team = BusinessTeamSerializer(required=False)

    is_active = serializers.BooleanField()
    is_team_admin = serializers.BooleanField()
    month_birth = serializers.CharField(max_length=2)
    year_birth = serializers.CharField(max_length=4)
    phone_number = serializers.CharField(max_length=30)
    ##SET THESE FIELDS REQUIRED=FALSE, THEN UNCOMMENT
    #created_date = serializers.DateTimeField()
    #modified_date = serializers.DateTimeField()

    def validate_is_active(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_activate should be boolean")
        return value 

    def validate_is_team_admin(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_team_admin should be boolean")
        return value

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("phone number cannot be null")
        return value

    def validate_month_birth(self, value):
        if not value:
            raise serializers.ValidationError("month_birth should be boolean")
        return value
    
    def validate_year_birth(self, value):
        if not value:
            raise serializers.ValidationError("year_birth should be boolean")
        return value

    def save(self, auth_user=auth_user, business_team=business_team):
        if not auth_user or not business_team:
            return None

        print("IN SAVE TEAMMEMBER METHOD")
        print(self.validated_data)

        is_active = self.validated_data.get("is_active", True)
        is_team_admin = self.validated_data.get("is_team_active", True)
        month_birth = self.validated_data.get("month_birth", "")
        year_birth = self.validated_data.get("year_birth", "")
        phone_number = self.validated_data.get("phone_number", "")

        print("PRINTING SELF TEAMMEMBER DATA")
        print(self.data)

        try:
            team_member = BusinessTeamMember()
            team_member.is_active = is_active
            team_member.is_team_admin = is_team_admin
            team_member.month_birth = month_birth
            team_member.year_birth = year_birth
            team_member.phone_number = phone_number
            team_member.auth_user = auth_user
            team_member.business_team = business_team
            print("IN BEFORE SAVE TEAMMEMBER")
            print(team_member.__dict__)
            team_member.save()
        except Exception:
            team_member = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return team_member
    
    
class IndividualEntitySerializer(serializers.Serializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

    auth_user = UserSerializer()
    address = AddressSerializer()

    month_birth = serializers.CharField(max_length=2)
    year_birth = serializers.CharField(max_length=4)
    phone_number = serializers.CharField(max_length=30)
    created_date = serializers.DateTimeField()
    modified_date = serializers.DateTimeField()
    
    
