# -*- coding: utf-8 -*-
from rest_framework import serializers
from .core import AddressSerializer, UserSerializer, RuralAddressSerializer
import traceback
import sys

from census.models import ResidentialSituationCode, HeadHouseholdLinkCode, \
                    ReligionCode, HandicapTypeCode, OccupationStatusCode, \
                    OccupationSituationCode, MarritalStatusCode, \
                    MarriageTypeCode, CensusTeam, CensusAgent, HouseholdRecord,\
                    Individual


class ResidentialSituationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialSituationCode
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date')


class HeadHouseholdLinkCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadHouseholdLinkCode
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date')


class ReligionCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligionCode
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date')


class HandicapTypeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandicapTypeCode
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date')


class OccupationStatusCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupationStatusCode
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date')


class OccupationSituationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupationSituationCode
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date')


class MarritalStatusCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarritalStatusCode
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date')


class MarriageTypeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarriageTypeCode
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date')


class CensusTeamSerializer(serializers.ModelSerializer):
    try:
        address_object = AddressSerializer(required=False)
    except Exception:
        pass
    try:
        address_object = RuralAddressSerializer(required=False)
    except Exception:
        pass

    class Meta:
        model = CensusTeam
        fields = ('pk', 'name', 'slug', 'description', 'code', 'created_date',
                    'modified_date', 'phone_number_1', 'address_object')
        read_only_fields = ('pk', 'name', 'slug', 'description', 'code',
                    'created_date', 'modified_date', 'phone_number_1',
                    'address_object')


class CensusAgentSerializer(serializers.Serializer):
    auth_user = UserSerializer(required=False)
    census_team = CensusTeamSerializer(required=False)
    try:
        address_object = AddressSerializer(required=False)
    except Exception:
        pass
    try:
        address_object = RuralAddressSerializer(required=False)
    except Exception:
        pass

    def validate_phone_number_1(self, value):
        if not value:
            raise serializers.ValidationError("phone_number_1 cannot be null")
        return value

    #def validate_phone_number_2(self, value):
    #    if not value:
    #        raise serializers.ValidationError("phone_number_2 cannot be null")
    #    return value

    #def validate_is_manager(self, value):
    #    if not isinstance(value, bool):
    #        raise serializers.ValidationError("is_manager should be boolean")
    #    return value

    def save(self, auth_user=None, address=None, census_team=None):
        print("IN SAVE AGENT SERIALIZER")
        print("AUTH USER")
        print(auth_user)
        print("ADDRESS")
        print(address)
        print("CENSUS TEAM")
        print(census_team)
        if not auth_user or not address or not census_team:
            return None

        print("IN SAVE CENSUS AGENT")
        print(self.validated_data)

        phone_number_1 = self.validated_data.get("phone_number_1", "")
        phone_number_2 = self.validated_data.get("phone_number_2", "")
        is_manager = self.validated_data.get("is_manager", False)

        print("PRINTING SELF CENSUSAGENT")
        print(self.data)

        try:
            census_agent = CensusAgent()
            census_agent.phone_number_1 = phone_number_1
            census_agent.phone_number_2 = phone_number_2
            census_agent.is_manager = is_manager
            census_agent.address_object = address
            census_agent.auth_user = auth_user
            census_agent.census_team = census_team
            print("IN BEFORE CENSUS AGENT SAVE")
            print(census_agent.__dict__)
            census_agent.save()
        except Exception:
            census_agent = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return census_agent


