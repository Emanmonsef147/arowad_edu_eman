from rest_framework import serializers
from .models import *
class CountrySerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    name = serializers.CharField(required=False)


class StateSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    country_id = serializers.IntegerField(required=False)

class CitiesSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    state_id = serializers.IntegerField(required=False)

class LangsSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    lang_name = serializers.CharField(required=False)
    lang_code = serializers.CharField(required=False)
    rtl = serializers.CharField(required=False)
    flag_code = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
    active = serializers.IntegerField(required=False)
    status = serializers.IntegerField(required=False)
    ip_address = serializers.CharField(required=False)

class ReligionSerializer(serializers.Serializer):
    id= serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
    active = serializers.IntegerField(required=False)
    ip_address = serializers.CharField(required=False)