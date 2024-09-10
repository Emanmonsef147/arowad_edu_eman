from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from academic.models import *
from .serializers import *
from .models import *
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication
import re
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F ,Value
from django.db.models.functions import Concat
from datetime import date
from datetime import datetime , timedelta
date_format = '%Y-%m-%d'
from validate_email import validate_email
from django.db import transaction
from django.db.models import Count
import filetype
from django.core.exceptions import ObjectDoesNotExist
from usermgr.models import User_Profile , User_Type
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
import base64
# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_reggrades_bylimitages(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        date_of_birth = applicant_serializer.data['date_of_birth']
        reg_grades = Reg_Grade_Academic_Years.objects.filter(reg_grade_id__age_limit_g__gte=date_of_birth ).select_related(
 'reg_grade_id__grade_id'
).values('reg_grade_id',
         grade_id = F('reg_grade_id__grade_id_id'),
grade_name =F('reg_grade_id__grade_id__grade_name_lng1') ).distinct()
        return JsonResponse({"success": {'registergrades':list(reg_grades)}})
    else:
        return JsonResponse({"error": applicant_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_academic_year_bylimitages(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        date_of_birth = applicant_serializer.data['date_of_birth']
        reg_grade_id = applicant_serializer.data['reg_grade_id']
        academic_years = Reg_Grade_Academic_Years.objects.filter(reg_grade_id=reg_grade_id,reg_grade_id__age_limit_g__gte=date_of_birth ).select_related('academic_year_id').values('academic_year_id',year_name=F('academic_year_id_id__year_name_g' ),semster_name = F('academic_year_id_id__semester_name'))
        return JsonResponse({"success": {'academic_year':list(academic_years)}})
    else:
        return JsonResponse({"error": applicant_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_status_by_category(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    status_serializer = StatusSerializer(data=request.data)
    if status_serializer.is_valid():
        category = status_serializer.data['category']
        status = Status.objects.filter(category=category ).values('category','name','id')
        return JsonResponse({"success": list(status)})
    else:
        return JsonResponse({"error": status_serializer.errors})

def get_expected_mime_types(doc_type):
    if doc_type == 'PDF':
        return ['application/pdf']
    elif doc_type == 'Image':
        return ['image/jpeg', 'image/png', 'image/gif']
    # elif doc_type in ['Word', 'Excel', 'PowerPoint', 'Text', 'CSV', 'Presentation', 'Spreadsheet', 'Document']:
    #     return ['application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    #             'application/msword',
    #             'application/vnd.ms-excel',
    #             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    #             'application/vnd.ms-powerpoint',
    #             'text/plain',
    #             'text/csv']
    # elif doc_type == 'Archive':
    #     return ['application/zip']
    # elif doc_type == 'Audio':
    #     return ['audio/mpeg', 'audio/mp4']
    # elif doc_type == 'Video':
    #     return ['video/mp4', 'video/mpeg']
    else:
        return []

def validate_file(file, expected_mime_types):
    kind = filetype.guess(file.read())
    if kind is not None and kind.mime in expected_mime_types:
        return True
    return False


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def applicant_document_type_create(request):
    serializer = ApplicantDocumentTypeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        doc_name_lng1 = serializer.data['doc_name_lng1']
        doc_name_lng2 = serializer.data['doc_name_lng2']
        doc_desc_lng1 = serializer.data['doc_desc_lng1']
        doc_desc_lng2 = serializer.data['doc_desc_lng2']
        is_necessary = serializer.data['is_necessary']
        doc_type = serializer.data['doc_type']
        notes = serializer.data['notes']
        # school_id = serializer.data['school_id']


        check_length = [doc_name_lng1, doc_name_lng2, doc_desc_lng1, doc_desc_lng2]
        for val in check_length:
            if len(val) > 25:
                return JsonResponse({"error": f"{val} should be less than 25 characters."})
            if not isinstance(val, str):
                return JsonResponse({"error": f"{val} should be a string."})

        if not isinstance(notes, str) and len(notes) > 50:
            return JsonResponse(
                {"error": f"{notes} should be a string or notes should be less than 50 characters."})

        check_duplicate_en = [doc_name_lng1, doc_desc_lng1]
        for val in check_duplicate_en:
            if ApplicantDocumentType.objects.filter(doc_name_lng1=val).count() > 0:
                return JsonResponse({"error": f"{val} already exists."})

        check_duplicate_ar = [doc_name_lng2, doc_desc_lng2]
        for val in check_duplicate_ar:
            if ApplicantDocumentType.objects.filter(doc_name_lng2=val).count() > 0:
                return JsonResponse({"error": f"{val} already exists."})
        names = [doc_name_lng1, doc_name_lng2]
        formatted_names = []
        for name in names:
            lowercase_name = name.lower()

            # Remove spaces and replace with underscores
            formatted_name = lowercase_name.replace(" ", "_")

            formatted_names.append(formatted_name)
        try:
                ApplicantDocumentType.objects.create(
                    doc_name_lng1=formatted_names[0],
                    doc_name_lng2 = formatted_names[1],
                    doc_desc_lng1=doc_desc_lng1,
                    doc_desc_lng2=doc_desc_lng2,
                    is_necessary=is_necessary,
                    doc_type=doc_type,
                    notes = notes ,
                    school_id_id=user.useradditionalfields.school_id.id,
                    created_by=user, updated_by=user)
                return JsonResponse({"success": "Applicant Document Type created successfully"},
                                )
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": serializer.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def applicant_document_type_view_all(request):
    try:
        applicant_document_types = ApplicantDocumentType.objects.all().values('id','doc_name_lng1','doc_name_lng2','doc_desc_lng1','doc_desc_lng2','doc_type','is_necessary')
        return JsonResponse({"success":list(applicant_document_types)})
    except ObjectDoesNotExist:
        return JsonResponse({"error": "No Applicant Document Types found"})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def applicant_document_type_view_one(request):
    doc_type_id = request.data.get("doc_type_id")
    if not doc_type_id:
        return JsonResponse({"error": "Document Type ID is required"})

    try:
        applicant_document_type = ApplicantDocumentType.objects.get(id=doc_type_id)
    except ApplicantDocumentType.DoesNotExist:
        return JsonResponse({"error": "Applicant Document Type not found"})

    data = {
        "doc_type_id": applicant_document_type.id,
        "doc_name_lng1": applicant_document_type.doc_name_lng1,
        "doc_name_lng2": applicant_document_type.doc_name_lng2,
        "doc_desc_lng1": applicant_document_type.doc_desc_lng1,
        "doc_desc_lng2": applicant_document_type.doc_desc_lng2,
        "doc_type":applicant_document_type.doc_type,
        "is_necessary":applicant_document_type.is_necessary,
        "notes": applicant_document_type.notes
    }

    return JsonResponse({"success": data})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def applicant_document_type_update(request):
    doc_type_id = request.data.get('doc_type_id')
    try:
        applicant_doc_type = ApplicantDocumentType.objects.get(id=doc_type_id)
    except ApplicantDocumentType.DoesNotExist:
        return JsonResponse({"error": "Applicant Document Type does not exist"})
    serializer = ApplicantDocumentTypeSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        doc_name_lng1 = serializer.data['doc_name_lng1']
        doc_name_lng2 = serializer.data['doc_name_lng2']
        doc_desc_lng1 = serializer.data['doc_desc_lng1']
        doc_desc_lng2 = serializer.data['doc_desc_lng2']
        notes = serializer.data['notes']
        is_necessary = serializer.data['is_necessary']
        doc_type = serializer.data['doc_type']

        check_length = [doc_name_lng1, doc_name_lng2, doc_desc_lng1, doc_desc_lng2]
        for val in check_length:
            if len(val) > 25:
                return JsonResponse({"error": f"{val} should be less than 25 characters."})
            if not isinstance(val, str):
                return JsonResponse({"error": f"{val} should be a string."})

        if not isinstance(notes, str) and len(notes) > 50:
            return JsonResponse(
                {"error": f"{notes} should be a string or notes should be less than 50 characters."})

        check_duplicate_en = [doc_name_lng1, doc_desc_lng1]
        for val in check_duplicate_en:
            if ApplicantDocumentType.objects.filter(doc_name_lng1=val).exclude(id=doc_type_id).exists():
                return JsonResponse({"error": f"{val} already exists."})

        check_duplicate_ar = [doc_name_lng2, doc_desc_lng2]
        for val in check_duplicate_ar:
            if ApplicantDocumentType.objects.filter(doc_name_lng2=val).exclude(id=doc_type_id).exists():
                return JsonResponse({"error": f"{val} already exists."})

        try:
            applicant_doc_type.doc_name_lng1 = doc_name_lng1
            applicant_doc_type.doc_name_lng2 = doc_name_lng2
            applicant_doc_type.doc_desc_lng1 = doc_desc_lng1
            applicant_doc_type.doc_desc_lng2 = doc_desc_lng2
            applicant_doc_type.notes = notes
            applicant_doc_type.is_necessary=is_necessary
            applicant_doc_type.doc_type=doc_type
            applicant_doc_type.updated_by = user
            applicant_doc_type.save()

            return JsonResponse({"success": "Applicant Document Type updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({"error": serializer.errors})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def applicant_document_type_delete(request):
    doc_type_id = request.data.get("doc_type_id")
    if not doc_type_id:
        return JsonResponse({"error": "Document Type ID is required"})
    try:
        applicant_doc_type = ApplicantDocumentType.objects.get(id=doc_type_id)
    except ApplicantDocumentType.DoesNotExist:
        return JsonResponse({"error": "Applicant Document Type not found"})
    try:
        applicant_doc_type.delete()
        return JsonResponse({"success": "Applicant Document Type deleted successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)})

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_applicant(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        #form1
        user = request.user

        iqama_id= applicant_serializer.data['iqama_id']
        date_of_birth = applicant_serializer.data['date_of_birth']
        gender = applicant_serializer.data['gender']
        nationality_id = applicant_serializer.data['nationality_id']
        acadmic_year_id = applicant_serializer.data['acadmic_year_id']
        reg_grade_id = applicant_serializer.data['reg_grade_id']
        programme_id = applicant_serializer.data['programme_id']

        #form2
        first_name = applicant_serializer.data['first_name']
        second_name = applicant_serializer.data['second_name']
        third_name = applicant_serializer.data['third_name']
        last_name = applicant_serializer.data['last_name']
        first_name_ar = applicant_serializer.data['first_name_ar']
        second_name_ar = applicant_serializer.data['second_name_ar']
        third_name_ar = applicant_serializer.data['third_name_ar']
        last_name_ar = applicant_serializer.data['last_name_ar']
        religion_id = applicant_serializer.data['religion_id']
        language_id = applicant_serializer.data['language_id']
        birth_country = applicant_serializer.data['birth_country']
        iqama_source = applicant_serializer.data['iqama_source']
        iqama_source_date = applicant_serializer.data['iqama_source_date']
        passport_id = applicant_serializer.data['passport_id']
        passport_expiry_date = applicant_serializer.data['passport_expiry_date']
        passport_country = applicant_serializer.data['passport_country']
        parent_iqama_id = applicant_serializer.data['parent_iqama_id']
        parent_iqama_source = applicant_serializer.data['parent_iqama_source']
        parent_iqama_source_date = applicant_serializer.data['parent_iqama_source_date']

        #form3
        email = applicant_serializer.data['email']
        phone1 = applicant_serializer.data['phone1']
        phone2 = applicant_serializer.data['phone2']
        address_line = applicant_serializer.data['address_line']
        country_id = applicant_serializer.data['country_id']
        state_id = applicant_serializer.data['state_id']
        city_id = applicant_serializer.data['city_id']

        # add this fields in form student information in front

        # status_id = applicant_serializer.data['email']
        # has_paid = applicant_serializer.data['email']
        # print_token = applicant_serializer.data['email']
        # amount = applicant_serializer.data['email']
        # have_siblling = applicant_serializer.data['email']

        #form4
        # Applicant Gurdian Data
        first_name_gur = applicant_serializer.data['first_name_gur']
        second_name_gur = applicant_serializer.data['second_name_gur']
        third_name_gur = applicant_serializer.data['third_name_gur']
        last_name_gur = applicant_serializer.data['last_name_gur']
        first_name_gur_ar = applicant_serializer.data['first_name_gur_ar']
        second_name_gur_ar = applicant_serializer.data['second_name_gur_ar']
        third_name_gur_ar = applicant_serializer.data['third_name_gur_ar']
        last_name_gur_ar = applicant_serializer.data['last_name_gur_ar']
        iqama_id_gur = applicant_serializer.data['iqama_id_gur']
        iqama_source_gur = applicant_serializer.data['iqama_source_gur']
        iqama_source_date_gur = applicant_serializer.data['iqama_source_date_gur']
        nationality_id_gur = applicant_serializer.data['nationality_id_gur']
        country_id_gur = applicant_serializer.data['country_id_gur']
        state_id_gur = applicant_serializer.data['state_id_gur']
        city_id_gur = applicant_serializer.data['city_id_gur']

        passport_id_gur= applicant_serializer.data['passport_id_gur']
        passport_expiry_date_gur = applicant_serializer.data['passport_expiry_date_gur']
        passport_country_gur = applicant_serializer.data['passport_country_gur']
        relation_gur = applicant_serializer.data['relation_gur']
        language_id_gur = applicant_serializer.data['language_id_gur']
        religion_id_gur = applicant_serializer.data['religion_id_gur']
        date_of_birth_gur = applicant_serializer.data['date_of_birth_gur']

        education = applicant_serializer.data['education']
        job = applicant_serializer.data['job']
        company = applicant_serializer.data['company']
        address_line_gur = applicant_serializer.data['address_line_gur']
        mobile_phone = applicant_serializer.data['mobile_phone']
        mother_phone = applicant_serializer.data['mother_phone']
        emergency_phone = applicant_serializer.data['emergency_phone']
        email_gur = applicant_serializer.data['email_gur']
        employee_id_name = applicant_serializer.data['employee_id_name']




        # applicant_previous_school_data
        last_attended_school = request.data.get('last_attended_school', None)
        last_attended_school_ar = request.data.get('last_attended_school_ar',None)
        last_score = request.data.get('last_score', None)
        evaluvation = request.data.get('evaluvation', None)
        last_grade_id = request.data.get('last_grade_id', None)
        last_year_id = request.data.get('last_year_id', None)
        last_country_id = request.data.get('last_country_id', None)
        # last_attended_school = applicant_serializer.data['last_attended_school']
        # last_attended_school_ar = applicant_serializer.data['last_attended_school_ar']
        # last_score = applicant_serializer.data['last_score']
        # evaluation = applicant_serializer.data['evaluation']
        # last_grade_id = applicant_serializer.data['last_grade_id']
        # last_year_id = applicant_serializer.data['last_year_id']
        # last_country_id = applicant_serializer.data['last_country_id']

        #Applicant Documents

        str_applicant_document_types_id = request.data.get("applicant_document_types_id", "")
        # print(str_applicant_document_types_id)

        new_applicant_no = ''
        if Applicant.objects.exists():
            old = Applicant.objects.last().applicant_no
            if old:
                old2 = ""
                for l in old.split('A'):
                    if l.startswith('0'):
                        old2 = l[1:]
                        print(old2)
                    else:
                        old2 = l
                        # print(old2)
                old2 = int(old2)
                old2 = old2 + 1
                # print(str(old2))
                n = 0
                n = len(str(old2))
                app_number = old2
                for i in range(n, 5):
                    if n != 5:
                        app_number = '0' + str(app_number)
                        # print(i)

                new_applicant_no= 'A' + str(app_number)
        else:
            new_applicant_no = 'A00001'

        # if len(str(iqama_id)) != len(str(National_Setting.objects.last().length)):
        #     print(len(str(National_Setting.objects.last().length)))
        #     print(len(iqama_id))
        last_national_setting = National_Setting.objects.last()
        national_setting_length = last_national_setting.length
        national_setting_is_numeric = last_national_setting.is_numeric
        s_iqama = [parent_iqama_id, iqama_id,iqama_id_gur]
        for iqama in s_iqama:
            if national_setting_is_numeric and not iqama.isdigit():
                return JsonResponse({"error": "National ID must be numeric."})

            if national_setting_length is not None and len(iqama) != national_setting_length:
                return JsonResponse(
                    {"error": f"{iqama}must be at least {national_setting_length} characters long."})

        s_names = [first_name, second_name,
                   third_name, last_name,
                   first_name_ar,second_name_ar,
                   third_name_ar, last_name_ar,
                   first_name_gur,first_name_gur_ar,
                   second_name_gur,second_name_gur_ar,
                   third_name_gur,third_name_gur_ar,
                   last_name_gur,last_name_gur_ar]

        for nam in s_names:
            if len(nam) < 2:
                return JsonResponse({"error": nam + "_less_than_2_character"})
        for nam in s_names:
            special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if not special_char.search(nam) == None:
                return JsonResponse({"error": nam + "_no_special_char"})

        s_passport = [passport_id_gur,passport_id]
        for passport in s_passport:
            if len(str(passport)) < 14:
                return JsonResponse({'error': 'applicant_student_passport_id_less_than_14'})
        iqama_src = [iqama_source,parent_iqama_source,iqama_source_gur]
        for src in iqama_src:
            if len(str(src)) < 5:
                return JsonResponse({'error': 'iqama_source_less_than_5'})
            if not src.isalpha():
                return JsonResponse({'error': 'iqama_source_only_letters'})

        dates = [date_of_birth,iqama_source_date,parent_iqama_source_date,passport_expiry_date,date_of_birth_gur,iqama_source_date_gur]
        for d in dates:
            if not datetime.strptime(d, date_format):
                return JsonResponse({'error': d + '_not_a_date'})

            if len(d) < 10:
                return JsonResponse({'error': d + '_less_than_10_char'})

        if datetime.strptime(date_of_birth, date_format).date() > date.today():
                return JsonResponse({'error': str(date_of_birth) + '_not_valid'})

        if gender == 'Male' or gender == 'Female':
            gender = applicant_serializer.data['gender']
        else:
            return JsonResponse({"error": "gender_not_male_or_female"})

        countries = [nationality_id,birth_country,passport_country,country_id_gur,country_id]
        for country in countries:
            if Country.objects.filter(id=country).count() <1:
                return JsonResponse({"error": "country_not_found"})

        if Academic_Years.objects.filter(id=acadmic_year_id).count() < 1:
            return JsonResponse({"error": "acadmic_year_not_found"})

        if Registration_Grade.objects.filter(id=reg_grade_id).count() < 1:
            return JsonResponse({"error": "register_grade_not_found"})

        if Grade_Programme.objects.filter(id=programme_id).count() < 1:
            return JsonResponse({"error": "programme_grade_not_found"})

        # if Status.objects.filter(id=status_id).count() < 1 :
        #     return JsonResponse({"error":"status_not_found"})
        if RELIGION.objects.filter(id=religion_id).count() < 1 :
            return JsonResponse({"error":"religion_not_found"})
        if Langs.objects.filter(id=language_id).count() < 1 :
            return JsonResponse({"error":"language_not_found"})

        states = [state_id, state_id_gur]
        for st in states:
            if State.objects.filter(id=st).count() < 1:
                return JsonResponse({"error": "state_not_found"})

        cities = [city_id,city_id_gur]
        for city in cities:
            if Cities.objects.filter(id=city).count()  < 1:
                return JsonResponse({"error": "city_not_found"})

        phones = [phone1,phone2,mobile_phone,mother_phone,emergency_phone]
        for phone in phones:
            if phone is None:
                return JsonResponse({'error': 'applicant_student_phone_null'})
            if len(str(phone)) < 3:
                return JsonResponse({'error': 'applicant_student_phone_less_than_5'})
            for i in phone:
                if not i.isdigit():
                    return JsonResponse({'error': 'applicant_student_phone_no_digit'})

        emails = [email , email_gur]
        for em in emails:
            if em is not None:
                if len(em) < 8:
                    return JsonResponse({'error': 'email_less_than_8'})
                if not validate_email(em):
                    return JsonResponse({'error': 'email_invalid'})
            else:
                return JsonResponse({'error': 'email_null'})

        if Applicant.objects.filter(iqama_id=iqama_id).count() > 0:
            return JsonResponse({"error": "iqama_id_exists"})


        #Applicant Document Type


        #-----------------------------------------------------------------------------------------

        doc_names = ApplicantDocumentType.objects.all()
        attachment_files = []

        for name in doc_names:
            file_name = name.doc_name_lng1
            uploaded_file = request.FILES.get(file_name)
            if name.is_necessary == 1:
                if file_name not in request.FILES or not uploaded_file:
                    return JsonResponse({"error": f"Attachment {file_name} is required."})
            if uploaded_file:
                doc_type = name.doc_type
                expected_mime_types = get_expected_mime_types(doc_type)
                if expected_mime_types and validate_file(uploaded_file, expected_mime_types):
                    attachment_files.append({name.id: uploaded_file})
                else:
                    return JsonResponse(
                        {"error": f"Invalid file type for attachment: {file_name} should be {doc_type}."})


        document_types = str_applicant_document_types_id.split(',')
        print("Length of document types:",len(document_types))
        print("Length of attachment_files:", len(attachment_files))

        if len(document_types) != len(attachment_files):
            return JsonResponse({"error": "Attachment and document type count mismatch."})

        applicant_document_types_id = [int(id) for id in str_applicant_document_types_id.split(',') if id.isdigit()]
        for i in range(len(applicant_document_types_id)):
            if ApplicantDocumentType.objects.filter(id=applicant_document_types_id[i]).count() == 0:
                return JsonResponse({"error": "Applicant Document Type not found"})

        add_aplc=True
        while add_aplc == True:
            try:
                with transaction.atomic():
                    applicant = Applicant.objects.create(
                        applicant_no =new_applicant_no,
                        iqama_id=iqama_id,
                        date_of_birth = date_of_birth,
                        gender = gender,
                        nationality_id_id =nationality_id,
                        acadmic_year_id_id = acadmic_year_id,
                        reg_grade_id_id = reg_grade_id,
                        programme_id_id=programme_id,
                        first_name = first_name,
                        second_name = second_name,
                        third_name = third_name,
                        last_name = last_name,
                        first_name_ar = first_name_ar,
                        second_name_ar = second_name_ar,
                        third_name_ar = third_name_ar,
                        last_name_ar = last_name_ar,

                        birth_country_id = birth_country,
                        iqama_source = iqama_source,
                        iqama_source_date = iqama_source_date,
                        parent_iqama_id = parent_iqama_id,
                        parent_iqama_source = parent_iqama_source,
                        parent_iqama_source_date = parent_iqama_source_date,
                        passport_id = passport_id,
                        passport_expiry_date = passport_expiry_date,
                        passport_country_id = passport_country,
                        religion_id_id = religion_id,
                        language_id_id = language_id,
                        country_id_id=country_id,
                        city_id_id = city_id,
                        state_id_id =state_id,
                        address_line = address_line,
                        phone1 = phone1,
                        phone2 = phone2,
                        email = email,
                        employee_id_name=employee_id_name ,
                        created_by=user,
                        updated_by=user,
                        status_id_id=Status.objects.get(status_order_by=1).status_order_by,
                        # have_siblling=have_siblling,
                        # print_token=print_token,
                        # has_paid=has_paid,
                        # amount=amount

                    )
                    #create user profile
                    user = User.objects.create_user(username=applicant_serializer.data['first_name_gur'], email=applicant_serializer.data['email_gur'],
                                                    password='Aitsp', is_active=True)
                    full_name = f"{applicant_serializer.data['first_name_gur']} {applicant_serializer.data['second_name_gur']}"
                    user_id = User.objects.get(username=applicant_serializer.data['first_name_gur'], email=applicant_serializer.data['email_gur'])
                    User_Profile.objects.create(user_id=user_id, fullname=full_name, phone=applicant_serializer.data['mobile_phone'],
                                                address=applicant_serializer.data['address_line_gur'],nat_id = applicant_serializer.data['iqama_id'])

                    # Create Applicant Pervious School Data


                    # Create the object with the appropriate values
                    if last_grade_id in [None , 0 ]:
                        last_grade_id = None
                    # print("last_grade_id after check:", last_grade_id)

                    school_data =  [last_attended_school ,last_attended_school_ar ,last_score , evaluvation , last_year_id,last_country_id]
                    result = all(item is None or item is not None for item in school_data)
                    # print("result of check:", result)
                    if result :
                        last_school = ApplicantPreviousSchoolData.objects.create(
                            applicant_id_id=applicant.id,
                            last_attended_school=last_attended_school,
                            last_attended_school_ar=last_attended_school_ar,
                            last_score=last_score,
                            evaluvation=evaluvation,
                            last_grade_id_id=last_grade_id,
                            last_year_id_id=last_year_id,
                            last_country_id_id=last_country_id,
                            created_by=user,
                            updated_by=user,)
                    else:
                        last_school= ApplicantPreviousSchoolData.objects.create(
                                applicant_id_id=applicant.id,
                                last_attended_school=None,
                                last_attended_school_ar=None,
                                last_score=None,
                                evaluvation=None,
                                last_grade_id_id=None,
                                last_year_id_id=None,
                                last_country_id_id=None,
                                created_by=user,
                                updated_by=user, )
                    # Create Applicant Guardian Data
                    app_gurdian = Applicant_Guardians.objects.create(
                        applicant_id_id = applicant.id,
                        first_name=first_name_gur,
                        second_name = second_name_gur,
                        third_name = third_name_gur,
                        last_name = last_name_gur,
                        first_name_ar=first_name_gur_ar,
                        second_name_ar =second_name_gur_ar,
                        third_name_ar=third_name_gur_ar,
                        last_name_ar=last_name_gur_ar,
                        iqama_id =iqama_id_gur,
                        iqama_source =iqama_source_gur,
                        iqama_source_date =iqama_source_date_gur,
                        nationality_id_id=nationality_id_gur,
                        passport_id= passport_id_gur,
                        passport_expiry_date=passport_expiry_date_gur,
                        passport_country_id=passport_country_gur,
                        religion_id_id=religion_id_gur,
                        language_id_id=language_id_gur,
                        _relation = relation_gur,
                        date_of_birth =date_of_birth_gur,
                        education=education,
                        job=job,
                        company=company,
                        address_line = address_line_gur,

                        email=email_gur,
                        country_id_id = country_id_gur,
                        state_id_id =state_id_gur,
                        city_id_id =city_id_gur,
                        mobile_phone= mobile_phone,
                        mother_phone = mother_phone,
                        emergency_phone=emergency_phone,
                        created_by = user,
                        updated_by = user

                    )
                    #Applicant Document Type
                    for attachment in attachment_files:
                        print(attachment)
                        for doc_type_id, uploaded_file in attachment.items():
                            doc_type = ApplicantDocumentType.objects.get(id=doc_type_id)
                            print(doc_type,uploaded_file)
                            ApplicantDocumentAttachment.objects.create(applicant_id_id=applicant.id,
                                                                      applicant_document_types_id_id=doc_type.id,
                                                                      attachment_file=uploaded_file,
                                                                       created_by=user, updated_by=user,
                                                                       )
                add_aplc = False
            except Exception as e:
                add_aplc = True
                return JsonResponse({'error': str(e)})

        return JsonResponse({"success": "applicant_added_successfully" , "no_of_applicant":applicant.applicant_no})

    else:
        return JsonResponse({"error": applicant_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_applicant_by_year(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        acadmic_year_id = applicant_serializer.data['acadmic_year_id']
        applicants = Applicant.objects.filter(acadmic_year_id=acadmic_year_id).values('reg_grade_id','status_id_id__name','reg_grade_id__grade_id__grade_name_lng1').annotate(status_count=Count('status_id_id'))
        grouped_data = {}
        status_categories = {
            'pay-admission-fee': 'in process',
            'pending-fee': 'in process',
            'success-test': 'in process',
            'fail-test': 'in process',
            'receive documents': 'in process',
            'not receive documents': 'in process',
            'pending': 'pending',
            'reject': 'reject',
            'accept': 'accept'
        }

        total_counts = {
            'pending': 0,
            'accept': 0,
            'reject': 0,
            'in process': 0
        }

        for app in applicants:
            reg_grade_id = app['reg_grade_id']
            grade_name = app['reg_grade_id__grade_id__grade_name_lng1']
            status_key = app['status_id_id__name']
            status_count = app['status_count']

            status_name = status_categories.get(status_key)
            total_counts[status_name] += status_count

            if grade_name not in grouped_data:
                grouped_data[grade_name] = {
                    'reg_grade_id': reg_grade_id,
                    'statuses': {},
                    'total_status_count': 0
                }

            if status_name not in grouped_data[grade_name]['statuses']:
                grouped_data[grade_name]['statuses'][status_name] = 0

            grouped_data[grade_name]['statuses'][status_name] += status_count
            grouped_data[grade_name]['total_status_count'] += status_count

        formatted_response = [
            {
                'reg_grade_id': grade_data['reg_grade_id'],
                'grade_name': grade,
                'statuses': [
                    {'status_name': status_name, 'status_count': count}
                    for status_name, count in grade_data['statuses'].items()
                ],
                'total_status_count': grade_data['total_status_count']
            }
            for grade, grade_data in grouped_data.items()
        ]

        final_response = {
            "success": formatted_response,
            "total-status-pending": total_counts['pending'],
            "total_status-accept": total_counts['accept'],
            "total_status-reject": total_counts['reject'],
            "total_status-inprocess": total_counts['in process'],
            'total': sum(total_counts.values())
        }

        return JsonResponse({"success": final_response})

    else:
        return JsonResponse({"error": applicant_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
def view_applicants_by_status(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        acadmic_year_id = applicant_serializer.data.get('acadmic_year_id')
        status_id = applicant_serializer.data.get('status_id')
        if status_id and status_id is not None:
            applicants_query = Applicant.objects.filter(acadmic_year_id=acadmic_year_id,status_id=status_id)
        else:
            applicants_query = Applicant.objects.filter(acadmic_year_id=acadmic_year_id)
            print(applicants_query)

        applicants = applicants_query.annotate(
            full_name=Concat('first_name', Value(' '), 'second_name', Value(' '), 'third_name', Value(' '), 'last_name')
        ).values(
            'applicant_no', 'full_name', 'phone1', 'created_at',
            grade_name=F('reg_grade_id__grade_id__grade_name_lng1'),
            programme_name=F('programme_id__programme_id__programme_name_lng1'),
            status=F('status_id__name'))

        return JsonResponse({"success": list(applicants)})
    else:
        return JsonResponse({"error": applicant_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_applicant_by_grade(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        reg_grade_id = applicant_serializer.data['reg_grade_id']
        acadmic_year_id = applicant_serializer.data['acadmic_year_id']
        if Applicant.objects.filter(reg_grade_id=reg_grade_id).count()>0:
            applicants_query = Applicant.objects.filter(reg_grade_id=reg_grade_id,acadmic_year_id=acadmic_year_id)
            applicants = applicants_query.annotate(
                full_name=Concat('first_name', Value(' '), 'second_name', Value(' '), 'third_name', Value(' '),
                                 'last_name')
            ).values(
                'applicant_no', 'full_name', 'phone1', 'created_at',
                grade_name=F('reg_grade_id__grade_id__grade_name_lng1'),
                programme_name=F('programme_id__programme_id__programme_name_lng1'),
                status=F('status_id__name'))
        else:
            return  JsonResponse({"error":"no_applicants_in_this_grade"})

        return JsonResponse({"success": list(applicants)})

    else:
        return JsonResponse({"error": applicant_serializer.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_applicant_by_filter(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        reg_grade_id = applicant_serializer.data['reg_grade_id']
        applicant_no = applicant_serializer.data['applicant_no']
        status_id  = applicant_serializer.data['status_id']
        gender = applicant_serializer.data['gender']
        start_date =  applicant_serializer.data['start_date']
        end_date = applicant_serializer.data['end_date']
        programme_id = applicant_serializer.data['programme_id']



        # date_object = datetime.strptime(end_date, '%Y-%m-%d')
        #
        # # Add one day to the date
        # new_date = date_object + timedelta(days=1)
        #
        # # Convert back to string if needed
        # new_date_string = new_date.strftime('%Y-%m-%d')
        filter_conditions = {}

        if applicant_no != 'all':
            filter_conditions['applicant_no'] = applicant_no

        if status_id != 'all':
            filter_conditions['status_id__id'] = status_id

        if gender != 'all':
            filter_conditions['gender'] = gender

        if programme_id != 'all':
            filter_conditions['programme_id__id'] = programme_id

        if reg_grade_id != 'all':
            filter_conditions['reg_grade_id__id'] = reg_grade_id

        # Add the date range condition
        if start_date != '' and end_date != '':
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                end_date_obj += timedelta(days=1)  # Include end date
                filter_conditions['created_at__range'] = [start_date_obj, end_date_obj]
            except ValueError:
                return JsonResponse({"error": "Invalid_date_format.Please use YYYY-MM-DD."})

        applicants_filtered = Applicant.objects.filter(**filter_conditions).values(
                'applicant_no', 'first_name', 'second_name', 'third_name', 'last_name', 'phone1','created_at',
                grade_name = F('reg_grade_id__grade_id__grade_name_lng1'), programme_name = F('programme_id__programme_id__programme_name_lng1'),
                status =F('status_id__name'))
        for applicant in applicants_filtered:
            applicant['full_name'] = ' '.join(filter(None, [applicant.get('first_name'), applicant.get('second_name'),
                                                            applicant.get('third_name'), applicant.get('last_name')]))

            # Remove individual name fields if needed in the final response
            del applicant['first_name']
            del applicant['second_name']
            del applicant['third_name']
            del applicant['last_name']
        print(list(applicants_filtered))

        return JsonResponse({"success": list(applicants_filtered)})

    else:
        return JsonResponse({"error": applicant_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_applicants_by_filter(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        reg_grade_id = applicant_serializer.data['reg_grade_id']
        applicant_no = applicant_serializer.data['applicant_no']
        status_id = applicant_serializer.data['status_id']
        gender = applicant_serializer.data['gender']
        start_date = applicant_serializer.data['start_date']
        end_date = applicant_serializer.data['end_date']
        programme_id = applicant_serializer.data['programme_id']
        filter_conditions = Q()

        filter_conditions &= Q(
            applicant_no=applicant_no if applicant_no != 'all' else Q())
        filter_conditions &= Q(
            status_id__id=status_id if status_id != 'all' else Q())
        filter_conditions &= Q(gender=gender if gender != 'all' else Q())
        filter_conditions &= Q(
            programme_id__id=programme_id if programme_id != 'all' else Q())
        filter_conditions &= Q(
            reg_grade_id__id=reg_grade_id if reg_grade_id != 'all' else Q())


        if start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)  # Include end date
                filter_conditions &= Q(created_at__range=(start_date_obj, end_date_obj))
            except ValueError:
                return JsonResponse({"error": "Invalid_date_format.Please use YYYY-MM-DD."})

        applicants_filtered = (Applicant.objects.filter(filter_conditions).annotate(
                               full_name=Concat('first_name', Value(' '), 'second_name', Value(
            ' '), 'third_name', Value(' '),
        'last_name')
        ).values(
            'applicant_no', 'full_name', 'phone1', 'created_at',
            grade_name=F('reg_grade_id__grade_id__grade_name_lng1'),
            programme_name=F('programme_id__programme_id__programme_name_lng1'),
            status=F('status_id__name')))

        return JsonResponse({"success": list(applicants_filtered)})

    else:
        return JsonResponse({"error": applicant_serializer.errors})


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def view_status_applicants(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        iqama_id= applicant_serializer.data['iqama_id']
        applicant_no = applicant_serializer.data['applicant_no']
        applicants = Applicant.objects.filter(iqama_id = iqama_id ,
                                              applicant_no = applicant_no).annotate(
                               full_name=Concat('first_name', Value(' '), 'second_name')
        ).values(
            'full_name','applicant_no','iqama_id',
            'email' , 'phone1',
            applicant_status=F('status_id__category'),
            grade_name=F('reg_grade_id__grade_id__grade_name_lng1'),)
        return JsonResponse({"success": list(applicants)})

    else:
        return JsonResponse({"error": applicant_serializer.errors})


@api_view(['POST'])
@permission_classes((AllowAny,))

def login_applicant(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        iqama_id = applicant_serializer.data['iqama_id']
        applicant_no = applicant_serializer.data['applicant_no']
        isuser= Applicant.objects.get(applicant_no = applicant_no).is_user
        if isuser == 0 :
            user_profile  = User_Profile.objects.get(nat_id = iqama_id)
            if  user_profile is not None :
                user_id = user_profile.user_id_id
                print(user_id)
                user_name = User.objects.get(id = user_id).username
                print(user_name)
                if not User.objects.filter(username=user_name):
                    return JsonResponse({'error': 'user_not_found'})

                userauth = authenticate(request, username=user_name,password ='Aitsp' ,
                                                is_active=True)
                if userauth:
                                login(request, userauth)
                                new_token = ""
                                # userati=User.objects.all()
                                idd = 0
                                idd = User.objects.get(username=user_name).id
                                uouo = User_Profile.objects.get(user_id_id=idd)
                                image_base64 = ''
                                if Token.objects.filter(user_id=idd).count() > 0:
                                    with open("media/" + str(uouo.userimg), "rb") as image_file:
                                        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
                                        # print(image_base64)
                                    token = ""
                                    tokena = Token.objects.all()
                                    new_token = tokena.get(user_id=idd).key
                                    # print("old token",new_token)
                                else:
                                    new_token = Token.objects.create(
                                        user=User.objects.get(username=user_name))
                                    # print("new token",new_token)
                                    with open("media/" + str(uouo.userimg), "rb") as image_file:
                                        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
                                return JsonResponse({"username":user_name,
                                                 "token": str(new_token),
                                                 "user_img": image_base64,
                                                 "user_id": idd,
                                                 # "user_permission":userprofile.objects.get(userp=idd).perm_m
                                                 })
                                # HttpResponseRedirect('/dashboard')
                                # return redirect('/')
                elif User.objects.filter(username=user_name, is_active=False):
                    return JsonResponse({"error": "user_is_not_active"})
                else:
                    return JsonResponse({'error': 'wrong_username_or_password'})

            else :
                return  JsonResponse({'error':'user_profile_not_match'})
        else :
            return  JsonResponse ({'error':'change normal login'})


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def logout_applicant(request):
        authentication_classes = (TokenAuthentication)
        permission_classes = (IsAuthenticated,)
        # Delete the token associated with the user
        toto=LogoutSerializer(data=request.data)
        tokena=""
        if toto.is_valid():
            token=toto.data['token']

        # print(request.user)
            Token.objects.filter(key=token).delete()
            # logout(request)
            return JsonResponse({"success": "Successfully_logged_out."})
        else:
            return JsonResponse({"error":toto.errors})


@api_view(['POST'])
@permission_classes((AllowAny,))
def view_one_applicant(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        iqama_id = applicant_serializer.data['iqama_id']
        applicant_no = applicant_serializer.data['applicant_no']
        applicants = Applicant.objects.filter(iqama_id=iqama_id,
                                              applicant_no=applicant_no).values(
             'applicant_no','created_at','first_name','second_name','last_name',
            'first_name_ar' , 'second_name_ar' , 'last_name_ar',
            'iqama_id','iqama_source','iqama_source_date','date_of_birth','parent_iqama_id','parent_iqama_source','parent_iqama_source_date',
            'passport_id','passport_expiry_date','gender','have_siblling','employee_id_name',
            'address_line','email','phone1','phone2',

            grade_name=F('reg_grade_id__grade_id__grade_name_lng1'),
            programme_name = F('programme_id__programme_id__programme_name_lng1'),
            nationality = F('nationality_id'),
            guardian_first_name = F('applicant_guardians__first_name'),
            guardian_second_name = F('applicant_guardians__second_name'),
            guardian_last_name = F('applicant_guardians__last_name'),
            guardian_first_name_ar=F('applicant_guardians__first_name_ar'),
            guardian_second_name_ar=F('applicant_guardians__second_name_ar'),
            guardian_last_name_ar=F('applicant_guardians__last_name_ar'),
            guardian_iqama_id=F('applicant_guardians__iqama_id'),
            guardian_iqama_source=F('applicant_guardians__iqama_source'),
            guardian_iqama_source_date=F('applicant_guardians__iqama_source_date'),
            guardian_date_of_birth=F('applicant_guardians__date_of_birth'),
            guardian_relation = F('applicant_guardians___relation'),
            guardian_education=F('applicant_guardians__education'),
            guardian_job=F('applicant_guardians__job'),
            guardian_company=F('applicant_guardians__company'),
            guardian_address_line=F('applicant_guardians__address_line'),
            guardian_email=F('applicant_guardians__email'),
            guardian_mobile_phone=F('applicant_guardians__mobile_phone'),
            guardian_mother_phone=F('applicant_guardians__mother_phone'),
            guardian_emergency_phone =F('applicant_guardians__emergency_phone'),
            guardian_country =F('applicant_guardians__country_id'),
            guardian_state =F('applicant_guardians__state_id'),
            guardian_city =F('applicant_guardians__city_id'),
            birth_country_name= F('birth_country'),
            passport_country_name = F('passport_country'),
            language = F('language_id'),
            religion = F('religion_id'),
            country = F('country_id'),
            state = F('state_id'),
            city = F('city_id') ,
            last_attended_school = F('applicantpreviousschooldata__last_attended_school'),
            last_attended_school_ar = F('applicantpreviousschooldata__last_attended_school_ar'),
            evaluation = F('applicantpreviousschooldata__evaluvation'),
            last_score = F('applicantpreviousschooldata__last_score'),
            last_grade = F('applicantpreviousschooldata__last_grade_id__grade_name_lng1'),
            last_year = F('applicantpreviousschooldata__last_year_id__year'),
            last_country = F('applicantpreviousschooldata__last_country_id')
        )
        applicants_list = list(applicants)
        for applicant in applicants_list:
            if applicant['have_siblling'] == 0:
                applicant['have_siblling'] = 'Not Present'
            if applicant['employee_id_name'] is None:
                applicant['employee_id_name'] = 'Not Present'
        guardian_country_name = Country.objects.get(id=applicant['guardian_country']).name
        nationality = Country.objects.get(id=applicant['nationality']).name
        birth_country_name = Country.objects.get(id=applicant['birth_country_name']).name
        passport_country_name = Country.objects.get(id=applicant['passport_country_name']).name
        language = Langs.objects.get(id=applicant['language']).lang_name
        religion = RELIGION.objects.get(id=applicant['religion']).name
        country = Country.objects.get(id=applicant['country']).name
        state = State.objects.get(id=applicant['state']).name
        city = Cities.objects.get(id=applicant['city']).name
        guardian_state = State.objects.get(id=applicant['guardian_state']).name
        guardian_city = Cities.objects.get(id=applicant['guardian_city']).name
        last_country = Country.objects.get(id=applicant['last_country']).name
        applicant.update({
            'guardian_country': guardian_country_name,
            'guardian_state': guardian_state,
            'guardian_city': guardian_city,
            'nationality': nationality,
            'birth_country_name': birth_country_name,
            'passport_country_name': passport_country_name,
            'language': language,
            'religion': religion,
            'country': country,
            'state': state,
            'city': city,
            'last_country': last_country,
        })
        # applicant['guardian_country'] = guardian_country_name
        # applicant['guardian_state'] = guardian_state
        # applicant['guardian_city'] = guardian_city
        # applicant['nationality'] = nationality
        # applicant['birth_place'] = birth_place
        # applicant['country_passport'] = country_passport
        # applicant['language'] = language
        # applicant['religion'] = religion
        # applicant['country'] = country
        # applicant['state'] = state
        # applicant['city'] = city
        # applicant['last_country'] = last_country


        # applicant['contact_information'] = {
        #     'address': applicant.pop('address_line', 'Not Present'),
        #     'email': applicant.pop('email', 'Not Present'),
        #     'phone1': applicant.pop('phone1', 'Not Present'),
        #     'phone2': applicant.pop('phone2', 'Not Present'),
        # }
        return JsonResponse({"success": list(applicants_list)})

    else:
        return JsonResponse({"error": applicant_serializer.errors})


@api_view(['POST'])
@permission_classes((AllowAny,))
def update_applicant(request):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    applicant_serializer = ApplicantSerializer(data=request.data)
    if applicant_serializer.is_valid():
        iqama_id = applicant_serializer.data['iqama_id']
        applicant_no = applicant_serializer.data['applicant_no']
        # personal details
        first_name = applicant_serializer.data['first_name']
        second_name = applicant_serializer.data['second_name']
        third_name = applicant_serializer.data['third_name']
        last_name = applicant_serializer.data['last_name']
        first_name_ar = applicant_serializer.data['first_name_ar']
        second_name_ar = applicant_serializer.data['second_name_ar']
        third_name_ar = applicant_serializer.data['third_name_ar']
        last_name_ar = applicant_serializer.data['last_name_ar']
        # date_of_birth = applicant_serializer.data['date_of_birth']
        birth_country = applicant_serializer.data['birth_country']

        # nationality_id = applicant_serializer.data['nationality_id']
        iqama_source = applicant_serializer.data['iqama_source']
        iqama_source_date = applicant_serializer.data['iqama_source_date']
        parent_iqama_id = applicant_serializer.data['parent_iqama_id']
        parent_iqama_source = applicant_serializer.data['parent_iqama_source']
        parent_iqama_source_date = applicant_serializer.data['parent_iqama_source_date']
        passport_id = applicant_serializer.data['passport_id']
        passport_expiry_date = applicant_serializer.data['passport_expiry_date']
        passport_country = applicant_serializer.data['passport_country']
        gender = applicant_serializer.data['gender']
        religion_id = applicant_serializer.data['religion_id']
        language_id = applicant_serializer.data['language_id']
        # contact details
        email = applicant_serializer.data['email']
        phone1 = applicant_serializer.data['phone1']
        phone2 = applicant_serializer.data['phone2']
        address_line = applicant_serializer.data['address_line']
        country_id = applicant_serializer.data['country_id']
        state_id = applicant_serializer.data['state_id']
        city_id = applicant_serializer.data['city_id']
        # gurdian details
        first_name_gur = applicant_serializer.data['first_name_gur']
        second_name_gur = applicant_serializer.data['second_name_gur']
        third_name_gur = applicant_serializer.data['third_name_gur']
        last_name_gur = applicant_serializer.data['last_name_gur']
        first_name_gur_ar = applicant_serializer.data['first_name_gur_ar']
        second_name_gur_ar = applicant_serializer.data['second_name_gur_ar']
        third_name_gur_ar = applicant_serializer.data['third_name_gur_ar']
        last_name_gur_ar = applicant_serializer.data['last_name_gur_ar']
        iqama_id_gur = applicant_serializer.data['iqama_id_gur']
        iqama_source_gur = applicant_serializer.data['iqama_source_gur']
        iqama_source_date_gur = applicant_serializer.data['iqama_source_date_gur']
        passport_id_gur = applicant_serializer.data['passport_id_gur']
        passport_expiry_date_gur = applicant_serializer.data['passport_expiry_date_gur']
        passport_country_gur = applicant_serializer.data['passport_country_gur']
        relation_gur = applicant_serializer.data['relation_gur']
        date_of_birth_gur = applicant_serializer.data['date_of_birth_gur']
        language_id_gur = applicant_serializer.data['language_id_gur']
        religion_id_gur = applicant_serializer.data['religion_id_gur']
        nationality_id_gur = applicant_serializer.data['nationality_id_gur']
        education = applicant_serializer.data['education']
        job = applicant_serializer.data['job']
        company = applicant_serializer.data['company']
        address_line_gur = applicant_serializer.data['address_line_gur']
        mobile_phone = applicant_serializer.data['mobile_phone']
        mother_phone = applicant_serializer.data['mother_phone']
        emergency_phone = applicant_serializer.data['emergency_phone']
        email_gur = applicant_serializer.data['email_gur']
        employee_id_name = applicant_serializer.data['employee_id_name']
        country_id_gur = applicant_serializer.data['country_id_gur']
        state_id_gur = applicant_serializer.data['state_id_gur']
        city_id_gur = applicant_serializer.data['city_id_gur']
        # pervious school details
        last_attended_school = request.data.get('last_attended_school', None)
        last_attended_school_ar = request.data.get('last_attended_school_ar', None)
        last_score = request.data.get('last_score', None)
        evaluvation = request.data.get('evaluvation', None)
        last_grade_id = request.data.get('last_grade_id', None)
        last_year_id = request.data.get('last_year_id', None)
        last_country_id = request.data.get('last_country_id', None)

        if Applicant.objects.filter(iqama_id = iqama_id , applicant_no = applicant_no).count() < 1 :
            return  JsonResponse({'error':'this_applicant_not_found'})
        applicant_status = Applicant.objects.get(iqama_id = iqama_id , applicant_no = applicant_no).status_id_id
        if applicant_status != 1 :
            return JsonResponse({"error": "you_cannot_update_this_applicant"})

        # Validate iqama_id depend on national settings
        last_national_setting = National_Setting.objects.last()
        national_setting_length = last_national_setting.length
        national_setting_is_numeric = last_national_setting.is_numeric

        s_iqama = [parent_iqama_id, iqama_id, iqama_id_gur]
        for iqama in s_iqama:
            if national_setting_is_numeric and not iqama.isdigit():
                return JsonResponse({"error": "National ID must be numeric."})

            if national_setting_length is not None and len(iqama) != national_setting_length:
                return JsonResponse(
                    {"error": f"{iqama}must be at least {national_setting_length} characters long."})
        # Validate names
        s_names = [first_name, second_name,
                   third_name, last_name,
                   first_name_ar, second_name_ar,
                   third_name_ar, last_name_ar,
                   first_name_gur, first_name_gur_ar,
                   second_name_gur, second_name_gur_ar,
                   third_name_gur, third_name_gur_ar,
                   last_name_gur, last_name_gur_ar]

        for nam in s_names:
            if len(nam) < 2:
                return JsonResponse({"error": nam + "_less_than_2_character"})
        # for nam in s_names:
        #     special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        #     if not special_char.search(nam) == None:
        #         return JsonResponse({"error": nam + "_no_special_char"})
            if re.search(r'[@_!#$%^&*()<>?/\|}{~:]', nam):
                return JsonResponse({"error": f"{nam}_no_special_char"})

        ## Validate passport IDs
        s_passport = [passport_id_gur, passport_id]
        for passport in s_passport:
            if len(str(passport)) < 14:
                return JsonResponse({'error': 'applicant_student_passport_id_less_than_14'})
        # Validate iqama sources
        iqama_src = [iqama_source, parent_iqama_source, iqama_source_gur]
        for src in iqama_src:
            if len(str(src)) < 5:
                return JsonResponse({'error': 'iqama_source_less_than_5'})
            if not src.isalpha():
                return JsonResponse({'error': 'iqama_source_only_letters'})
        # Validate dates
        dates = [ iqama_source_date, parent_iqama_source_date, passport_expiry_date,
                 date_of_birth_gur, iqama_source_date_gur]
        for d in dates:
            if not datetime.strptime(d, date_format):
                return JsonResponse({'error': d + '_not_a_date'})

            if len(d) < 10:
                return JsonResponse({'error': d + '_less_than_10_char'})

        # Validate gender
        if gender == 'Male' or gender == 'Female':
            gender = applicant_serializer.data['gender']
        else:
            return JsonResponse({"error": "gender_not_male_or_female"})

        # Validate countries
        countries = [birth_country, passport_country, country_id_gur, country_id]
        for country in countries:
            if Country.objects.filter(id=country).count() < 1:
                return JsonResponse({"error": "country_not_found"})
        # Validate religion
        if RELIGION.objects.filter(id=religion_id).count() < 1:
            return JsonResponse({"error": "religion_not_found"})
        ## Validate languages
        if Langs.objects.filter(id=language_id).count() < 1:
            return JsonResponse({"error": "language_not_found"})
        # Validate states
        states = [state_id, state_id_gur]
        for st in states:
            if State.objects.filter(id=st).count() < 1:
                return JsonResponse({"error": "state_not_found"})
        # Validate cities
        cities = [city_id, city_id_gur]
        for city in cities:
            if Cities.objects.filter(id=city).count() < 1:
                return JsonResponse({"error": "city_not_found"})
        # Validate phones
        phones = [phone1, phone2, mobile_phone, mother_phone, emergency_phone]
        for phone in phones:
            if phone is None:
                return JsonResponse({'error': 'applicant_student_phone_null'})
            if len(str(phone)) < 3:
                return JsonResponse({'error': 'applicant_student_phone_less_than_5'})
            for i in phone:
                if not i.isdigit():
                    return JsonResponse({'error': 'applicant_student_phone_no_digit'})
        # Validate emails
        emails = [email, email_gur]
        for em in emails:
            if em is not None:
                if len(em) < 8:
                    return JsonResponse({'error': 'email_less_than_8'})
                if not validate_email(em):
                    return JsonResponse({'error': 'email_invalid'})
            else:
                return JsonResponse({'error': 'email_null'})

        # if Applicant.objects.filter(iqama_id=iqama_id).count() > 0:
        #     return JsonResponse({"error": "iqama_id_exists"})
        old_applicant = Applicant.objects.get(iqama_id =iqama_id ,applicant_no =applicant_no)
        birth_country = Country.objects.get(id=birth_country)
        passport_country = Country.objects.get(id=passport_country)
        passport_country_gur = Country.objects.get(id=passport_country_gur)
        old_applicant.first_name = first_name
        old_applicant.second_name = second_name
        old_applicant.third_name = third_name
        old_applicant.last_name = last_name
        old_applicant.first_name_ar = first_name_ar
        old_applicant.second_name_ar = second_name_ar
        old_applicant.third_name_ar = third_name_ar
        old_applicant.last_name_ar = last_name_ar
        old_applicant.birth_country = birth_country
        old_applicant.iqama_source = iqama_source
        old_applicant.iqama_source_date = iqama_source_date
        old_applicant.parent_iqama_id = parent_iqama_id
        old_applicant.parent_iqama_source = parent_iqama_source
        old_applicant.parent_iqama_source_date = parent_iqama_source_date
        old_applicant.passport_id_id = passport_id
        old_applicant.passport_expiry_date = passport_expiry_date
        old_applicant.passport_country = passport_country
        old_applicant.gender = gender
        old_applicant.religion_id_id =religion_id
        old_applicant.language_id_id = language_id
        # contact details
        old_applicant.email =email
        old_applicant.phone1 = phone1
        old_applicant.phone2 = phone2
        old_applicant.address_line = address_line
        old_applicant.country_id_id = country_id
        old_applicant.state_id_id = state_id
        old_applicant.city_id_id = city_id
        old_applicant.employee_id_name = employee_id_name
        old_applicant.save()
        # update guardian details
        applicant_id = old_applicant.id
        old_gur = Applicant_Guardians.objects.get(applicant_id = applicant_id)
        # print(old_gur)
        language_id_gur = Langs.objects.get(id=language_id_gur)
        religion_id_gur = RELIGION.objects.get(id=religion_id_gur)
        nationality_id_gur = Country.objects.get(id=nationality_id_gur)
        country_id_gur = Country.objects.get(id=country_id_gur)
        state_id_gur = State.objects.get(id=state_id_gur)
        city_id_gur = Cities.objects.get(id=city_id_gur)
        old_gur.first_name = first_name_gur
        old_gur.second_name = second_name_gur
        old_gur.third_name = third_name_gur
        old_gur.last_name = last_name_gur
        old_gur.first_name_ar = first_name_gur_ar
        old_gur.second_name_ar = second_name_gur_ar
        old_gur.third_name_ar = third_name_gur_ar
        old_gur.last_name_ar = last_name_gur_ar
        old_gur.iqama_id = iqama_id_gur
        old_gur.iqama_source = iqama_source_gur
        old_gur.iqama_source_date = iqama_source_date_gur
        old_gur.passport_id = passport_id_gur
        old_gur.passport_expiry_date =passport_expiry_date_gur
        old_gur.passport_country= passport_country_gur
        old_gur._relation = relation_gur
        old_gur.date_of_birth= date_of_birth_gur
        old_gur.language_id= language_id_gur
        old_gur.religion_id = religion_id_gur
        old_gur.nationality_id = nationality_id_gur
        old_gur.education = education
        old_gur.job = job
        old_gur.company = company
        old_gur.address_line= address_line_gur
        old_gur.mobile_phone = mobile_phone
        old_gur.mother_phone = mother_phone
        old_gur.emergency_phone = emergency_phone
        old_gur.email= email_gur
        old_gur.country_id =country_id_gur
        old_gur.state_id = state_id_gur
        old_gur.city_id  = city_id_gur
        old_gur.save()

        if last_grade_id in [None, 0]:
            last_grade_id = None

        school_data = [last_attended_school, last_attended_school_ar, last_score, evaluvation, last_year_id,
                       last_country_id]

        result = all(item is None or item is not None for item in school_data)

        old_school = ApplicantPreviousSchoolData.objects.get(applicant_id=applicant_id)

        if result:
            old_school.last_attended_school = last_attended_school
            old_school.last_attended_school_ar = last_attended_school_ar
            old_school.last_score = last_score
            old_school.evaluvation = evaluvation

            old_school.last_grade_id = Grade.objects.get(id=last_grade_id) if last_grade_id is not None else None
            old_school.last_year_id = Year.objects.get(id=last_year_id) if last_year_id is not None else None
            old_school.last_country_id = Country.objects.get(
                id=last_country_id) if last_country_id is not None else None
        else:
            old_school.last_attended_school = None
            old_school.last_attended_school_ar = None
            old_school.last_score = None
            old_school.evaluvation = None
            old_school.last_grade_id = None
            old_school.last_year_id = None
            old_school.last_country_id = None

        old_school.save()
        return JsonResponse({"success": "you_can_update_successfully_this_applicant"})


    else:
        return JsonResponse({"error": applicant_serializer.errors})