class HouseholdRecordSerializer(serializers.Serializer):
    census_agent = CensusAgentSerializer(required=False)
    try:
        address_object = AddressSerializer(required=False)
    except Exception:
        pass
    try:
        address_object = RuralAddressSerializer(required=False)
    except Exception:
        pass

    is_own_filled = serializers.BooleanField()
    filling_date = serializers.DateTimeField()
    male_present_resident_numb = serializers.CharField(max_length=2)
    female_present_resident_numb = serializers.CharField(max_length=2)
    male_absent_resident_numb = serializers.CharField(max_length=2)
    female_absent_resident_numb = serializers.CharField(max_length=2)
    visiting_male_numb = serializers.CharField(max_length=2)
    visiting_female_numb = serializers.CharField(max_length=2)

    def validate_is_own_filled(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("is_own_filled should be boolean")
        return value

    def validate_filling_date(self, value):
        if not value:
            raise serializers.ValidationError("filling_date cannot be null")
        return value

    def validate_male_present_resident_numb(self, value):
        if not value:
            raise serializers.ValidationError("male_present_resident_numb "
                                                            "cannot be null")
        return value

    def validate_female_present_resident_numb(self, value):
        if not value:
            raise serializers.ValidationError("female_present_resident_numb "
                                                            "cannot be null")
        return value

    def validate_male_absent_resident_numb(self, value):
        if not value:
            raise serializers.ValidationError("male_absent_resident_numb "
                                                            "cannot be null")
        return value

    def validate_female_absent_resident_numb(self, value):
        if not value:
            raise serializers.ValidationError("female_absent_resident_numb "
                                                            "cannot be null")
        return value

    def validate_visiting_male_numb(self, value):
        if not value:
            raise serializers.ValidationError("visiting_male_numb "
                                                            "cannot be null")
        return value

    def validate_visiting_female_numb(self, value):
        if not value:
            raise serializers.ValidationError("visiting_female_numb "
                                                            "cannot be null")
        return value

    def save(self, census_agent=None, address=None):
        if not census_agent or not address:
            return None

        if not isinstance(census_agent, CensusAgent):
            raise serializers.ValidationError("The param census_agent should"
                    " of type CensusAgent")

        print("IN SAVE HOUSEHOLDRECORD SERIALIZER")
        print(self.validated_data)

        is_own_filled = self.validated_data.get("is_own_filled", False)
        filling_date = self.validated_data.get("filling_date", None)
        male_present_resident_numb = \
                self.validated_data.get("male_present_resident_numb")
        female_present_resident_numb = \
                self.validated_data.get("female_present_resident_numb")
        male_absent_resident_numb = \
                self.validated_data.get("male_absent_resident_numb")
        female_absent_resident_numb = \
                self.validated_data.get("female_absent_resident_numb")
        visiting_male_numb = self.validated_data.get("visiting_male_numb")
        visiting_female_numb = self.validated_data.get("visiting_female_numb")

        print("PRINTING SELF HOUSEHOLD_RECORD DATA")
        print(self.data)

        try:
            household_record = HouseholdRecord()
            household_record.is_own_filled = is_own_filled
            household_record.filling_date = filling_date
            household_record.male_present_resident_numb = \
                                male_present_resident_numb
            household_record.female_present_resident_numb = \
                                female_present_resident_numb
            household_record.male_absent_resident_numb = \
                                           male_absent_resident_numb
            household_record.female_absent_resident_numb = \
                                           female_absent_resident_numb
            household_record.visiting_male_numb = visiting_male_numb
            household_record.visiting_female_numb = visiting_female_numb
            household_record.census_agent = census_agent
            household_record.address_object = address
            print("IN BEFORE SAVE HOUSEHOLD_RECORD")
            print(household_record)
            household_record.save()
        except Exception:
            household_record = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        return household_record


class IndividualSerializer(serializers.Serializer):
    auth_user = UserSerializer(required=False)
    marrital_status = MarritalStatusCodeSerializer(required=False)
    marriage_type = MarriageTypeCodeSerializer(required=False)
    head_household_link = HeadHouseholdLinkCodeSerializer(required=False)
    religion_code = ReligionCodeSerializer(required=False)
    handicap_type_code = HandicapTypeCodeSerializer(required=False)
    occupation_status_code = OccupationStatusCodeSerializer(required=False)
    occupation_situation_code = OccupationSituationCodeSerializer(
                                                                required=False)
    household_record = HouseholdRecordSerializer(required=False)

    date_of_birth = serializers.DateTimeField()
    age = serializers.IntegerField()
    occupation = serializers.CharField(max_length=255)
    highest_diploma = serializers.CharField(max_length=255)
    try:
        address_object = AddressSerializer(required=False)
    except Exception:
        pass
    try:
        address_object = RuralAddressSerializer(required=False)
    except Exception:
        pass
    try:
        place_of_birth_object = AddressSerializer(required=False)
    except Exception:
        pass
    try:
        place_of_birth_object = RuralAddressSerializer(required=False)
    except Exception:
        pass

    def validate_date_of_birth(self, value):
        if not value:
            raise serializers.ValidationError("date_of_birth "
                                                            "cannot be null")
        return value

    def validate_age(self, value):
        if not value:
            raise serializers.ValidationError("age cannot be null")
        return value

    def validate_occupation(self, value):
        if not value:
            raise serializers.ValidationError("occupation cannot be null")
        return value

    def validate_highest_diploma(self, value):
        if not value:
            raise serializers.ValidationError("highest_diploma cannot be null")
        return value

    def save(self, **more_data):
        input_params = {}
        if more_data is not None:
            items = more_data.items()
            for item in items:
                input_params[item[0]] = item[1]
        print("IN SAVE INDIVIDUAL METHOD")
        print(self.validated_data)

        auth_user = input_params.get("auth_user", None)
        address = input_params.get("address", None)
        household_record = input_params.get("household_record", None)

        if not auth_user or not address or not household_record:
            print("SAVE INDIVIDUAL -- USER OR ADDRESS OR HOUSEHOLD CANNOT NULL")
            return None

        marrital_status = input_params.get("marrital_status", None)
        marriage_type = input_params.get("marriage_type", None)
        head_household_link = input_params.get("head_household_link", None)
        religion_code = input_params.get("religion_code", None)
        handicap_type_code = input_params.get("handicap_type_code", None)
        occupation_status_code = input_params.get(
                                                "occupation_status_code", None)
        occupation_situation_code = input_params.get(
                                            "occupation_situation_code", None)
        place_of_birth = input_params.get("place_of_birth", None)

        print("PRINTING SELF INDIVIDUAL")
        print(self.data)

        try:
            individual = Individual()
            individual.auth_user = auth_user
            individual.address_object = address
            individual.household_record = household_record
            individual.marrital_status = marrital_status
            individual.marriage_type = marriage_type
            individual.head_household_link = head_household_link
            individual.religion_code = religion_code
            individual.handicap_type_code = handicap_type_code
            individual.occupation_situation_code = occupation_situation_code
            individual.occupation_status_code = occupation_status_code
            individual.place_of_birth_object = place_of_birth
        except Exception:
            individual = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

        return individual