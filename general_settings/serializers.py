from rest_framework import serializers
from .models import *
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
class StageSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    name_lng1 = serializers.CharField(required=False)
    name_lng2 = serializers.CharField(required=False)

class GradeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    grade_name_lng1 =  serializers.CharField(required=False)
    grade_name_lng2 = serializers.CharField(required=False)
    code =  serializers.CharField(required=False)
    section_name = serializers.CharField(required=False)
    grading_type_id = serializers.IntegerField(required=False)
    grade_order = serializers.IntegerField(required=False)
    stage_id = serializers.IntegerField(required=False)
    current_grade_id = serializers.IntegerField(required=False)

    name = serializers.CharField(required=False)
    grade_id = serializers.IntegerField(required=False)
    # gender = serializers.CharField(required=False)
    acadmic_year_id = serializers.IntegerField(required=False)
    programme_id = serializers.IntegerField(required=False)

class IntialClassSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    grade_id = serializers.IntegerField(required=False)
    acadmic_year_id = serializers.IntegerField(required=False)
    programme_id = serializers.IntegerField(required=False)
class RegisterationGradeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    grade_id = serializers.IntegerField(required=False)
    minimum_score = serializers.IntegerField(required=False)
    is_active = serializers.IntegerField(required=False)
    amount = serializers.IntegerField(required=False)
    # subject_based_fee_collection =serializers.IntegerField(required=False)
    enable_approval_system = serializers.IntegerField(required=False)
    # min_electives = serializers.IntegerField(required=False)
    # max_elective = serializers.IntegerField(required=False)
    # is_subject_based_registration = serializers.IntegerField(required=False)
    # include_additional_details = serializers.IntegerField(required=False)
    # additional_field_ids =  serializers.CharField(required=False)
    age_limit_g =  serializers.CharField(required=False)
    age_limit_h =  serializers.CharField(required=False)


class ProgrammeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    programme_name_lng1 = serializers.CharField(required=False)
    programme_name_lng2 = serializers.CharField(required=False)

class GradeProgrammeSerializer(serializers.Serializer):
    reg_grade_ids = serializers.ListField(required=False)
    programme_id = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False)
    is_active = serializers.IntegerField(required=False)
    grade_programme_name = serializers.CharField(required=False)
    reg_grade_id = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)


class NationalSettingSerializer(serializers.Serializer):
    is_numeric = serializers.IntegerField(required=False)
    national_length = serializers.CharField(required=False)

class GradeTypeSystemSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    grade_name =  serializers.CharField(required=False)
