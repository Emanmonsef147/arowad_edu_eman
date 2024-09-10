from rest_framework import serializers
from .models import *
class YearSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    year = serializers.IntegerField(required=False)


class AcademicYearSemestersSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    semster_id = serializers.IntegerField(required=False)
    academic_year_id = serializers.IntegerField(required=False)


class SemesterSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    no_of_quarters = serializers.IntegerField(required=False)
    semester_name_lng1 = serializers.CharField(required=False)
    semester_name_lng2 = serializers.CharField(required=False)
    start_date = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)
    admission_on = serializers.IntegerField(required=False)
    is_default = serializers.IntegerField(required=False)
    edit_std_status = serializers.IntegerField(required=False)
    grade_edit = serializers.IntegerField(required=False)
    week_plan = serializers.IntegerField(required=False)
    ignore_weekly_pal_dates = serializers.IntegerField(required=False)
    allow_add_material_cover = serializers.IntegerField(required=False)
    job_applicant_on = serializers.IntegerField(required=False)
    allow_to_create_weekly_plan = serializers.IntegerField(required=False)
    allow_to_view_weekly_plan = serializers.IntegerField(required=False)

class AcademicYearsSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    token = serializers.CharField(required=False)
    year_id = serializers.IntegerField(required=False)
    # no_of_semesters=serializers.IntegerField(required=False)
    # semester_name = serializers.CharField(required=False)
    year_name_h = serializers.CharField(required=False)
    year_name_g = serializers.CharField(required=False)
    start_date = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)
    finance_year_name = serializers.CharField(required=False)
    finance_start_date = serializers.CharField(required=False)
    finance_end_date =serializers.CharField(required=False)
    number_of_weeks = serializers.IntegerField(required=False)
