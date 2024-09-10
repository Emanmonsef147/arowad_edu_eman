from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *
# from seo.general_seo.models import Title,Meta,General_setting,Urls
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_countries(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # country_serializer = CountrySerializer(data=request.data)
    # if country_serializer.is_valid():
    countries = Country.objects.all().values('name',country_id =F('id'))
    return JsonResponse({"success": {'countries':list(countries)}})
    # else:
    #     return JsonResponse({"error": country_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_states(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    state_serializer = StateSerializer(data=request.data)
    if state_serializer.is_valid():
        country_id  = state_serializer.data['country_id']
        states = State.objects.filter(country_id=country_id).values('name','id')

        return JsonResponse({"success": {'states':list(states)}})
    else:
        return JsonResponse({"error": state_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_cities(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    city_serializer = CitiesSerializer(data=request.data)
    if city_serializer.is_valid():
        state_id = city_serializer.data['state_id']
        cities = Cities.objects.filter(state_id=state_id).values('name','id')
        return JsonResponse({"success": {'countries':list(cities)}})
    else:
        return JsonResponse({"error": city_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_langs(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # langs_serializer = LangsSerializer(data=request.data)
    # if langs_serializer.is_valid():
    langs = Langs.objects.all().values('lang_name','lang_code',lang_id =F('id'))
    return JsonResponse({"success": {'languages':list(langs)}})
    # else:
    #     return JsonResponse({"error": langs_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_religion(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # religion_serializer = ReligionSerializer(data=request.data)
    # if religion_serializer.is_valid():
    religions = RELIGION.objects.all().values('name',religion_id =F('id'))
    return JsonResponse({"success": {'religions':list(religions)}})
    # else:
    #     return JsonResponse({"error": religion_serializer.errors})