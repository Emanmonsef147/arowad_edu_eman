
from django.contrib.auth.models import User
from countries.models import *
from general_settings.models import *

# Create your models here.


# def connect_signals_for_user_tracking(model_class):
#     @receiver(pre_save, sender=model_class)
#     def set_updated_by(sender, instance, **kwargs):
#         if instance.pk:
#             instance.updated_by = instance.request.user
#
#     @receiver(post_save, sender=model_class)
#     def set_created_by(sender, instance, created, **kwargs):
#         if created:
#             instance.created_by = instance.request.user

class Status(models.Model):
    name_lng1 = models.CharField(max_length=255,null=True,blank=True)
    name_lng2 = models.CharField(max_length=255, null=True, blank=True)
    category_lng1 = models.CharField(max_length=255,null=True,blank=True)
    category_lng2 = models.CharField(max_length=255, null=True, blank=True)
    status_order_by = models.IntegerField(unique=True,default=0)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_status_user', blank=False, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_status_user', blank=False, null=False)


    class Meta:
        app_label = 'student'

class Guardian(models.Model):
    pass


class Student(models.Model):
    pass

class Employee(models.Model):
    pass


class Applicant(models.Model):
    GENDER_CHOICES = (
        ('Female', 'Female'),
        ('Male', 'Male'),)
    applicant_no = models.CharField(max_length=255, blank=True, null=True)
    first_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    second_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    third_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    last_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    first_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    second_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    third_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    last_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField()
    address_line = models.CharField(max_length=255, blank=True, null=True)
    phone1 = models.CharField(max_length=255, blank=True, null=True)
    phone2 = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True)
    religion_id = models.ForeignKey('countries.RELIGION', db_constraint=False, db_column='religion_id',
                                on_delete=models.DO_NOTHING, blank=True, null=True)
    language_id = models.ForeignKey('countries.Langs', db_constraint=False, db_column='language_id',
                      on_delete=models.DO_NOTHING, blank=True, null=True)
    iqama_id= models.CharField(max_length=255, blank=True, null=True)
    iqama_source= models.CharField(max_length=255, blank=True, null=True)
    iqama_source_date = models.DateField()
    parent_iqama_id = models.CharField(max_length=255, blank=True, null=True)
    parent_iqama_source = models.CharField(max_length=255, blank=True, null=True)
    parent_iqama_source_date = models.DateField()
    passport_id = models.CharField(max_length=255, blank=True, null=True)
    passport_expiry_date = models.DateField(default=datetime.now)
    passport_country = models.ForeignKey('countries.Country', db_constraint=False,
                                         db_column='passport_country_id',
                                         on_delete=models.DO_NOTHING, blank=True, null=True,
                                         related_name='passport_country_applicants')
    city_id = models.ForeignKey('countries.Cities',db_constraint=False,db_column='city_id', on_delete=models.DO_NOTHING,blank=True, null=True)
    state_id = models.ForeignKey('countries.State', db_constraint=False, db_column='state_id',on_delete=models.DO_NOTHING, blank=True, null=True)
    country_id = models.ForeignKey('countries.Country',db_constraint=False,db_column='country_id', on_delete=models.DO_NOTHING,blank=True, null=True,related_name='country_applicants')
    nationality_id = models.ForeignKey('countries.Country', db_constraint=False, db_column='nationality_id',on_delete=models.DO_NOTHING,related_name='nationality_applicants', blank=True, null=True)
    birth_country = models.ForeignKey('countries.Country', db_constraint=False, db_column='birth_country',
                                   on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='bitrh_country_applicants')

    status_id = models.ForeignKey(Status, to_field='status_order_by',null=True,blank=True, on_delete=models.DO_NOTHING,related_name='applicant_status_id')
    has_paid = models.IntegerField(default=0,blank=True, null=True)
    print_token = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField(default=0.00,null=True,blank=True)
    have_siblling = models.IntegerField(default=0,null=True,blank=True)
    employee_id_name = models.CharField(max_length=255,null=True,blank=True)
    #sibling_id = models.ForeignKey(Guardian,blank=True, null=True, on_delete=models.DO_NOTHING,db_column='sibling_id',related_name='applicant_sibling')
    # student_id = models.ForeignKey(Student,blank=True, null=True, on_delete=models.DO_NOTHING)
    # employee_id = models.ForeignKey(Employee,blank=True, null=True, on_delete=models.DO_NOTHING)
    # parent_id = models.ForeignKey(Guardian,blank=True, null=True, on_delete=models.DO_NOTHING,db_column='parent_id',related_name='applicant_guardian')
    programme_id = models.ForeignKey('general_settings.Grade_Programme',blank=True, null=True, on_delete=models.DO_NOTHING)
    reg_grade_id = models.ForeignKey('general_settings.Registration_Grade', on_delete=models.DO_NOTHING)
    acadmic_year_id = models.ForeignKey('academic.Academic_Years',on_delete=models.DO_NOTHING,blank=True,null=True)
    # semster_id = models.ForeignKey('academic.Academic_Year_Semesters',on_delete=models.DO_NOTHING,blank=True,null=True)
    is_user = models.IntegerField(default=0)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_applicant_user', blank=False, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_applicant_user', blank=False, null=False)

    class Meta:
        app_label = 'student'


class ApplicantDocumentType(models.Model):
    DOC_TYPES = (
        ('PDF', 'PDF'),
        ('Image', 'Image')
    )
    doc_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    doc_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    doc_desc_lng1 = models.TextField(blank=True, null=True)
    doc_desc_lng2 = models.TextField(blank=True, null=True)
    is_necessary = models.IntegerField(default=0)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, default='Other')
    school_id = models.ForeignKey(Schools, on_delete=models.DO_NOTHING, related_name='applicant_document_type_school_id')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='applicant_document_type_created_by', blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='applicant_document_type_updated_by', blank=False, null=False)

    class Meta:
        app_label = 'student'
        db_table = 'student_applicant_document_type'



