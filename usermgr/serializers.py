from rest_framework import serializers
from django.http import JsonResponse
import re


class activationSerializer(serializers.Serializer):
    token=serializers.CharField()
class forgetpassSerializer(serializers.Serializer):
    email=serializers.CharField()

class resetpassSerializer(serializers.Serializer):
    token=serializers.CharField()
    password=serializers.CharField()
    re_password=serializers.CharField()

class checkTokenserializer(serializers.Serializer):
    token = serializers.CharField()
class usersSerializer(serializers.Serializer):
    token = serializers.CharField()
    type = serializers.CharField()
class activateuserSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_id = serializers.CharField()

class loginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class chRoleeuserSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_id = serializers.CharField()
    role = serializers.CharField(required=False)
    url=serializers.CharField(required=False)
    url_type = serializers.CharField(required=False)

class RoleUrlSerializer(serializers.Serializer):
    role=serializers.CharField(required=False)
    url=serializers.CharField(required=False)
    user_id=serializers.CharField(required=False)
    token=serializers.CharField()
class addurlSerializer(serializers.Serializer):
    url=serializers.CharField(required=False)
    url_type = serializers.CharField(required=False)
    token = serializers.CharField()
    url_id = serializers.CharField(required=False)

class usercheckSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)
