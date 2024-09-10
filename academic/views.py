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
from datetime import datetime

from django.contrib.auth.decorators import login_required
# Create your views here.

# Create Year

# @login_required(login_url='users:login_front')


@api_view(['POST'])
@permission_classes([AllowAny])
def add_year(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # if not request.user.has_perm('academic.add_year'):
    #     return JsonResponse({'error': 'Permission denied'})
    # else:
    year_serializer = YearSerializer(data=request.data)
    if year_serializer.is_valid():
            # token = year_serializer.data['token']
            year = year_serializer.data['year']

            if not str(year).isdigit() or len(str(year)) != 4:
                return JsonResponse({"error":"please_enter_valid_year"})

            current_year = datetime.now().year
            min_year = current_year - 10
            max_year = current_year + 10

            if year < min_year or year > max_year:
                return JsonResponse({"error": "invalid_year"})

            if Year.objects.filter(year=year).count() > 0:
                return JsonResponse({"error": "year_exists"})

            new_year = Year.objects.create(
                year=year
            )
            new_year.save()
            return JsonResponse({"success": "year_addeed_successfully"})

    else:
            return JsonResponse({"error": year_serializer.errors})



@login_required(login_url='users:login_front')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_year(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    if not request.user.has_perm('academic.change_year'):
        return JsonResponse({'error': 'Permission denied'})
    else:
        year_serializer = YearSerializer(data=request.data)
        if year_serializer.is_valid():
            id = year_serializer.data['id']
            year = year_serializer.data['year']
            token = year_serializer.data["token"]

            if not str(year).isdigit() or len(str(year)) != 4:
                return JsonResponse({"error":"please_enter_valid_year"})

            current_year = datetime.now().year
            min_year = current_year - 10
            max_year = current_year + 10

            if year < min_year or year > max_year:
                return JsonResponse({"error": "invalid_year"})

            if Year.objects.filter(id=id).count() < 1:
                return JsonResponse({"error": 'year_not_found'})

            old_year = Year.objects.get(id=id).year
            if old_year != year:
                if Year.objects.filter(year=year).count() > 0:
                    return JsonResponse({"error": "year_exists"})
                else:

                    year_obj = Year.objects.get(id=id)
                    year_obj.year = year
                    year_obj.save()
            return JsonResponse({"success": "year_updated_successfully"})
        else:
            return JsonResponse({"error": year_serializer.errors})




# View All Year
@login_required(login_url='users:login_front')
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def view_all_years(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    if not request.user.has_perm('academic.view_year'):
        return JsonResponse({'error': 'Permission denied'})
    else:

        years = Year.objects.all().order_by('id').values('id', 'year')
        return JsonResponse({'success': list(years)})



# View One Year
@login_required(login_url='users:login_front')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def view_one_year(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    if not request.user.has_perm('academic.view_year'):
        return JsonResponse({'error': 'Permission denied'})
    year_serializer = YearSerializer(data=request.data)

    if year_serializer.is_valid():
        id = year_serializer.data['id']
        token = year_serializer.data['token']

        if Year.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'year_not_found'})

        year_obj = Year.objects.get(id=id)

        return JsonResponse({'success': {
            'id': year_obj.id,
            'year': year_obj.year}})
    else:
        return JsonResponse({'error': year_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_all_last_years(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    current_year = datetime.now().year
    years = Year.objects.filter(year__lt=current_year).order_by('id').values('id', 'year')
    return JsonResponse({'success': list(years)})
@api_view(['POST'])
@permission_classes([AllowAny])
def add_semster(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    semster_serializer = SemesterSerializer(data=request.data)
    if semster_serializer.is_valid():
       # token = year_serializer.data['token']
        no_of_quarters = semster_serializer.data['no_of_quarters']
        semester_name_lng1 = semster_serializer.data['semester_name_lng1']
        semester_name_lng2 = semster_serializer.data['semester_name_lng2']
        start_date = semster_serializer.data['start_date']
        end_date = semster_serializer.data['end_date']
        admission_on = semster_serializer.data['admission_on']
        is_default = semster_serializer.data['is_default']
        edit_std_status = semster_serializer.data['edit_std_status']
        grade_edit = semster_serializer.data['grade_edit']
        week_plan = semster_serializer.data['week_plan']
        ignore_weekly_pal_dates = semster_serializer.data['ignore_weekly_pal_dates']
        allow_add_material_cover = semster_serializer.data['allow_add_material_cover']
        job_applicant_on = semster_serializer.data['job_applicant_on']
        allow_to_create_weekly_plan = semster_serializer.data['allow_to_create_weekly_plan']
        allow_to_view_weekly_plan = semster_serializer.data['allow_to_view_weekly_plan']


        if Semester.objects.filter(semester_name_lng1=semester_name_lng1 , semester_name_lng2 = semester_name_lng2 ).count() > 0:
            return JsonResponse({"error": "semester_exists"})
        if int(allow_to_create_weekly_plan) not in range(1, 61) or int(allow_to_view_weekly_plan) not in range(1, 61):
            return JsonResponse({"error":"this_out_range"})
        semster = Semester.objects.create(
            no_of_quarters = no_of_quarters ,
            semester_name_lng1= semester_name_lng1 ,
            semester_name_lng2= semester_name_lng2 ,
            start_date= start_date ,
            end_date= end_date ,
            admission_on=admission_on ,
            is_default=is_default ,
            edit_std_status=edit_std_status ,
            grade_edit= grade_edit ,
            week_plan= week_plan ,
            ignore_weekly_pal_dates = ignore_weekly_pal_dates ,
            allow_add_material_cover = allow_add_material_cover ,
            job_applicant_on= job_applicant_on ,
            allow_to_create_weekly_plan = allow_to_create_weekly_plan ,
            allow_to_view_weekly_plan = allow_to_view_weekly_plan ,

        )
        semster.save()
        return JsonResponse({"success": "semster_added_successfully"})

    else:
            return JsonResponse({"error": semster_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
def update_semster(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    semster_serializer = SemesterSerializer(data=request.data)
    if semster_serializer.is_valid():
        id = semster_serializer.data['id']
        no_of_quarters = semster_serializer.data['no_of_quarters']
        semester_name_lng1 = semster_serializer.data['semester_name_lng1']
        semester_name_lng2 = semster_serializer.data['semester_name_lng2']
        start_date = semster_serializer.data['start_date']
        end_date = semster_serializer.data['end_date']
        admission_on = semster_serializer.data['admission_on']
        is_default = semster_serializer.data['is_default']
        edit_std_status = semster_serializer.data['edit_std_status']
        grade_edit = semster_serializer.data['grade_edit']
        week_plan = semster_serializer.data['week_plan']
        ignore_weekly_pal_dates = semster_serializer.data['ignore_weekly_pal_dates']
        allow_add_material_cover = semster_serializer.data['allow_add_material_cover']
        job_applicant_on = semster_serializer.data['job_applicant_on']
        allow_to_create_weekly_plan = semster_serializer.data['allow_to_create_weekly_plan']
        allow_to_view_weekly_plan = semster_serializer.data['allow_to_view_weekly_plan']
        # token = year_serializer.data["token"]
        if Semester.objects.filter(id=id).count()<1:
            return JsonResponse({"error": 'semester_not_found'})

        if Semester.objects.filter(semester_name_lng1=semester_name_lng1 , semester_name_lng2 = semester_name_lng2).exclude(id=id).exists():
            return JsonResponse({"error": 'semester_name_already_exists'})
        # Update the semester details
        semester = Semester.objects.get(id=id)
        semester.semester_name_lng1 = semester_name_lng1
        semester.semester_name_lng2 = semester_name_lng2
        semester.no_of_quarters = no_of_quarters
        semester.start_date = start_date
        semester.end_date = end_date
        semester.admission_on = admission_on
        semester.is_default = is_default
        semester.edit_std_status = edit_std_status
        semester.grade_edit = grade_edit
        semester.week_plan = week_plan
        semester.زignore_weekly_pal_dates = ignore_weekly_pal_dates
        semester.allow_add_material_cover = allow_add_material_cover
        semester.job_applicant_on = job_applicant_on
        semester.allow_to_create_weekly_plan = allow_to_create_weekly_plan
        semester.allow_to_view_weekly_plan = allow_to_view_weekly_plan
        semester.save()
        return JsonResponse({"success": "semester_updated_successfully"})
    else:
        return JsonResponse({"error": semster_serializer.errors})

# view all semesters
@api_view(['POST'])
@permission_classes([AllowAny])
def view_all_semsters(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    semsters = Semester.objects.all().order_by('id').values('id','semester_name_lng1','semester_name_lng2','no_of_quarters' , 'start_date','end_date' , 'admission_on','is_default')
    return JsonResponse({'success': list(semsters)})



 # View One Semester
@api_view(['POST'])
@permission_classes([AllowAny])
def view_one_semster(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    semster_serializer = SemesterSerializer(data=request.data)
    if semster_serializer.is_valid():
        id = semster_serializer.data['id']
        if Semester.objects.filter(id=id).count() < 1:
            return JsonResponse({"error": 'semster_not_found'})

        semster = Semester.objects.get(id=id)

        return JsonResponse({'success': {
            'id': semster.id,
            'semester_name_lng1': semster.semester_name_lng1,
            'semester_name_lng2': semster.semester_name_lng2,
            'no_of_quarters': semster.no_of_quarters,
            'start_date' : semster.start_date,
            'end_date' : semster.end_date,
            'admission_on' : semster.admission_on,
            'is_default' : semster.is_default,
            'edit_std_status': semster.edit_std_status,
            'grade_edit' : semster.grade_edit,
            'week_plan' : semster.week_plan,
            'ignore_weekly_pal_dates' : semster.ignore_weekly_pal_dates,
            'allow_add_material_cover' : semster.allow_add_material_cover,
            'job_applicant_on': semster.job_applicant_on,
            'allow_to_create_weekly_plan' : semster.allow_to_create_weekly_plan,
            'allow_to_view_weekly_plan' : semster.allow_to_view_weekly_plan
        }})
    else:
        return JsonResponse({'error': semster_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def add_acadmic_year(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
    if acadmic_year_serializer.is_valid():
        # token = year_serializer.data['token']
        year_id = acadmic_year_serializer.data['year_id']
        start_date = acadmic_year_serializer.data['start_date']
        end_date = acadmic_year_serializer.data['end_date']
        finance_start_date = acadmic_year_serializer.data['finance_start_date']
        finance_end_date = acadmic_year_serializer.data['finance_end_date']
        number_of_weeks = acadmic_year_serializer.data['number_of_weeks']

        if Academic_Years.objects.filter(year_id=year_id).count() > 0:
            return JsonResponse({"error":"this_year_already_added"})


        year_obj = Year.objects.get(id=year_id).year
        next_year = int(year_obj) + 1
        year_name_g= f"{year_obj}/{next_year}"


        hijri = convert.Gregorian(int(year_obj), 1, 1).to_hijri()
        hijri_year = hijri.year
        hijri_year_next = int(hijri_year) + 1
        # print(hijri_year)
        year_name_h = f"{hijri_year}/{hijri_year_next}"
        # print(year_name_h)

        acadmic_year = Academic_Years.objects.create(
            year_id_id=year_id,
            year_name_h=year_name_h,
            year_name_g=year_name_g,
            start_date=start_date,
            end_date=end_date,
            finance_year_name=year_name_g,
            finance_start_date =finance_start_date,
            finance_end_date =finance_end_date,
            number_of_weeks=number_of_weeks,

        )
        acadmic_year.save()
        return JsonResponse({"success":"acadmic_year_add_successfully"})
    else:
        return JsonResponse({"error": acadmic_year_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
def view_acadmic_years(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
    # if acadmic_year_serializer.is_valid():
    acadmic_years = Academic_Years.objects.select_related('year').values('id','year_name_g','start_date' , 'end_date' , year_name=F('year_id__year'))
    return JsonResponse({"success": list(acadmic_years)})



@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_acadmic_years_is_acceptedopen(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    acadmic_years = Academic_Years.objects.filter(admission_on=1).values('year_name_g', acadmic_year_id=F('id'))
    return JsonResponse({"success": list(acadmic_years)})
@api_view(['POST'])
@permission_classes([AllowAny])
def view_one_acadmic_year(request , id ):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    if Academic_Years.objects.filter(id=id).count() < 1:
        return JsonResponse({"error": "not_found"})

    acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
    if acadmic_year_serializer.is_valid():
        # id = acadmic_year_serializer.data['id']
        # if Academic_Years.objects.filter(id=id).count() < 1:
        #     return JsonResponse({"error": 'acadmic_year_not_found'})

        acadmic_year = Academic_Years.objects.get(id=id)

        return JsonResponse({'success': {
            'id': acadmic_year.id,
            'year': Year.objects.get(id=acadmic_year.year_id_id).year,
            'year_name_h':acadmic_year.year_name_h,
        'year_name_g':acadmic_year.year_name_g,
        'start_date':acadmic_year.start_date,
        'end_date':acadmic_year.end_date,
        'finance_year_name': acadmic_year.finance_year_name,
        'finance_start_date':acadmic_year.finance_start_date,
        'finance_end_date': acadmic_year.finance_end_date,
        'number_of_weeks': acadmic_year.number_of_weeks,

        }})
    else:
        return JsonResponse({'error': acadmic_year_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def update_acadmic_year(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
    if acadmic_year_serializer.is_valid():
        id = acadmic_year_serializer.data['id']
        # year_id = acadmic_year_serializer.data['year_id']
        # no_of_semesters = acadmic_year_serializer.data['no_of_semesters']
        # year_name = acadmic_year_serializer.data['year_name']
        # # year_name_ar = acadmic_year_serializer.data['year_name_ar']
        # # # finance_year_name = acadmic_year_serializer.data['finance_year_name']
        # semester_name = acadmic_year_serializer.data['semester_name']
        start_date = acadmic_year_serializer.data['start_date']
        end_date = acadmic_year_serializer.data['end_date']
        finance_start_date = acadmic_year_serializer.data['finance_start_date']
        finance_end_date = acadmic_year_serializer.data['finance_end_date']
        number_of_weeks = acadmic_year_serializer.data['number_of_weeks']
        # admission_on = acadmic_year_serializer.data['admission_on']
        # is_default = acadmic_year_serializer.data['is_default']
        # edit_std_status = acadmic_year_serializer.data['edit_std_status']
        # grade_edit = acadmic_year_serializer.data['grade_edit']
        # week_plan = acadmic_year_serializer.data['week_plan']
        # ignore_weekly_pal_dates = acadmic_year_serializer.data['ignore_weekly_pal_dates']
        # allow_add_material_cover = acadmic_year_serializer.data['allow_add_material_cover']
        # job_applicant_on = acadmic_year_serializer.data['job_applicant_on']
        # allow_to_create_weekly_plan = acadmic_year_serializer.data['allow_to_create_weekly_plan']
        # allow_to_view_weekly_plan = acadmic_year_serializer.data['allow_to_view_weekly_plan']

        # token = year_serializer.data["token"]
        if Academic_Years.objects.filter(id=id).count()<1:
            return JsonResponse({"error": 'acadmic_year_not_found'})

        # old_year = Academic_Years.objects.get(id=id).year_id
        # if old_year != year_id:
        #     return JsonResponse({"error":"year_error"}
        #     )
        # # if Academic_Years.objects.filter(year_id=year_id, no_of_semester=no_of_semesters).count() > 0:
        # #     return JsonResponse({"error": "this_year_already_added"})
        # old_no_of_semesters = Academic_Years.objects.get(id=id).no_of_semester
        # if no_of_semesters != old_no_of_semesters:
        #     if Academic_Years.objects.filter(year_id=year_id, no_of_semester=no_of_semesters).count() > 0:
        #         return JsonResponse({"error": "this_year_already_added"})
        # else:
        #
        #

        # year_obj = Year.objects.get(id=id).year
        #         # print(year_obj)
        #
        # next_year = int(year_obj) + 1
        # year_name_g = f"{year_obj}/{next_year}"
        # # print(year_name_g)
        #
        # hijri = convert.Gregorian(int(year_obj), 1, 1).to_hijri()
        # hijri_year = hijri.year
        # hijri_year_next = int(hijri_year) + 1
        # # print(hijri_year)
        # year_name_h = f"{hijri_year}/{hijri_year_next}"
        acadmic_year = Academic_Years.objects.get(id=id)
        # Update the semester details
        # acadmic_year.year_id_id =year_id
        # acadmic_year.no_of_semester=no_of_semesters
        # acadmic_year.semester_name=semester_name
        # acadmic_year.year_name_h=year_name_h
        # acadmic_year.year_name_g=year_name_g
        acadmic_year.start_date=start_date
        acadmic_year.end_date=end_date
        # acadmic_year.finance_year_name=year_name_g
        acadmic_year.finance_start_date=finance_start_date
        acadmic_year.finance_end_date=finance_end_date
        acadmic_year.number_of_weeks=number_of_weeks



        acadmic_year.save()
        return JsonResponse({"success": "acadmic_year_updated_successfully"})
    else:
        return JsonResponse({"error": acadmic_year_serializer.errors})
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
#         for i in range(no_of_semesters):
#             Semester.objects.create(
#                 semester_name_lng1= "First" if i ==0 else "Second" if i == 1 else "Third",
#                 semester_name_lng2 = "الاول" if i ==0 else "الثاني" if i == 1 else "الثالث",
#                 academic_year_semester_id_id= semster.id
#             )
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
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def view_all_semsters(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     semsters = Academic_Year_Semesters.objects.all().order_by('id').values('id','no_of_semesters','no_of_quarters_each_sem',year_name = F('year_id__year'))
#     return JsonResponse({'success': list(semsters)})
#
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
#     # acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     # if acadmic_year_serializer.is_valid():
#     year_semsters = Academic_Year_Semesters.objects.select_related('year').values('no_of_semesters', 'year_id',year_name=F('year_id__year'),semester_id =F('id'))
#     return JsonResponse({"success": list(year_semsters)})
#     # else:
#     #     return JsonResponse({"error": acadmic_year_serializer.errors})
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
#             year_name_h=year_name_h,
#             year_name_g=year_name_g,
#             start_date=start_date,
#             end_date=end_date,
#             # finance_year_name=year_name_g,
#             # finance_start_date =finance_start_date,
#             # finance_end_date =finance_end_date,
#             number_of_weeks=number_of_weeks,
#         admission_on=admission_on,
#         is_default=is_default,
#         edit_std_status=edit_std_status,
#         grade_edit=grade_edit,
#         week_plan=week_plan,
#         ignore_weekly_pal_dates=ignore_weekly_pal_dates,
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
#     # acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     # if acadmic_year_serializer.is_valid():
#     acadmic_years = Academic_Years.objects.select_related('year').values('id','semester_name','year_name_g','admission_on','is_default','edit_std_status','grade_edit',year_name=F('year_id__year'))
#     return JsonResponse({"success": list(acadmic_years)})
#     # else:
#     #     return JsonResponse({"error": acadmic_year_serializer.errors})
#
#
# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt
# def view_acadmic_years_is_acceptedopen(request):
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated,)
#     # acadmic_year_serializer = AcademicYearsSerializer(data=request.data)
#     # if acadmic_year_serializer.is_valid():
#     acadmic_years = Academic_Years.objects.filter(admission_on=1).values('year_name_g', 'semester_name','no_of_semester', acadmic_year_id=F('id'))
#     return JsonResponse({"success": list(acadmic_years)})
#     # else:
#     #     return JsonResponse({"error": acadmic_year_serializer.errors})
# @api_view(['POST'])
#
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
#         # year_id = acadmic_year_serializer.data['year_id']
#         # no_of_semesters = acadmic_year_serializer.data['no_of_semesters']
#         # year_name = acadmic_year_serializer.data['year_name']
#         # # year_name_ar = acadmic_year_serializer.data['year_name_ar']
#         # # # finance_year_name = acadmic_year_serializer.data['finance_year_name']
#         # semester_name = acadmic_year_serializer.data['semester_name']
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
#         # old_year = Academic_Years.objects.get(id=id).year_id
#         # if old_year != year_id:
#         #     return JsonResponse({"error":"year_error"}
#         #     )
#         # # if Academic_Years.objects.filter(year_id=year_id, no_of_semester=no_of_semesters).count() > 0:
#         # #     return JsonResponse({"error": "this_year_already_added"})
#         # old_no_of_semesters = Academic_Years.objects.get(id=id).no_of_semester
#         # if no_of_semesters != old_no_of_semesters:
#         #     if Academic_Years.objects.filter(year_id=year_id, no_of_semester=no_of_semesters).count() > 0:
#         #         return JsonResponse({"error": "this_year_already_added"})
#         # else:
#         #
#         #
#
#         # year_obj = Year.objects.get(id=id).year
#         #         # print(year_obj)
#         #
#         # next_year = int(year_obj) + 1
#         # year_name_g = f"{year_obj}/{next_year}"
#         # # print(year_name_g)
#         #
#         # hijri = convert.Gregorian(int(year_obj), 1, 1).to_hijri()
#         # hijri_year = hijri.year
#         # hijri_year_next = int(hijri_year) + 1
#         # # print(hijri_year)
#         # year_name_h = f"{hijri_year}/{hijri_year_next}"
#         acadmic_year = Academic_Years.objects.get(id=id)
#         # Update the semester details
#         # acadmic_year.year_id_id =year_id
#         # acadmic_year.no_of_semester=no_of_semesters
#         # acadmic_year.semester_name=semester_name
#         # acadmic_year.year_name_h=year_name_h
#         # acadmic_year.year_name_g=year_name_g
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