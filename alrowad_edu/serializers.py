from rest_framework import serializers
from django.http import JsonResponse
import re
class oneuserSerializer(serializers.Serializer):
    idd = serializers.CharField(required=False)