class ApplicantDocumentAttachment(models.Model):
    applicant_id = models.ForeignKey(Applicant, on_delete=models.DO_NOTHING)
    applicant_document_types_id = models.ForeignKey('ApplicantDocumentType', on_delete=models.DO_NOTHING)
    attachment_file = models.FileField(upload_to='files/applicant', blank=True, null=True)
    school_id = models.ForeignKey(Schools, on_delete=models.DO_NOTHING,
                                  related_name='applicant_document_attachment_school_id',default=1)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='applicant_document_attachment_created_by', blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   related_name='applicant_document_attachment_updated_by', blank=False, null=False)

    class Meta:
        app_label = 'student'
        db_table = 'student_applicant_document_attachment'



# class imageApplicant(models.Model):
#     applicant_id  = models.ForeignKey(Applicant,on_delete=models.DO_NOTHING)
#     photo = models.FileField(null=True, blank=True,upload_to='files/applicant')
#     notes = models.TextField(null=True, blank=True)
#     active = models.IntegerField(default=1)
#     ip_address = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(default=datetime.now)
#     updated_at = models.DateTimeField(default=datetime.now)
#     created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_img_applicant_user', blank=False, null=False)
#     updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_img_applicant_user', blank=False, null=False)
#
#     class Meta:
#         app_label = 'student'

class ApplicantPreviousSchoolData(models.Model):
    applicant_id = models.ForeignKey(Applicant,on_delete=models.DO_NOTHING)
    last_attended_school_lng1 = models.CharField(max_length=255, blank=True, null=True)
    last_attended_school_lng2 = models.CharField(max_length=255, blank=True, null=True)
    last_score = models.CharField(max_length=255, blank=True, null=True)
    evaluvation = models.CharField(max_length=255, blank=True, null=True)
    last_grade_id = models.ForeignKey('general_settings.Grade',on_delete=models.DO_NOTHING,null=True,blank=True)
    last_year_id =models.ForeignKey('academic.Year',on_delete=models.DO_NOTHING,null=True,blank=True)
    last_country_id = models.ForeignKey('countries.Country', db_constraint=False, db_column='last_country_id',
                                   on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='last_country_school')
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_pervious_school_user', blank=False, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_pervious_school_user', blank=False, null=False)

    class Meta:
        app_label = 'student'
        db_table = 'student_applicant_previous_school_data'


class Applicant_Guardians(models.Model):
    RELATION_CHOICES = (
        ('Mother', 'Mother'),
        ('Father', 'Father'),
        ('Brother', 'Brother'),
        ('Sister','Sister'),
        ('Uncle','Uncle'),
        ('Aunt','Aunt'),
        ('GrandFather','GrandFather'),
        ('GrandMother','GrandMother'),
        ('Others', 'Others')
    )
    EDU_CHOICES = (
        ('PhD','PhD'),
        ('Master','Master'),
        ('Bachelor','Bachelor'),
        ('High School','High School'),
        ('None','None')
    )
    applicant_id = models.ForeignKey(Applicant, on_delete=models.DO_NOTHING)
    first_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    second_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    third_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    last_name_lng1 = models.CharField(max_length=255, blank=True, null=True)
    first_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    second_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    third_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    last_name_lng2 = models.CharField(max_length=255, blank=True, null=True)
    iqama_id = models.CharField(max_length=255, blank=True, null=True)
    iqama_source = models.CharField(max_length=255, blank=True, null=True)
    iqama_source_date = models.DateField()
    passport_id = models.CharField(max_length=255, blank=True, null=True)
    passport_expiry_date = models.DateField(default=datetime.now)
    passport_country = models.ForeignKey('countries.Country', db_constraint=False,
                                         db_column='passport_country_id',
                                         on_delete=models.DO_NOTHING, blank=True, null=True,
                                         related_name='passport_country_applicant_guardian')
    _relation = models.CharField(choices=RELATION_CHOICES, blank=True, null=True)
    religion_id = models.ForeignKey('countries.RELIGION', db_constraint=False, db_column='religion_id',
                                    on_delete=models.DO_NOTHING, blank=True, null=True)
    # religion = models.CharField(choices=RELIGION_CHOICES, blank=True, null=True)
    language_id = models.ForeignKey('countries.Langs', db_constraint=False, db_column='language_id',
                                    on_delete=models.DO_NOTHING, blank=True, null=True)
    date_of_birth = models.DateField()
    education = models.CharField(choices=EDU_CHOICES, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    address_line = models.CharField(max_length=255, blank=True, null=True)

    email = models.CharField(max_length=255, blank=True, null=True)
    nationality_id = models.ForeignKey('countries.Country', db_constraint=False, db_column='nationality_id',on_delete=models.DO_NOTHING,related_name='nationality_gur_applicant', blank=True, null=True)
    country_id = models.ForeignKey('countries.Country', db_constraint=False, db_column='country_id',
                                   on_delete=models.DO_NOTHING, blank=True, null=True)
    state_id = models.ForeignKey('countries.State', db_constraint=False, db_column='state_id',
                                 on_delete=models.DO_NOTHING, blank=True, null=True)
    city_id = models.ForeignKey('countries.Cities', db_constraint=False, db_column='city_id',
                                on_delete=models.DO_NOTHING, blank=True, null=True)
    mobile_phone = models.CharField(max_length=255, blank=True, null=True)
    mother_phone = models.CharField(max_length=255, blank=True, null=True)
    emergency_phone = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_applicant_gur_user', blank=False, null=False)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_applicant_gur_user', blank=False, null=False)

    class Meta:
        app_label = 'student'