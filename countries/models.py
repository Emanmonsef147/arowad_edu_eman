from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.



class Country(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    iso3 = models.CharField(max_length=255,blank=True, null=True)
    iso2 = models.CharField(max_length=255,blank=True, null=True)
    numeric_code = models.CharField(max_length=255,blank=True, null=True)
    phone_code = models.CharField(max_length=255,blank=True, null=True)
    capital = models.CharField(max_length=255,blank=True, null=True)
    currency = models.CharField(max_length=255,blank=True, null=True)
    currency_name = models.CharField(max_length=255,blank=True, null=True)
    currency_symbol = models.CharField(max_length=255,blank=True, null=True)
    tld = models.CharField(max_length=255,blank=True, null=True)
    native = models.CharField(max_length=255,blank=True, null=True)
    region = models.CharField(max_length=255,blank=True, null=True)
    subregion = models.CharField(max_length=255,blank=True, null=True)
    nationality = models.CharField(max_length=255,blank=True, null=True)
    latitude = models.CharField(max_length=255,blank=True, null=True)
    longitude = models.CharField(max_length=255,blank=True, null=True)
    emoji = models.CharField(max_length=255,blank=True, null=True)
    emojiU = models.CharField(max_length=255,blank=True, null=True)


    class Meta:
        # app_label helps django to recognize your db
        app_label = 'countries'


class State(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    country_id = models.ForeignKey(Country , on_delete=models.DO_NOTHING)
    country_code = models.CharField(max_length=255,blank=True, null=True)
    country_name = models.CharField(max_length=255,blank=True, null=True)
    state_code = models.CharField(max_length=255,blank=True, null=True)
    type = models.CharField(max_length=255,blank=True, null=True)
    latitude = models.CharField(max_length=255,blank=True, null=True)
    longitude = models.CharField(max_length=255,blank=True, null=True)


    class Meta:
        # app_label helps django to recognize your db
        app_label = 'countries'


class Cities(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)
    state_id = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    state_code = models.CharField(max_length=255,blank=True, null=True)
    state_name = models.CharField(max_length=255,blank=True, null=True)
    country_id = models.ForeignKey(Country , on_delete=models.DO_NOTHING)
    country_code = models.CharField(max_length=255,blank=True, null=True)
    country_name = models.CharField(max_length=255,blank=True, null=True)
    latitude = models.CharField(max_length=255,blank=True, null=True)
    longitude = models.CharField(max_length=255,blank=True, null=True)
    wikiDataId = models.CharField(max_length=255,blank=True, null=True)


    class Meta:
        # app_label helps django to recognize your db
        app_label = 'countries'

class Langs(models.Model):
        lang_name = models.CharField(max_length=255, unique=True, db_index=True)
        lang_code = models.CharField(max_length=7, db_index=True, unique=True)
        rtl = models.BooleanField(default=False)
        flag_code = models.CharField(max_length=10, default="us")
        notes = models.TextField(null=True, blank=True)
        active = models.IntegerField(default=1)
        status = models.IntegerField(default=0)
        ip_address = models.CharField(max_length=255)


        class Meta:
            # app_label helps django to recognize your db
            app_label = 'countries'

class RELIGION(models.Model):
        name = models.CharField(max_length=255, blank=True,null=True)
        notes = models.TextField(null=True, blank=True)
        active = models.IntegerField(default=1)
        ip_address = models.CharField(max_length=255)

        class Meta:
            # app_label helps django to recognize your db
            app_label = 'countries'


