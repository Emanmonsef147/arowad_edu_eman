from django.contrib.auth.models import User
from django.db import models
from countries.models import *
from datetime import datetime




class GradeTypeSystem(models.Model):
    grade_name = models.CharField(max_length=255)

    class Meta:
        app_label = 'general_settings'
        db_table = 'general_settings_grade_type_system'
class Schools(models.Model):
    name_lng1 = models.CharField(max_length=255)
    name_lng2 = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    last_seeded_at = models.DateField(auto_now_add=True)
    is_deleted = models.IntegerField(default=1)
    notes = models.TextField(default='notes',blank=True,null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_school_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_school_user',default=1)

    class Meta:
        app_label = 'general_settings'
        db_table = 'general_settings_schools'

class FinanceFeeCollections(models.Model):
    pass

    class Meta:
        app_label = 'general_settings'
        db_table = 'general_settings_finance_fee_collections'

class Events(models.Model):
    title_lng1 = models.CharField(max_length=255, null=True, blank=True)
    title_lng2 = models.CharField(max_length=255, null=True, blank=True)
    description_lng1 = models.TextField(blank=True, null=True)
    description_lng2 = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    is_common = models.IntegerField(default=1)
    is_holiday = models.IntegerField(default=1)
    is_exam = models.IntegerField(default=1)
    is_due = models.IntegerField(default=1)
    finance_fee_collections_id = models.ForeignKey(FinanceFeeCollections,on_delete=models.DO_NOTHING,default=1)
    finance_fee_collections_type = models.CharField(max_length=255, blank=True, null=True)
    school_id = models.ForeignKey(Schools,on_delete=models.DO_NOTHING)
    notes = models.TextField(default='notes',blank=True,null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_event_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_event_user',default=1)

    class Meta:
        app_label = 'general_settings'
        db_table = 'general_settings_events'

# Create your models here.
class Stage(models.Model):
    name_lng1 = models.CharField(max_length=255,blank=True, null=True)
    name_lng2 = models.CharField(max_length=255,blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_stage_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_stage_user',default=1)

    class Meta:
        app_label = 'general_settings'

class Grade(models.Model):
    CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),)
    GENDER_CHOICES = (
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Mixed', 'Mixed'))
    grade_name_lng1 = models.CharField(max_length=255,blank=True, null=True)
    grade_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255,blank=True, null=True)
    # section_name = models.CharField(choices=GENDER_CHOICES,blank=True, null=True)
    # is_deleted = models.IntegerField(default=0,blank=True, null=True)
    grading_type_id = models.ForeignKey(GradeTypeSystem,on_delete=models.DO_NOTHING,null=True,blank=True)
    grade_order = models.IntegerField(choices=CHOICES,blank=True, null=True)
    stage_id = models.ForeignKey(Stage, on_delete=models.DO_NOTHING)

    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_grade_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_grade_user',default=1)

    class Meta:
        app_label = 'general_settings'
        
class Stu_Intial_Class(models.Model):
    name_lng1 = models.CharField(max_length=255,null=True,blank=True)
    name_lng2 = models.CharField(max_length=255,null=True,blank=True)
    grade_id = models.ForeignKey(Grade,on_delete=models.DO_NOTHING)
    acadmic_year_id = models.ForeignKey('academic.Academic_Years',on_delete=models.DO_NOTHING,blank=True,null=True)
    programme_id = models.ForeignKey('general_settings.Programme', blank=True, null=True,
                                     on_delete=models.DO_NOTHING)

    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_intial_class_user', default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_intial_class_user', default=1)

    class Meta:
        app_label = 'general_settings'

class Programme(models.Model):
    programme_name_lng1 = models.CharField(max_length=255,null=True,blank=True)
    programme_name_lng2 = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_programme_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_programme_user',default=1)

    class Meta:
        app_label = 'general_settings'

class Stu_Class(models.Model):
    name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    programme_id = models.ForeignKey(Programme, on_delete=models.DO_NOTHING)
    grade_id = models.ForeignKey(Grade, on_delete=models.DO_NOTHING)
    student_categories_id = models.ForeignKey('StudentCategories', on_delete=models.DO_NOTHING, blank=True, null=True)
    school_id = models.ForeignKey(Schools, on_delete=models.DO_NOTHING, default=1)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_class_user', default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_class_user', default=1)

    class Meta:
        app_label = 'general_settings'
