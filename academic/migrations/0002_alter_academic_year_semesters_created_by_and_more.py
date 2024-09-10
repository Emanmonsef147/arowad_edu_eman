# Generated by Django 5.0.4 on 2024-05-21 11:24

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='academic_year_semesters',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_semester_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='academic_year_semesters',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_semester_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester_name_lng1', models.CharField(blank=True, max_length=255, null=True)),
                ('semester_name_lng2', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_semester_name_user', to=settings.AUTH_USER_MODEL)),
                ('semester_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='academic.academic_year_semesters')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_semester_name_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
