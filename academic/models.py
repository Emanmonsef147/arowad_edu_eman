from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from general_settings.models import GSettingStatus
# Create your models here.
class Year(models.Model):
    year = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    status_idf = models.ForeignKey(GSettingStatus, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='created_year_user',default=1)
    updated_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='updated_year_user',default=1)
    class Meta:
        app_label = 'academic'



class Semester(models.Model):
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
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52'),
        ('53', '53'),
        ('54', '54'),
        ('55', '55'),
        ('56', '56'),
        ('57', '57'),
        ('58', '58'),
        ('59', '59'),
        ('60', '60'),

    )
    semester_name_lng1 = models.CharField(max_length=255,null=True,blank=True)
    semester_name_lng2 = models.CharField(max_length=255, null=True, blank=True)
    no_of_quarters = models.IntegerField(blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    admission_on = models.IntegerField(default=0, blank=True, null=True)
    is_default = models.IntegerField(default=0, blank=True, null=True)
    edit_std_status = models.IntegerField(default=0,blank=True, null=True)
    grade_edit = models.IntegerField(default=0,blank=True, null=True)
    week_plan = models.IntegerField(default=0,blank=True, null=True)
    ignore_weekly_pal_dates = models.IntegerField(default=0, blank=True, null=True)
    allow_add_material_cover = models.IntegerField(default=0, blank=True, null=True)
    job_applicant_on = models.IntegerField(default=0, blank=True, null=True)
    allow_to_create_weekly_plan = models.IntegerField(choices=CHOICES,blank=True, null=True)
    allow_to_view_weekly_plan = models.IntegerField(choices=CHOICES,blank=True, null=True)
    # academic_year_semester_id = models.ForeignKey(Academic_Year_Semesters,on_delete=models.DO_NOTHING)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    status_idf = models.ForeignKey(GSettingStatus, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_semester_name_user', default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_semester_name_user', default=1)

    class Meta:
        app_label = 'academic'

class Academic_Years(models.Model):

    year_id = models.ForeignKey(Year, on_delete=models.DO_NOTHING)
    # semester_id = models.ForeignKey(Academic_Year_Semesters, on_delete=models.DO_NOTHING,null=True,blank=True)
    # no_of_semester = models.IntegerField(blank=True,null=True)
    # semester_name = models.CharField(max_length=255, blank=True, null=True)
    year_name_g = models.CharField(max_length=255,blank=True, null=True)
    year_name_h= models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    finance_year_name = models.CharField(max_length=255, blank=True, null=True)
    finance_start_date = models.DateField(blank=True, null=True)
    finance_end_date = models.DateField(blank=True, null=True)
    number_of_weeks = models.IntegerField(blank=True, null=True)
    # admission_on = models.IntegerField(default=0, blank=True, null=True)
    # is_default = models.IntegerField(default=0, blank=True, null=True)
    # edit_std_status = models.IntegerField(default=0,blank=True, null=True)
    # grade_edit = models.IntegerField(default=0,blank=True, null=True)
    # week_plan = models.IntegerField(default=0,blank=True, null=True)
    # ignore_weekly_pal_dates = models.IntegerField(default=0, blank=True, null=True)
    # allow_add_material_cover = models.IntegerField(default=0, blank=True, null=True)
    # job_applicant_on = models.IntegerField(default=0, blank=True, null=True)
    # allow_to_create_weekly_plan = models.IntegerField(choices=CHOICES,blank=True, null=True)
    # allow_to_view_weekly_plan = models.IntegerField(choices=CHOICES,blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    status_idf = models.ForeignKey(GSettingStatus, on_delete=models.CASCADE, default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_academic_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_academic_user',default=1)

    class Meta:
        app_label = 'academic'


class Academic_Year_Semester(models.Model):
    academic_year_id = models.ForeignKey(Academic_Years, on_delete=models.DO_NOTHING)
    # year_id = models.ForeignKey(Year, on_delete=models.DO_NOTHING)
    semster_id  = models.ForeignKey(Semester, on_delete=models.DO_NOTHING)
    status_idf = models.ForeignKey(GSettingStatus, on_delete=models.CASCADE, default=1)
    notes = models.TextField(null=True, blank=True)
    active = models.IntegerField(default=1)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_semester_user',default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_semester_user',default=1)

    class Meta:
        app_label = 'academic'