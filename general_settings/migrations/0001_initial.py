# Generated by Django 5.0.4 on 2024-04-23 10:14

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Finance_Fee_Collections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Grade_Type_System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='National_Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_numeric', models.IntegerField(default=0)),
                ('length', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_name_lng1', models.CharField(blank=True, max_length=255, null=True)),
                ('grade_name_lng2', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('grade_order', models.IntegerField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20')], null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_grade_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_grade_user', to=settings.AUTH_USER_MODEL)),
                ('grading_type_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.grade_type_system')),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme_name_lng1', models.CharField(blank=True, max_length=255, null=True)),
                ('programme_name_lng2', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_programme_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_programme_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration_Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_score', models.IntegerField(default=0)),
                ('is_active', models.IntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('subject_based_fee_collection', models.IntegerField(blank=True, null=True)),
                ('enable_approval_system', models.IntegerField(default=0)),
                ('min_electives', models.IntegerField(blank=True, null=True)),
                ('max_elective', models.IntegerField(blank=True, null=True)),
                ('is_subject_based_registration', models.IntegerField(default=0)),
                ('include_additional_details', models.IntegerField(blank=True, null=True)),
                ('additional_field_ids', models.CharField(blank=True, max_length=255, null=True)),
                ('age_limit_g', models.DateField(default='1998-01-01')),
                ('age_limit_h', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_reg_grade_user', to=settings.AUTH_USER_MODEL)),
                ('grade_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.grade')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_reg_grade_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reg_Grade_Academic_Years',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('academic_year_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='academic.academic_years')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_reg_grade_academic_years_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_reg_grade_academic_years_user', to=settings.AUTH_USER_MODEL)),
                ('reg_grade_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.registration_grade')),
            ],
        ),
        migrations.CreateModel(
            name='Grade_Programme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('Female', 'Female'), ('Male', 'Male'), ('Both', 'Both')], null=True)),
                ('is_active', models.IntegerField(blank=True, default=0, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_grade_pro_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_grade_pro_user', to=settings.AUTH_USER_MODEL)),
                ('programme_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.programme')),
                ('reg_grade_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.registration_grade')),
            ],
        ),
        migrations.CreateModel(
            name='Schools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_lng1', models.CharField(max_length=255)),
                ('name_lng2', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('last_seeded_at', models.DateField(auto_now_add=True)),
                ('is_deleted', models.IntegerField(default=1)),
                ('notes', models.TextField(blank=True, default='notes', null=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_school_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_school_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(auto_now_add=True)),
                ('is_common', models.IntegerField(default=1)),
                ('is_holiday', models.IntegerField(default=1)),
                ('is_exam', models.IntegerField(default=1)),
                ('is_due', models.IntegerField(default=1)),
                ('finance_fee_collections_type', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, default='notes', null=True)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_event_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_event_user', to=settings.AUTH_USER_MODEL)),
                ('finance_fee_collections_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.finance_fee_collections')),
                ('school_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.schools')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_lng1', models.CharField(blank=True, max_length=255, null=True)),
                ('name_lng2', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_stage_user', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_stage_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='grade',
            name='stage_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.stage'),
        ),
        migrations.CreateModel(
            name='Stu_Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_class_user', to=settings.AUTH_USER_MODEL)),
                ('grade_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.grade')),
                ('programme_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.programme')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_class_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stu_Intial_Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('acadmic_year_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='academic.academic_years')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_intial_class_user', to=settings.AUTH_USER_MODEL)),
                ('grade_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.grade')),
                ('programme_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='general_settings.programme')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_intial_class_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
