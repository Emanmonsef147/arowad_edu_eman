from rest_framework import serializers
from .models import *
from datetime import datetime

class StatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    category = serializers.CharField(required=False)
class ApplicantSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    iqama_id = serializers.CharField(required=False)
    date_of_birth = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    nationality_id = serializers.IntegerField(required=False)
    acadmic_year_id = serializers.IntegerField(required=False)
    reg_grade_id = serializers.CharField(required=False)
    programme_id = serializers.CharField(required=False)

    first_name = serializers.CharField(required=False)
    second_name = serializers.CharField(required=False)
    third_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    first_name_ar = serializers.CharField(required=False)
    second_name_ar = serializers.CharField(required=False)
    third_name_ar = serializers.CharField(required=False)
    last_name_ar = serializers.CharField(required=False)

    address_line = serializers.CharField(required=False)
    phone1 = serializers.CharField(required=False)
    phone2 = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

    religion_id= serializers.CharField(required=False)
    language_id = serializers.CharField(required=False)

    iqama_source = serializers.CharField(required=False)
    iqama_source_date = serializers.CharField(required=False)
    parent_iqama_id = serializers.CharField(required=False)
    parent_iqama_source = serializers.CharField(required=False)
    parent_iqama_source_date = serializers.CharField(required=False)
    passport_id = serializers.CharField(required=False)
    passport_expiry_date = serializers.CharField(required=False)
    passport_country = serializers.IntegerField(required=False)
    city_id =serializers.IntegerField(required=False)
    state_id = serializers.IntegerField(required=False)
    country_id = serializers.IntegerField(required=False)
    birth_country = serializers.IntegerField(required=False)
    applicant_no = serializers.CharField(required=False)
    status_id = serializers.CharField(required=False)
    has_paid = serializers.IntegerField(required=False)
    print_token = serializers.CharField(required=False)
    amount = serializers.FloatField(required=False)
    have_siblling = serializers.IntegerField(required=False)
    employee_id_name = serializers.CharField(required=False)
    # sibling_id = serializers.IntegerField(required=False)
    # student_id = serializers.IntegerField(required=False)
    # employee_id = serializers.IntegerField(required=False)
    # parent_id = serializers.IntegerField(required=False)



    # semster_id = serializers.IntegerField(required=False)

    # applicant_previous_school_data
    last_attended_school =serializers.CharField(required=False,allow_blank=True)
    last_attended_school_ar = serializers.CharField(required=False,allow_blank=True)
    last_score = serializers.CharField(required=False,allow_blank=True)
    evaluvation = serializers.CharField(required=False,allow_blank=True)
    last_grade_id = serializers.IntegerField(required=False,allow_null=True)
    last_year_id = serializers.IntegerField(required=False,allow_null=True)
    last_country_id = serializers.IntegerField(required=False,allow_null=True)

   # Applicant Gurdian Data
    first_name_gur = serializers.CharField(required=False)
    second_name_gur = serializers.CharField(required=False)
    third_name_gur = serializers.CharField(required=False)
    last_name_gur = serializers.CharField(required=False)
    first_name_gur_ar = serializers.CharField(required=False)
    second_name_gur_ar = serializers.CharField(required=False)
    third_name_gur_ar = serializers.CharField(required=False)
    last_name_gur_ar = serializers.CharField(required=False)
    iqama_id_gur = serializers.CharField(required=False)
    iqama_source_gur = serializers.CharField(required=False)
    iqama_source_date_gur = serializers.CharField(required=False)
    passport_id_gur = serializers.CharField(required=False)
    passport_expiry_date_gur = serializers.CharField(required=False)
    passport_country_gur = serializers.IntegerField(required=False)
    relation_gur = serializers.CharField(required=False)
    religion_id_gur = serializers.CharField(required=False)
    language_id_gur = serializers.CharField(required=False)
    date_of_birth_gur = serializers.CharField(required=False)
    education = serializers.CharField(required=False)
    job = serializers.CharField(required=False)
    company = serializers.CharField(required=False)
    address_line_gur = serializers.CharField(required=False)

    email_gur = serializers.CharField(required=False)
    nationality_id_gur = serializers.IntegerField(required=False)
    country_id_gur = serializers.IntegerField(required=False)
    state_id_gur =serializers.IntegerField(required=False)
    city_id_gur = serializers.IntegerField(required=False)
    mobile_phone = serializers.CharField(required=False)
    mother_phone = serializers.CharField(required=False)
    emergency_phone = serializers.CharField(required=False)

    start_date = serializers.CharField(required=False, default='',allow_blank=True)
    end_date = serializers.CharField(required=False ,default='',allow_blank=True)


class ApplicantDocumentTypeSerializer(serializers.Serializer):
    # Applicant Document Type
    doc_name_lng1 = serializers.CharField(required=False)
    doc_name_lng2 = serializers.CharField(required=False)
    doc_desc_lng1 = serializers.CharField(required=False)
    doc_desc_lng2 = serializers.CharField(required=False)
    is_necessary = serializers.IntegerField(required=False)
    doc_type = serializers.CharField(required=False)
    notes = serializers.CharField(required=False)
    # school_id =serializers.IntegerField(required=False)


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(required=False)