class Registration_Grade(models.Model):
    Bool_CHOICES = (
        (1, 1),
        (0, 0)
    )
    school_id = models.ForeignKey(Schools, on_delete=models.CASCADE,null=True)
    grade_id = models.ForeignKey(Grade, on_delete=models.CASCADE)
    is_allow_admission = models.SmallIntegerField(choices=Bool_CHOICES,blank=True, null=True)
    min_score = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    min_g_birthdate = models.DateField(blank=True, null=True)
    min_h_birthdate = models.DateField(blank=True, null=True)
    is_enable_approval_system = models.SmallIntegerField(choices=Bool_CHOICES,blank=True, null=True)
    is_subject_based_fee_colletion = models.SmallIntegerField(choices=Bool_CHOICES,blank=True, null=True)
    is_subject_based_registration = models.SmallIntegerField(choices=Bool_CHOICES,blank=True, null=True)
    elective_min_score = models.IntegerField(default=0)
    elective_max_score = models.IntegerField(default=0)
    is_include_additional_details = models.SmallIntegerField(choices=Bool_CHOICES,blank=True, null=True)
    additional_fields_array_ids = models.CharField(max_length=255,blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    active = models.SmallIntegerField(choices=Bool_CHOICES, default=1)
    status_idf = models.ForeignKey('GSettingStatus', on_delete=models.CASCADE,null=True)
    ip_address = models.CharField(blank=True, max_length=255, null=True)


    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_registration_grades_user')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_registration_grades_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'general_settings'

class Grade_Programme(models.Model):
    Gender_CHOICES = (
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Both', 'Both')
    )
    reg_grade_id = models.ForeignKey(Registration_Grade,on_delete=models.DO_NOTHING)
    programme_id = models.ForeignKey(Programme,on_delete=models.DO_NOTHING)
    # grade_programme_name = models.CharField(max_length=255,null=True,blank=True)
    gender = models.CharField(choices=Gender_CHOICES,blank=True, null=True)
    is_active = models.IntegerField(default=0,null=True,blank=True)
    notes = models.TextField(null=True, blank=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_grade_pro_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_grade_pro_user',default=1)

    class Meta:
        app_label = 'general_settings'

class Reg_Grade_Academic_Years(models.Model):
    reg_grade_id = models.ForeignKey(Registration_Grade,on_delete=models.DO_NOTHING)
    academic_year_id = models.ForeignKey('academic.Academic_Years',on_delete=models.DO_NOTHING)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_reg_grade_academic_years_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_reg_grade_academic_years_user',default=1)

    class Meta:
        app_label = 'general_settings'





class National_Setting(models.Model):
    is_numeric = models.IntegerField(default=0)
    length = models.IntegerField()

    class Meta:
        app_label = 'general_settings'


# ========================================= amr tables -tables related to finance- ========================================= #


class GSettingStatus(models.Model):
    Bool_CHOICES = (
        (1, 1),
        (0, 0)
    )
    school_id = models.ForeignKey(Schools, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name_lng1 = models.CharField(max_length=100)
    name_lng2 = models.CharField(max_length=100)
    notes = models.TextField()
    active = models.SmallIntegerField(choices=Bool_CHOICES)
    status_idf = models.ForeignKey('GSettingStatus', on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='created_gsettingstatus_user', default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='updated_gsettingstatus_user', default=1)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'general_settings'
        db_table = 'general_settings_status'


class StudentCategories(models.Model):
    Bool_CHOICES = (
        (1, 1),
        (0, 0)
    )
    school_id = models.ForeignKey(Schools, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name_lng1 = models.CharField(max_length=100)
    name_lng2 = models.CharField(max_length=100)
    notes = models.TextField()
    active = models.SmallIntegerField(choices=Bool_CHOICES)
    status_idf = models.ForeignKey(GSettingStatus, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='created_student_categories_user', default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='updated_student_categories_user', default=1)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'general_settings'
        db_table = 'general_settings_student_categories'


class ReceiverTypes(models.Model):
    Bool_CHOICES = (
        (1, 1),
        (0, 0)
    )
    school_id = models.ForeignKey(Schools, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name_lng1 = models.CharField(max_length=100)
    name_lng2 = models.CharField(max_length=100)
    notes = models.TextField()
    active = models.SmallIntegerField(choices=Bool_CHOICES)
    status_idf = models.ForeignKey(GSettingStatus, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='created_receiver_types_user', default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='updated_receiver_types_user', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'general_settings'
        db_table = 'general_settings_receiver_types'


class StakeholdersTypes(models.Model):
    Bool_CHOICES = (
        (1, 1),
        (0, 0)
    )
    school_id = models.ForeignKey(Schools, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name_lng1 = models.CharField(max_length=100)
    name_lng2 = models.CharField(max_length=100)
    notes = models.TextField()
    active = models.SmallIntegerField(choices=Bool_CHOICES)
    status_idf = models.ForeignKey(GSettingStatus, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='created_stakeholders_types_user', default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='updated_stakeholders_types_user', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'general_settings'
        db_table = 'general_settings_stakeholders_types'


class AttachmentFileTypes(models.Model):
    Bool_CHOICES = (
        (1, 1),
        (0, 0)
    )
    school_id = models.ForeignKey(Schools, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name_lng1 = models.CharField(max_length=100)
    name_lng2 = models.CharField(max_length=100)
    notes = models.TextField()
    active = models.SmallIntegerField(choices=Bool_CHOICES)
    status_idf = models.ForeignKey(GSettingStatus, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='created_attachment_file_types_user', default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='updated_attachment_file_types_user', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'finance'
        db_table = 'general_settings_attachment_file_types'
