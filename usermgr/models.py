from django.db import models
from datetime import datetime
# Create your models here.
from django.contrib.auth.models import User
from general_settings.models import Schools
class Private_Url(models.Model):
    url = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255, default='127.0.0.1')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_private_url_user',
                                   default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_private_url_user',
                                   default=1)


    class Meta:
        app_label = 'usermgr'


class Public_Url(models.Model):
    url = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255, default='127.0.0.1')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_public_url_user',
                                   default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_public_url_user',
                                   default=1)

    class Meta:
        app_label = 'usermgr'


class User_urls(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    url_id = models.IntegerField()

    class Meta:
        app_label = 'usermgr'



class User_Type(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=255, choices=(('superadmin', 'superadmin'),
                                                          ('admin', 'admin'),
                                                          ('hr', 'hr'),
                                                          ('employee', 'employee'),
                                                          ('teacher', 'teacher'),
                                                          ('guardian', 'guardian'),
                                                          ('student', 'student'),))
    ip_address = models.CharField(max_length=255, default='127.0.0.1')
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='created_user_type',
                                   default=1)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='updated_user_type',
                                   default=1)

    class Meta:
        app_label = 'usermgr'


class User_Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # f_name=models.CharField(max_length=255, blank=True)
    # l_name=models.CharField(max_length=255, blank=True)
    fullname = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255, blank=True)
    birth = models.DateField(default=datetime.now)
    userimg = models.ImageField(null=True, blank=True, upload_to='files/user', default='files/user/default.jpg')
    date_joined = models.DateTimeField(blank=True, default=datetime.now)
    perm_one = models.BooleanField(default=False)
    perm_two = models.BooleanField(default=False)
    perm_tri = models.BooleanField(default=False)
    perm_quad = models.BooleanField(default=False)
    perm_pent = models.BooleanField(default=False)
    perm_hex = models.BooleanField(default=False)
    admin_msg = models.TextField()
    nat_id = models.CharField(max_length=14, blank=True,null=True,default='000')

    class Meta:
        app_label = 'usermgr'


class Reset_password(models.Model):
    link = models.CharField(max_length=255, db_index=True)
    last_forget = models.DateTimeField(default=datetime.now)

    class Meta:
        app_label = 'usermgr'


class Forget_time(models.Model):
    email = models.CharField(max_length=255)
    last_demand = models.DateTimeField(default=datetime.now)

    class Meta:
        app_label = 'usermgr'



class Types_Urls(models.Model):
    type = models.CharField(max_length=255)
    url_id = models.IntegerField(default=1)

    class Meta:
        app_label = 'usermgr'


class UserAdditionalFields(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='useradditionalfields')
    school_id = models.ForeignKey(Schools, on_delete=models.DO_NOTHING, default=1)

    class Meta:
        app_label = 'usermgr'
        db_table = 'user_additional_fields'