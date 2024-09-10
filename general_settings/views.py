from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from hijri_converter import convert
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from academic.models import *

# from seo.general_seo.serializers import TitleSerializer,MetaSerializer,UrlsSerializer,GeneralSettingSerializer
# Create your views here.

# Create Year

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def add_year(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     year_serializer = YearSerializer(data=request.data)
#     if year_serializer.is_valid():
#         # token = year_serializer.data['token']
#         year = year_serializer.data['year']
#
#         if not str(year).isdigit() or len(str(year)) != 4:
#             return JsonResponse({"error":"please_enter_valid_year"})
#
#         current_year = datetime.now().year
#
#         if year < current_year:
#             return JsonResponse({"error": "invalid_year"})
#
#         if Year.objects.filter(year=year).count() > 0:
#             return JsonResponse({"error": "year_exists"})
#
#         new_year = Year.objects.create(
#             year=year
#         )
#         new_year.save()
#         return JsonResponse({"success": "year_addeed_successfully"})
#
#     else:
#         return JsonResponse({"error": year_serializer.errors})
#
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def update_year(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     year_serializer = YearSerializer(data=request.data)
#     if year_serializer.is_valid():
#         id = year_serializer.data['id']
#         year = year_serializer.data['year']
#
#         # token = year_serializer.data["token"]
#
#         if Year.objects.filter(id=id).count() < 1:
#             return JsonResponse({"error": 'year_not_found'})
#
#         old_year = Year.objects.get(id=id).year
#         if old_year != year:
#             if Year.objects.filter(year=year).count() > 0:
#                 return JsonResponse({"error": "year_exists"})
#             else:
#
#                 year_obj = Year.objects.get(id=id)
#                 year_obj.year = year
#                 year_obj.save()
#         return JsonResponse({"success": "year_updated_successfully"})
#     else:
#         return JsonResponse({"error": year_serializer.errors})
#
#
# # Delete year
#
# # @api_view(['POST'])
# # @permission_classes([AllowAny])
# # @csrf_exempt
# # def delete_year(request):
# #     authentication_classes = (TokenAuthentication, SessionAuthentication)
# #     permission_classes = (IsAuthenticated,)
# #     year_serializer = YearSerializer(data=request.data)
# #     if year_serializer.is_valid():
# #         id = year_serializer.data['id']
# #         if Year.objects.filter(id=id).count() < 1:
# #             return JsonResponse({"error": "year_not_found"})
# #         year = Year.objects.get(id=id)
# #         year.delete()
# #         return JsonResponse({"success": "year_deleted_successfully"})
# #     else:
# #         return JsonResponse({"error": year_serializer.errors})
#
#
# # View All Years
#
#
#
# def view_all_years(request):
#     year_serliazer = YearSerializer(data=request.data)
#     if year_serliazer.is_valid():
#         years = Year.objects.all().order_by('id').values('id', 'year')
#         return JsonResponse({'success': list(years)})
#     else:
#         return JsonResponse({'error': year_serliazer.errors})
#
#
# # View One Year
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def view_one_year(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     year_serializer = YearSerializer(data=request.data)
#     if year_serializer.is_valid():
#         id = year_serializer.data['id']
#         if Year.objects.filter(id=id).count() < 1:
#             return JsonResponse({"error": 'year_not_found'})
#
#         year_obj = Year.objects.get(id=id)
#
#         return JsonResponse({'success': {
#             'id': year_obj.id,
#             'year': year_obj.year}})
#     else:
#         return JsonResponse({'error': year_serializer.errors})
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def add_semster(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     semster_serializer = AcademicYearSemestersSerializer(data=request.data)
#     if semster_serializer.is_valid():
#         # token = year_serializer.data['token']
#         year_id = semster_serializer.data['year_id']
#         no_of_semesters = semster_serializer.data['no_of_semesters']
#         no_of_quarters_each_sem = semster_serializer.data['no_of_quarters_each_sem']
#
#         if Year.objects.filter(id=year_id).count()<1:
#             return JsonResponse({"error": "year_not_exist"})
#
#
#         if Academic_Year_Semesters.objects.filter(year_id=year_id,no_of_semesters=no_of_semesters,no_of_quarters_each_sem=no_of_quarters_each_sem).count() > 0:
#                 return JsonResponse({"error": "this_year_already_added_semster"})
#
#
#         semster = Academic_Year_Semesters.objects.create(
#                     year_id_id=year_id,
#                     no_of_semesters=no_of_semesters,
#                     no_of_quarters_each_sem=no_of_quarters_each_sem
#         )
#         semster.save()
#         return JsonResponse({"success": "semster_addeed_successfully"})
#
#     else:
#         return JsonResponse({"error": semster_serializer.errors})
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def update_semster(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     semster_serializer = AcademicYearSemestersSerializer(data=request.data)
#     if semster_serializer.is_valid():
#         id = semster_serializer.data['id']
#         no_of_semesters = semster_serializer.data['no_of_semesters']
#         no_of_quarters_each_sem = semster_serializer.data['no_of_quarters_each_sem']
#
#         # token = year_serializer.data["token"]
#         if Academic_Year_Semesters.objects.filter(id=id).count()<1:
#             return JsonResponse({"error": 'semester_not_found'})
#         old_sem = Academic_Year_Semesters.objects.get(id=id).no_of_semesters
#         old_qua = Academic_Year_Semesters.objects.get(id=id).no_of_quarters_each_sem
#         if no_of_semesters < old_sem or no_of_quarters_each_sem < old_qua:
#             return JsonResponse({"error":"failed_updated_no_of_semstets"})
#         else:
#             semester = Academic_Year_Semesters.objects.get(id=id)  # Update the semester details
#             semester.no_of_semesters = no_of_semesters
#             semester.no_of_quarters_each_sem = no_of_quarters_each_sem
#
#             semester.save()
#             return JsonResponse({"success": "semester_updated_successfully"})
#     else:
#         return JsonResponse({"error": semster_serializer.errors})
#
#
# def view_all_semsters(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     semster_serializer = AcademicYearSemestersSerializer(data=request.data)
#     if semster_serializer.is_valid():
#         semsters = Academic_Year_Semesters.objects.all().order_by('id').values('id','no_of_semesters','no_of_quarters_each_sem',year_name = F('year_id__year'))
#         return JsonResponse({'success': list(semsters)})
#     else:
#         return JsonResponse({'error': semster_serializer.errors})
#
#
# # View One Semester
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def view_one_semster(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     semster_serializer = AcademicYearSemestersSerializer(data=request.data)
#     if semster_serializer.is_valid():
#         id = semster_serializer.data['id']
#         if Academic_Year_Semesters.objects.filter(id=id).count() < 1:
#             return JsonResponse({"error": 'semster_not_found'})
#
#         semster = Academic_Year_Semesters.objects.get(id=id)
#
#         return JsonResponse({'success': {
#             'id': semster.id,
#             'year_id': semster.year_id_id,
#         'no_of_semesters':semster.no_of_semesters,
#         'no_of_quarters_each_sem':semster.no_of_quarters_each_sem}})
#     else:
#         return JsonResponse({'error': semster_serializer.errors})
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def view_years_by_semsters(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     if acadmic_year_serializer.is_valid():
#         year_semsters = Academic_Year_Semesters.objects.select_related('year').values('no_of_semesters', 'year_id',year_name=F('year_id__year'),semester_id =F('id'))
#         return JsonResponse({"success": list(year_semsters)})
#     else:
#         return JsonResponse({"error": acadmic_year_serializer.errors})
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def add_acadmic_year(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     if acadmic_year_serializer.is_valid():
#         # token = year_serializer.data['token']
#         year_id = acadmic_year_serializer.data['year_id']
#         no_of_semesters = acadmic_year_serializer.data['no_of_semesters']
#         # year_name = acadmic_year_serializer.data['year_name']
#         # # year_name_ar = acadmic_year_serializer.data['year_name_ar']
#         # # # finance_year_name = acadmic_year_serializer.data['finance_year_name']
#         semester_name = acadmic_year_serializer.data['semester_name']
#         start_date = acadmic_year_serializer.data['start_date']
#         end_date = acadmic_year_serializer.data['end_date']
#         # finance_start_date = acadmic_year_serializer.data['finance_start_date']
#         # finance_end_date = acadmic_year_serializer.data['finance_end_date']
#         number_of_weeks = acadmic_year_serializer.data['number_of_weeks']
#         admission_on =acadmic_year_serializer.data['admission_on']
#         is_default = acadmic_year_serializer.data['is_default']
#         edit_std_status = acadmic_year_serializer.data['edit_std_status']
#         grade_edit = acadmic_year_serializer.data['grade_edit']
#         week_plan = acadmic_year_serializer.data['week_plan']
#         ignore_weekly_pal_dates = acadmic_year_serializer.data['ignore_weekly_pal_dates']
#         allow_add_material_cover = acadmic_year_serializer.data['allow_add_material_cover']
#         job_applicant_on = acadmic_year_serializer.data['job_applicant_on']
#         allow_to_create_weekly_plan = acadmic_year_serializer.data['allow_to_create_weekly_plan']
#         allow_to_view_weekly_plan = acadmic_year_serializer.data['allow_to_view_weekly_plan']
#
#         if Academic_Years.objects.filter(year_id=year_id,no_of_semester=no_of_semesters).count() > 0:
#             return JsonResponse({"error":"this_year_already_added"})
#
#         if int(allow_to_create_weekly_plan) not in range(1, 61) or int(allow_to_view_weekly_plan) not in range(1, 61):
#             return JsonResponse({"error":"this_out_range"})
#
#         year_obj = Year.objects.get(id=year_id).year
#         next_year = int(year_obj) + 1
#         year_name_g= f"{year_obj}/{next_year}"
#
#
#         hijri = convert.Gregorian(int(year_obj), 1, 1).to_hijri()
#         hijri_year = hijri.year
#         hijri_year_next = int(hijri_year) + 1
#         # print(hijri_year)
#         year_name_h = f"{hijri_year}/{hijri_year_next}"
#         # print(year_name_h)
#
#         acadmic_year = Academic_Years.objects.create(
#             year_id_id=year_id,
#             no_of_semester=no_of_semesters,
#             semester_name=semester_name,
#             year_name_h =year_name_h,
#             year_name_g = year_name_g,
#             start_date =start_date,
#             end_date=end_date,
#             # finance_year_name=year_name_g,
#             # finance_start_date =finance_start_date,
#             # finance_end_date =finance_end_date,
#             number_of_weeks =number_of_weeks,
#         admission_on= admission_on,
#         is_default = is_default,
#         edit_std_status = edit_std_status,
#         grade_edit = grade_edit,
#         week_plan = week_plan,
#         ignore_weekly_pal_dates = ignore_weekly_pal_dates,
#         allow_add_material_cover = allow_add_material_cover,
#         job_applicant_on = job_applicant_on,
#         allow_to_create_weekly_plan = allow_to_create_weekly_plan,
#         allow_to_view_weekly_plan = allow_to_view_weekly_plan
#         )
#         acadmic_year.save()
#         return JsonResponse({"success":"acadmic_year_add_successfully"})
#     else:
#         return JsonResponse({"error": acadmic_year_serializer.errors})
#
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def view_acadmic_years(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     if acadmic_year_serializer.is_valid():
#         acadmic_years = Academic_Years.objects.select_related('year').values('semester_name','year_name_g','admission_on','is_default','edit_std_status','grade_edit',year_name=F('year_id__year'))
#         return JsonResponse({"success": list(acadmic_years)})
#     else:
#         return JsonResponse({"error": acadmic_year_serializer.errors})
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def view_acadmic_years_is_acceptedopen(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     if acadmic_year_serializer.is_valid():
#         acadmic_years = Academic_Years.objects.filter(admission_on=1).values('year_name_g', 'semester_name','semester_id', acadmic_year_id=F('id'))
#         return JsonResponse({"success": list(acadmic_years)})
#     else:
#         return JsonResponse({"error": acadmic_year_serializer.errors})
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def view_one_acadmic_year(request , id ):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     if Academic_Years.objects.filter(id=id).count() < 1:
#         return JsonResponse({"error": "not_found"})
#
#     acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     if acadmic_year_serializer.is_valid():
#         # id = acadmic_year_serializer.data['id']
#         # if Academic_Years.objects.filter(id=id).count() < 1:
#         #     return JsonResponse({"error": 'acadmic_year_not_found'})
#
#         acadmic_year = Academic_Years.objects.get(id=id)
#
#         return JsonResponse({'success': {
#             'id': acadmic_year.id,
#             'year': Year.objects.get(id=acadmic_year.year_id_id).year,
#             'semester': acadmic_year.no_of_semester,
#             'semester_name': acadmic_year.semester_name,
#             'year_name_h':acadmic_year.year_name_h,
#         'year_name_g':acadmic_year.year_name_g,
#         'start_date':acadmic_year.start_date,
#         'end_date':acadmic_year.end_date,
#         # 'finance_year_name': acadmic_year.finance_year_name,
#         # 'finance_start_date':acadmic_year.finance_start_date,
#         # 'finance_end_date': acadmic_year.finance_end_date,
#         'number_of_weeks': acadmic_year.number_of_weeks,
#         'admission_on':acadmic_year.admission_on,
#         'is_default':acadmic_year.is_default,
#         'edit_std_status' :acadmic_year.edit_std_status,
#         'grade_edit':acadmic_year.grade_edit,
#         'week_plan':acadmic_year.week_plan,
#         'ignore_weekly_pal_dates' :acadmic_year.ignore_weekly_pal_dates,
#         'allow_add_material_cover':acadmic_year.allow_add_material_cover,
#         'job_applicant_on' :acadmic_year.job_applicant_on,
#         'allow_to_create_weekly_plan' :acadmic_year.allow_to_create_weekly_plan,
#         'allow_to_view_weekly_plan' :acadmic_year.allow_to_view_weekly_plan
#         }})
#     else:
#         return JsonResponse({'error': acadmic_year_serializer.errors})
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def update_acadmic_year(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     if acadmic_year_serializer.is_valid():
#         id = acadmic_year_serializer.data['id']
#         year_id = acadmic_year_serializer.data['year_id']
#         no_of_semesters = acadmic_year_serializer.data['no_of_semesters']
#         # year_name = acadmic_year_serializer.data['year_name']
#         # # year_name_ar = acadmic_year_serializer.data['year_name_ar']
#         # # # finance_year_name = acadmic_year_serializer.data['finance_year_name']
#         semester_name = acadmic_year_serializer.data['semester_name']
#         start_date = acadmic_year_serializer.data['start_date']
#         end_date = acadmic_year_serializer.data['end_date']
#         # finance_start_date = acadmic_year_serializer.data['finance_start_date']
#         # finance_end_date = acadmic_year_serializer.data['finance_end_date']
#         number_of_weeks = acadmic_year_serializer.data['number_of_weeks']
#         admission_on = acadmic_year_serializer.data['admission_on']
#         is_default = acadmic_year_serializer.data['is_default']
#         edit_std_status = acadmic_year_serializer.data['edit_std_status']
#         grade_edit = acadmic_year_serializer.data['grade_edit']
#         week_plan = acadmic_year_serializer.data['week_plan']
#         ignore_weekly_pal_dates = acadmic_year_serializer.data['ignore_weekly_pal_dates']
#         allow_add_material_cover = acadmic_year_serializer.data['allow_add_material_cover']
#         job_applicant_on = acadmic_year_serializer.data['job_applicant_on']
#         allow_to_create_weekly_plan = acadmic_year_serializer.data['allow_to_create_weekly_plan']
#         allow_to_view_weekly_plan = acadmic_year_serializer.data['allow_to_view_weekly_plan']
#
#         # token = year_serializer.data["token"]
#         if Academic_Years.objects.filter(id=id).count()<1:
#             return JsonResponse({"error": 'acadmic_year_not_found'})
#
#         year_obj = Year.objects.get(id=year_id).year
#         # print(year_obj)
#
#         next_year = int(year_obj) + 1
#         year_name_g = f"{year_obj}/{next_year}"
#         # print(year_name_g)
#
#         hijri = convert.Gregorian(int(year_obj), 1, 1).to_hijri()
#         hijri_year = hijri.year
#         hijri_year_next = int(hijri_year) + 1
#         # print(hijri_year)
#         year_name_h = f"{hijri_year}/{hijri_year_next}"
#         acadmic_year = Academic_Years.objects.get(id=id)
#         # Update the semester details
#         acadmic_year.year_id_id =year_id
#         acadmic_year.no_of_semester=no_of_semesters
#         acadmic_year.semester_name=semester_name
#         acadmic_year.year_name_h=year_name_h
#         acadmic_year.year_name_g=year_name_g
#         acadmic_year.start_date=start_date
#         acadmic_year.end_date=end_date
#         # acadmic_year.finance_year_name=year_name_g
#         # acadmic_year.finance_start_date=finance_start_date
#         # acadmic_year.finance_end_date=finance_end_date
#         acadmic_year.number_of_weeks=number_of_weeks
#         acadmic_year.admission_on=admission_on
#         acadmic_year.is_default=is_default
#         acadmic_year.week_plan=week_plan
#         acadmic_year.edit_std_status=edit_std_status
#         acadmic_year.grade_edit=grade_edit
#         acadmic_year.ignore_weekly_pal_dates=ignore_weekly_pal_dates
#         acadmic_year.allow_add_material_cover=allow_add_material_cover
#         acadmic_year.allow_to_view_weekly_plan=allow_to_view_weekly_plan
#         acadmic_year.allow_to_create_weekly_plan=allow_to_create_weekly_plan
#         acadmic_year.job_applicant_on=job_applicant_on
#
#         acadmic_year.save()
#         return JsonResponse({"success": "acadmic_year_updated_successfully"})
#     else:
#         return JsonResponse({"error": acadmic_year_serializer.errors})
# Add Stage
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_stage(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    stage_serializer = StageSerializer(data=request.data)
    if stage_serializer.is_valid():
        # token = year_serializer.data['token']
        name_lng1 = stage_serializer.data['name_lng1']
        name_lng2 = stage_serializer.data['name_lng2']

        if Stage.objects.filter(name_lng1=name_lng1).count() > 0:
            return JsonResponse({"error": "stage_exists"})


        stage = Stage.objects.create(
            name_lng1=name_lng1,
            name_lng2=name_lng2
        )
        stage.save()
        return JsonResponse({"success": "stage_added_successfully"})

    else:
        return JsonResponse({"error": stage_serializer.errors})


#Update Stage
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def update_stage(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    stage_serializer = StageSerializer(data=request.data)
    if stage_serializer.is_valid():
        id = stage_serializer.data['id']
        name_lng1 = stage_serializer.data['name_lng1']
        name_lng2 = stage_serializer.data['name_lng2']

        # token = year_serializer.data["token"]
        old_name_lng1 = None  # Initialize these variables
        old_name_lng2 = None
        if Stage.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'stage_not_found'})

        old_name_lng1 = Stage.objects.get(id=id).name_lng1
        old_name_lng2 = Stage.objects.get(id=id).name_lng2

        if old_name_lng1 != name_lng1 and old_name_lng2 != name_lng2:
            if Stage.objects.filter(name_lng1=name_lng1, name_lng2=name_lng2).exclude(id=id).count() > 0:
                return JsonResponse({"error": "name_lng_stage_exists"})
            else:
                stage_obj = Stage.objects.get(id=id)
                stage_obj.name_lng1 = name_lng1
                stage_obj.name_lng2 = name_lng2
                stage_obj.save()
                return JsonResponse({"success": "stage_updated_successfully"})
        else:
            stage_obj = Stage.objects.get(id=id)
            stage_obj.name_lng1 = name_lng1
            stage_obj.name_lng2 = name_lng2
            stage_obj.save()
            return JsonResponse({"success": "stage_updated_successfully"})
    else:
        return JsonResponse({"error": stage_serializer.errors})


# Delete Stage

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def delete_stage(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    stage_serializer = StageSerializer(data=request.data)
    if stage_serializer.is_valid():
        id = stage_serializer.data['id']
        if Stage.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": "stage_not_found"})
        stage = Stage.objects.get(id=id)
        stage.delete()
        return JsonResponse({"success": "stage_deleted_successfully"})
    else:
        return JsonResponse({"error": stage_serializer.errors})


# View All Stages

@api_view(['POST'])
@permission_classes([AllowAny])
def view_all_satges(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    stages = Stage.objects.all().order_by('id').values('id', 'name_lng1','name_lng2')
    return JsonResponse({'success': list(stages)})



# View One Stage

@api_view(['POST'])
@permission_classes([AllowAny])
def view_one_stage(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    stage_serializer = StageSerializer(data=request.data)
    if stage_serializer.is_valid():
        id = stage_serializer.data['id']
        if Stage.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'stage_not_found'})

        stage_obj = Stage.objects.get(id=id)

        return JsonResponse({'success': {
            'id': stage_obj.id,
            'name_lng1': stage_obj.name_lng1,
        'name_lng2':stage_obj.name_lng2}})
    else:
        return JsonResponse({'error': stage_serializer.errors})



# Add Grade
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_grade(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_serializer = GradeSerializer(data=request.data)
    if grade_serializer.is_valid():
        # token = year_serializer.data['token']
        grade_name_lng1 = grade_serializer.data['grade_name_lng1']
        grade_name_lng2 = grade_serializer.data['grade_name_lng2']
        code = grade_serializer.data['code']
        grading_type_id = grade_serializer.data['grading_type_id']
        grade_order = grade_serializer.data['grade_order']
        stage_id = grade_serializer.data['stage_id']

        name = grade_serializer.data['name']
        # grade_id = grade_serializer.data['grade_id']
        # gender = grade_serializer.data['gender']
        acadmic_year_id = grade_serializer.data['acadmic_year_id']
        programme_id = grade_serializer.data['programme_id']

        # if Stu_Intial_Class.objects.filter(gender=gender,programme_id=programme_id).count() > 0:
        #     return JsonResponse({"error": "this_class_already_exists"})
        filter_condition = Q(grade_name_lng1=grade_name_lng1) | Q(grade_order=grade_order) | Q(grade_name_lng2=grade_name_lng2)
        if Grade.objects.filter(filter_condition).count() > 0:
            return JsonResponse({"error": "grade_exist"})
        if int(grade_order) not in range(1, 21):
            return JsonResponse({"error":"this_out_range"})
        if Stu_Intial_Class.objects.filter(name=name).count()>0:
            return  JsonResponse({"error":"this_name_exist"})
        add_aplc = True
        while add_aplc == True:
            try:
                with transaction.atomic():
                    grade = Grade.objects.create(
                                    grade_name_lng1=grade_name_lng1,
                                    grade_name_lng2=grade_name_lng2,
                                    code=code,
                                    grading_type_id_id=grading_type_id,
                                    grade_order=grade_order,
                                    stage_id_id=stage_id
                                )
                    intial_class = Stu_Intial_Class.objects.create(
                        grade_id=grade,
                        name=name,
                        acadmic_year_id_id = acadmic_year_id,
                        programme_id_id = programme_id)
                add_aplc = False
            except Exception as e:
                 add_aplc = True
                 return JsonResponse({'error': str(e)})
        return JsonResponse({"success": "grade_addeed_successfully"})

    else:
        return JsonResponse({"error": grade_serializer.errors})


#Update Grade
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def update_grade(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_serializer = GradeSerializer(data=request.data)
    if grade_serializer.is_valid():
        id = grade_serializer.data['id']
        grade_name_lng1 = grade_serializer.data['grade_name_lng1']
        grade_name_lng2 = grade_serializer.data['grade_name_lng2']
        code = grade_serializer.data['code']
        grading_type_id = grade_serializer.data['grading_type_id']
        grade_order = grade_serializer.data['grade_order']

        stage_id = grade_serializer.data['stage_id']

        old_grade_name_lng1 = None
        old_grade_name_lng2 = None

        if Grade.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'grade_not_found'})

        old_grade_name_lng1 = Grade.objects.get(id=id).grade_name_lng1
        old_grade_name_lng2 = Grade.objects.get(id=id).grade_name_lng2
        old_grade_order = Grade.objects.get(id=id).grade_order

        if old_grade_name_lng1 != grade_name_lng1 or old_grade_name_lng2 != grade_name_lng2 or old_grade_order != grade_order :
            filter_condition = Q(grade_name_lng1=grade_name_lng1) | Q(grade_name_lng2=grade_name_lng2) | Q(grade_order=grade_order)
            if Grade.objects.filter(filter_condition ).count() > 0:
                return JsonResponse({"error": "grade_exists"})
            else:
                grade_obj = Grade.objects.get(id=id)
                grade_obj.grade_name_lng1 = grade_name_lng1
                grade_obj.grade_name_lng2 = grade_name_lng2
                grade_obj.code = code
                grade_obj.grading_type_id_id = grading_type_id
                grade_obj.grade_order = grade_order
                grade_obj.stage_id_id = stage_id
                grade_obj.save()

                return JsonResponse({"success": "grade_updated_successfully"})
        else:

            grade_obj = Grade.objects.get(id=id)
            grade_obj.grade_name_lng1 = grade_name_lng1
            grade_obj.grade_name_lng2 = grade_name_lng2
            grade_obj.code = code
            grade_obj.grading_type_id_id = grading_type_id
            grade_obj.grade_order = grade_order
            grade_obj.stage_id_id = stage_id
            grade_obj.save()

            return JsonResponse({"success": "grade_updated_successfully"})
        #
        # if old_grade_name_lng2 != grade_name_lng2:
        #     if Grade.objects.filter(grade_name_lng2=grade_name_lng2).count() > 0:
        #         return JsonResponse({"error": "grade_name_lng2_stage_exists"})

        # Update the grade's attributes

    else:
        return JsonResponse({"error": grade_serializer.errors})


# Delete Grade

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def delete_grade(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_serializer = GradeSerializer(data=request.data)
    if grade_serializer.is_valid():
        id = grade_serializer.data['id']
        if Grade.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": "grade_not_found"})
        grade = Grade.objects.get(id=id)
        grade.delete()
        return JsonResponse({"success": "grade_deleted_successfully"})
    else:
        return JsonResponse({"error": grade_serializer.errors})



@api_view(['POST'])
@permission_classes([AllowAny])
def view_last_grades(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_serializer = GradeSerializer(data=request.data)
    if grade_serializer.is_valid():
        current_grade_id = grade_serializer.data['current_grade_id']
        grade_order = Grade.objects.get(id=current_grade_id).grade_order
        print(grade_order)
        grades = []
        if grade_order == 1 :
            return JsonResponse({'success': grades})
        else:
             grades = Grade.objects.all().filter(grade_order__lt=grade_order).values(grade_name =F('grade_name_lng1'),last_grade_id =F('id'))
             return JsonResponse({'success': list(grades)})
    else:
        return JsonResponse({'error': grade_serializer.errors})
# View All Grades

@api_view(['POST'])
@permission_classes([AllowAny])
def view_all_grades(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    grades = Grade.objects.all().order_by('id').values('id', 'grade_name_lng1','grade_name_lng2','code','grade_order')
    return JsonResponse({'success': list(grades)})



# View One Grade

@api_view(['POST'])
@permission_classes([AllowAny])
def view_one_grade(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_serializer = GradeSerializer(data=request.data)
    if grade_serializer.is_valid():
        id = grade_serializer.data['id']
        if Grade.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'grade_not_found'})

        grade_obj = Grade.objects.get(id=id)

        return JsonResponse({'success': {
            'id': grade_obj.id,
            'grade_name_lng1': grade_obj.grade_name_lng1,
        'grade_name_lng2':grade_obj.grade_name_lng2,
        'code':grade_obj.code,
            'grading_type_id':grade_obj.grading_type_id_id,
                # Grade_Type_System.objects.get(id = grade_obj.grading_type_id_id).grade_name,

            'grade_order':grade_obj.grade_order,
            'stage_id':grade_obj.stage_id_id,
                # Stage.objects.get(id=grade_obj.stage_id_id).name_lng1
        }})
    else:
        return JsonResponse({'error': grade_serializer.errors})
    

#Update Student Intial Class

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def update_intial_class(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    intial_class_serializer = IntialClassSerializer(data=request.data)
    if intial_class_serializer.is_valid():
        id = intial_class_serializer.data['id']
        name = intial_class_serializer.data['name']
        grade_id = intial_class_serializer.data['grade_id']
        acadmic_year_id = intial_class_serializer.data['acadmic_year_id']
        programme_id = intial_class_serializer.data['programme_id']


        old_name= None
        old_grade_id = None

        if Stu_Intial_Class.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'stu_intial_class_not_found'})

        old_name = Stu_Intial_Class.objects.get(id=id).name
        old_grade_id = Stu_Intial_Class.objects.get(id=id).grade_id_id


        if old_name != name or old_grade_id != grade_id:
            filter_condition = Q(name=name) | Q(grade_id_id=grade_id)
            if Stu_Intial_Class.objects.filter(filter_condition).count() > 0:
                return JsonResponse({"error": "intial_class_exists"})

            else:
                intial_class_obj = Stu_Intial_Class.objects.get(id=id)
                intial_class_obj.name = name
                intial_class_obj.grade_id_id = grade_id
                intial_class_obj.programme_id_id = programme_id
                intial_class_obj.acadmic_year_id_id = acadmic_year_id
                intial_class_obj.save()

                return JsonResponse({"success": "intial_class_updated_successfully"})
        else:

            intial_class_obj = Stu_Intial_Class.objects.get(id=id)
            intial_class_obj.name = name
            intial_class_obj.grade_id_id = grade_id
            intial_class_obj.programme_id_id = programme_id
            intial_class_obj.acadmic_year_id_id = acadmic_year_id
            intial_class_obj.save()

            return JsonResponse({"success": "intial_class_updated_successfully"})


    else:
        return JsonResponse({"error": intial_class_serializer.errors})


# View One Intial Class

@api_view(['POST'])
@permission_classes([AllowAny])
def view_one_intial_class(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    intial_class_serializer = IntialClassSerializer(data=request.data)
    if intial_class_serializer.is_valid():
        id = intial_class_serializer.data['id']
        if Stu_Intial_Class.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'intial_class_not_found'})

        intial_class_obj = Stu_Intial_Class.objects.get(id=id)

        return JsonResponse({'success': {
            'id': intial_class_obj.id,
            'name': intial_class_obj.name,
            'grade_id':intial_class_obj.grade_id_id,
                # Grade.objects.get(id = intial_class_obj.grade_id_id).grade_name_lng1,
            'programme_id':intial_class_obj.programme_id_id,
                # Programme.objects.get(id = intial_class_obj.programme_id_id).programme_name_lng1,
            'academic_year_id': intial_class_obj.acadmic_year_id_id
                # Academic_Years.objects.get(id = intial_class_obj.acadmic_year_id_id).year_name_g,

            }})
    else:
        return JsonResponse({'error': intial_class_serializer.errors})


# View All intial classes

@api_view(['POST'])
@permission_classes([AllowAny])
def view_all_intial_classes(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    intial_classes = Stu_Intial_Class.objects.select_related('grade').values('id', 'name',grade_name = F('grade_id__grade_name_lng1'))
    return JsonResponse({'success': list(intial_classes)})
# Add Registeration-Grade
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_register_grade(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    reg_grade_serializer = RegisterationGradeSerializer(data=request.data)
    if reg_grade_serializer.is_valid():
        # token = year_serializer.data['token']
        grade_id = reg_grade_serializer.data['grade_id']
        minimum_score = reg_grade_serializer.data['minimum_score']
        is_active = reg_grade_serializer.data['is_active']
        amount = reg_grade_serializer.data['amount']
        enable_approval_system =reg_grade_serializer.data['enable_approval_system']
        age_limit_g = reg_grade_serializer.data['age_limit_g']

        if Registration_Grade.objects.filter(grade_id=grade_id).count() > 0:
            return JsonResponse({"error": "register_grade_exists"})

        date_of_birth = str(age_limit_g)

        # Create a datetime object from the date string
        parsed_date = datetime.strptime(date_of_birth, '%Y-%m-%d')

        # Extract year, month, and day components
        year = parsed_date.year
        month = parsed_date.month
        day = parsed_date.day

        # Convert the extracted date components to the Hijri calendar
        hijri = convert.Gregorian(year, month, day).to_hijri()
        # print(hijri)

        reg_grade = Registration_Grade.objects.create(
           grade_id_id=grade_id,
            minimum_score=minimum_score,
            is_active=is_active,
            amount=amount,
            enable_approval_system=enable_approval_system,
            age_limit_g=str(age_limit_g),
            age_limit_h=str(hijri)

        )
        reg_grade.save()
        return JsonResponse({"success": "register_grade_addeed_successfully"})

    else:
        return JsonResponse({"error": reg_grade_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def toggle(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    reg_grade_serializer = RegisterationGradeSerializer(data=request.data)
    if reg_grade_serializer.is_valid():
        id = reg_grade_serializer.data['id']
        try:
            reg_grade_obj = Registration_Grade.objects.get(id=id)
            reg_grade_obj.is_active = not reg_grade_obj.is_active
            reg_grade_obj.save()
            return JsonResponse({"success": "Toggle successful for this grade"})

        except ObjectDoesNotExist:
            return JsonResponse({"error": 'Registration grade not found'})
    else :
        return JsonResponse({"error": reg_grade_serializer.errors})


#Update RegisterGrade
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def update_reg_grade(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    reg_grade_serializer = RegisterationGradeSerializer(data=request.data)
    if reg_grade_serializer.is_valid():
        id = reg_grade_serializer.data['id']
        minimum_score = reg_grade_serializer.data['minimum_score']
        is_active = reg_grade_serializer.data['is_active']
        amount = reg_grade_serializer.data['amount']
        enable_approval_system = reg_grade_serializer.data['enable_approval_system']
        age_limit_g = reg_grade_serializer.data['age_limit_g']


        if Registration_Grade.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'registeration_grade_not_found'})

        try:
            date_of_birth = str(age_limit_g)

            # Create a datetime object from the date string
            parsed_date = datetime.strptime(date_of_birth, '%Y-%m-%d')

            # Extract year, month, and day components
            year = parsed_date.year
            month = parsed_date.month
            day = parsed_date.day

            # Convert the extracted date components to the Hijri calendar
            hijri = convert.Gregorian(year, month, day).to_hijri()

            # Update the register grade's attributes
            reg_grade_obj = Registration_Grade.objects.get(id=id)
            reg_grade_obj.minimum_score = minimum_score
            reg_grade_obj.is_active = is_active
            reg_grade_obj.amount = amount
            reg_grade_obj.enable_approval_system = enable_approval_system
            reg_grade_obj.age_limit_g = str(age_limit_g)  # Assign the string representation
            reg_grade_obj.age_limit_h = str(hijri)
            reg_grade_obj.save()
            return JsonResponse({"success": "reg_grade_added_successfully"})

        except (ValueError, TypeError):
            # Handle the case where age_limit_g is not in the expected format
            return JsonResponse({"error": "Invalid date format or value in age_limit_g"})


    else:
        return JsonResponse({"error": reg_grade_serializer.errors})


#  View One RegisterGrade

@api_view(['POST'])
@permission_classes([AllowAny])
def view_one_reg_grade(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    reg_grade_serializer = RegisterationGradeSerializer(data=request.data)
    if reg_grade_serializer.is_valid():
        id = reg_grade_serializer.data['id']
        if Registration_Grade.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'registeration_grade_not_found'})

        reg_grade_obj = Registration_Grade.objects.get(id=id)

        return JsonResponse({'success': {
            'id': reg_grade_obj.id,
        'grade':reg_grade_obj.grade_id_id,
        'grade_name':reg_grade_obj.grade_id.grade_name_lng1,
        'minimum_score': reg_grade_obj.minimum_score,
        'is_active':reg_grade_obj.is_active,
        'amount':reg_grade_obj.amount,
       'enable_approval_system':reg_grade_obj.enable_approval_system ,
        'age_limit_g':reg_grade_obj.age_limit_g ,
        'age_limit_h':reg_grade_obj.age_limit_h}})
    else:
        return JsonResponse({'error': reg_grade_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_all_reg_grades(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # reg_grade_serializer = RegisterationGradeSerializer(data=request.data)
    # if reg_grade_serializer.is_valid():
    reg_grades = Registration_Grade.objects.select_related('grade').values('id','is_active', grade_name =F('grade_id__grade_name_lng1'),code =F('grade_id__code'))
    # print(reg_grades)
    return JsonResponse({"success": list(reg_grades)})
    # else:
    #     return JsonResponse({"error": reg_grade_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_programme(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    programme_serializer = ProgrammeSerializer(data=request.data)
    if programme_serializer.is_valid():
        # token = year_serializer.data['token']
        programme_name_lng1 = programme_serializer.data['programme_name_lng1']
        programme_name_lng2 = programme_serializer.data['programme_name_lng2']

        if Programme.objects.filter(programme_name_lng1=programme_name_lng1,programme_name_lng2=programme_name_lng2).count() > 0:
            return JsonResponse({"error": "programme_exists"})


        programme = Programme.objects.create(
            programme_name_lng1=programme_name_lng1,
            programme_name_lng2=programme_name_lng2
        )
        programme.save()
        return JsonResponse({"success": "programme_added_successfully"})

    else:
        return JsonResponse({"error": programme_serializer.errors})

# Update Programme
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def update_programme(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    programme_serializer = ProgrammeSerializer(data=request.data)
    if programme_serializer.is_valid():
        id = programme_serializer.data['id']
        programme_name_lng1 = programme_serializer.data['programme_name_lng1']
        programme_name_lng2 = programme_serializer.data['programme_name_lng2']


        old_programme_name_lng1 = None
        old_programme_name_lng2 = None
        if Programme.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'programme_not_found'})

        old_programme_name_lng1 = Programme.objects.get(id=id).programme_name_lng1
        old_programme_name_lng2 = Programme.objects.get(id=id).programme_name_lng2

        if old_programme_name_lng1 != programme_name_lng1 or old_programme_name_lng2 != programme_name_lng2:
            filter_condition = Q(programme_name_lng1=programme_name_lng1) | Q(programme_name_lng2=programme_name_lng2)
            if Programme.objects.filter(filter_condition).exclude(id=id).count() > 0:
                return JsonResponse({"error": "name_lng_programme_exists"})
            else:
                programme_obj = Programme.objects.get(id=id)
                programme_obj.programme_name_lng1 = programme_name_lng1
                programme_obj.programme_name_lng2 = programme_name_lng2
                programme_obj.save()
                return JsonResponse({"success": "programme_updated_successfully"})
        else:
            programme_obj = Programme.objects.get(id=id)
            programme_obj.programme_name_lng1 = programme_name_lng1
            programme_obj.programme_name_lng2 = programme_name_lng2
            programme_obj.save()
            return JsonResponse({"success": "programme_updated_successfully"})
    else:
        return JsonResponse({"error": programme_serializer.errors})

#View All Programmes
@api_view(['POST'])
@permission_classes([AllowAny])
def view_all_programmes(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    programmes= Programme.objects.all().order_by('id').values('id', 'programme_name_lng1','programme_name_lng2')
    return JsonResponse({'success': list(programmes)})


#  View One Programme

@api_view(['POST'])
@permission_classes([AllowAny])
def view_one_programme(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    programme_serializer = ProgrammeSerializer(data=request.data)
    if programme_serializer.is_valid():
        id = programme_serializer.data['id']
        if Programme.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'programme_not_found'})

        programme_obj = Programme.objects.get(id=id)

        return JsonResponse({'success': {
            'id': programme_obj.id,
        'programme_name_lng1':programme_obj.programme_name_lng1,
        'programme_name_lng2':programme_obj.programme_name_lng2,
       }})
    else:
        return JsonResponse({'error': programme_serializer.errors})
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_all_grades_by_programme(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_programme_serializer = GradeProgrammeSerializer(data=request.data)
    if grade_programme_serializer.is_valid():
        programme_id = grade_programme_serializer.data['programme_id']
        grades_in_programme = Grade_Programme.objects.filter(programme_id_id=programme_id).values_list(
            # 'reg_grade_id__grade_id__grade_name_lng1',
            'reg_grade_id', flat=True
        ).distinct()
        print(grades_in_programme)
        grades_without_programme  = Registration_Grade.objects.select_related('grade').exclude(id__in=grades_in_programme).values(
            'grade_id__grade_name_lng1',
            'id'
        ).distinct()

        # print(grad)
        # grade_programmes = Grade_Programme.objects.filter(id=id).select_related('Programme','Registration_Grade', 'Grade').values(
        #      'programme_id__programme_name', 'id', 'reg_grade_id__grade_id__grade_name_lng1'
        # )
        return JsonResponse({"success": list(grades_without_programme)})
    else:
        return JsonResponse({"error": grade_programme_serializer.errors})
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_grade_programme(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_programme_serializer = GradeProgrammeSerializer(data=request.data)
    if grade_programme_serializer.is_valid():
        # token = year_serializer.data['token']
        reg_grade_ids = grade_programme_serializer.data['reg_grade_ids']
        programme_id = grade_programme_serializer.data['programme_id']
        gender = grade_programme_serializer.data['gender']
        is_active = grade_programme_serializer.data['is_active']

        print(reg_grade_ids[0].replace("'",""))
        for reg_grade_id in list(reg_grade_ids[0].replace(",","")):
            print(reg_grade_id)
            grade_programme = Grade_Programme.objects.create(
                reg_grade_id_id=reg_grade_id,
                programme_id_id=programme_id,
                gender=gender,
                is_active=is_active
            )
            grade_programme.save()
        return JsonResponse({"success": "grade_programme_added_successfully"})

    else:
        return JsonResponse({"error": grade_programme_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_programme_by_grades(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_programme_serializer = GradeProgrammeSerializer(data=request.data)
    if grade_programme_serializer.is_valid():
        reg_grade_id = grade_programme_serializer.data['reg_grade_id']
        grade_programmes = Grade_Programme.objects.filter(reg_grade_id_id=reg_grade_id).values('id',program_name =F('programme_id__programme_name_lng1'))

        return JsonResponse({"success": list(grade_programmes)})
    else:
        return JsonResponse({"error": grade_programme_serializer.errors})


# Add National Setting
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_national_setting(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    national_setting_serializer = NationalSettingSerializer(data=request.data)
    if national_setting_serializer.is_valid():
        # token = year_serializer.data['token']
        is_numeric = national_setting_serializer.data['is_numeric']
        national_length = national_setting_serializer.data['national_length']

        if is_numeric not in [0, 1]:
            return JsonResponse({"error":"is_numeric_must_be_0_or_1."})

        if not national_length.isdigit() :
            return JsonResponse({"error": "national_length must be a valid integer"})
        if int(national_length) <= 8:
            return JsonResponse({"error": "national_length must be a valid greater than 8."})
        national_setting = National_Setting.objects.first()
        if national_setting:
            # Update existing national setting
            national_setting.is_numeric = is_numeric
            national_setting.length = national_length
            national_setting.save()
            return JsonResponse({"success": "national_setting_updated_successfully"})
        else:
            # Create new national setting
            # if National_Setting.objects.all().count()>0:
            #     return JsonResponse({"error":"add_only_one_national_setting"})
            National_Setting.objects.create(
                is_numeric=is_numeric,
                length=national_length
            )
            return JsonResponse({"success": "national_setting_added_successfully"})

        # national_setting = National_Setting.objects.create(
        #     is_numeric=is_numeric,
        #     length=national_length
        # )
        # national_setting.save()


    else:
        return JsonResponse({"error": national_setting_serializer.errors})


#Update National Setting
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def update_national_setting(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    national_setting_serializer = NationalSettingSerializer(data=request.data)
    if national_setting_serializer.is_valid():
        # id = national_setting_serializer.data['id']
        is_numeric = national_setting_serializer.data['is_numeric']
        national_length = national_setting_serializer.data['national_length']

        if is_numeric not in [0, 1]:
            return JsonResponse({"error":"is_numeric_must_be_0_or_1."})

        if not national_length.isdigit() :
            return JsonResponse({"error": "national_length must be a valid integer"})
        if int(national_length) <= 8:
            return JsonResponse({"error": "national_length must be a valid greater than 8."})
        # if National_Setting.objects.filter(id=id).count() < 1:
        #     return JsonResponse({"error": 'national_setting_not_found'})


        national_setting_obj = National_Setting.objects.first()
        national_setting_obj.is_numeric = is_numeric
        national_setting_obj.length=national_length
        national_setting_obj.save()
        return JsonResponse({"success": "national_setting_updated_successfully"})
    else:
        return JsonResponse({"error": national_setting_serializer.errors})


# Delete National Setting

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def delete_national_setting(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    national_setting_serializer = NationalSettingSerializer(data=request.data)
    if national_setting_serializer.is_valid():
        id = national_setting_serializer.data['id']
        if National_Setting.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": "national_setting_not_found"})
        national_setting = National_Setting.objects.get(id=id)
        national_setting.delete()
        return JsonResponse({"success": "national_setting_deleted_successfully"})
    else:
        return JsonResponse({"error": national_setting_serializer.errors})





# View all National Setting

@api_view(['POST'])
@permission_classes([AllowAny])
def view_national_setting(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    if National_Setting.objects.all().count()<1:
        return JsonResponse({"error":"national_setting_not_found"})

    national_settings= list(National_Setting.objects.all().values('is_numeric',national_length=F('length')))

    return JsonResponse({'success': national_settings[0]})

# Add Grade Type Sytem
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def add_grade_type(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_type_serializer = GradeTypeSystemSerializer(data=request.data)
    if grade_type_serializer.is_valid():
        grade_name = grade_type_serializer.data['grade_name']
        if GradeTypeSystem.objects.filter(grade_name=grade_name).count() > 0:
            return  JsonResponse({"error":"this_grade_type_found"})

        grade_type = GradeTypeSystem.objects.create(
            grade_name=grade_name,
        )
        grade_type.save()
        return JsonResponse({"success": "grade_type_added_successfully"})

    else:
        return JsonResponse({"error": grade_type_serializer.errors})


#Update Grade Type System
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def update_grade_type(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_type_serializer = GradeTypeSystemSerializer(data=request.data)
    if grade_type_serializer.is_valid():
        grade_name = grade_type_serializer.data['grade_name']
        id = grade_type_serializer.data['id']

        if GradeTypeSystem.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'grade_type_system_not_found'})

        old_grade_name = GradeTypeSystem.objects.get(id=id).grade_name
        if old_grade_name != grade_name:
            if GradeTypeSystem.objects.filter(grade_name=grade_name).count()>0:
                return JsonResponse({"error":"this_grade_type_exists"})
            else:
                grade_type_obj = GradeTypeSystem.objects.get(id=id)
                grade_type_obj.grade_name = grade_name
                grade_type_obj.save()
                return JsonResponse({"success": "grade_type_system_updated_successfully"})
        else:
            grade_type_obj = GradeTypeSystem.objects.get(id=id)
            grade_type_obj.grade_name = grade_name
            grade_type_obj.save()
            return JsonResponse({"success": "grade_type_system_updated_successfully"})
    else:
        return JsonResponse({"error": grade_type_serializer.errors})


# View One Grade Type System
@api_view(['POST'])
@permission_classes([AllowAny])
def view_one_grade_type(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_type_serializer = GradeTypeSystemSerializer(data=request.data)
    if grade_type_serializer.is_valid():
        id = grade_type_serializer.data['id']
        if GradeTypeSystem.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'grade_type_system_not_found'})

        grade_type_obj = GradeTypeSystem.objects.get(id=id)

        return JsonResponse({'success': {
            'id': grade_type_obj.id,
            'grade_name': grade_type_obj.grade_name}})
    else:
        return JsonResponse({'error': grade_type_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
def view_all_grade_types(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    grade_types= GradeTypeSystem.objects.all().order_by('id').values('id', 'grade_name')
    return JsonResponse({'success': list(grade_types)})

