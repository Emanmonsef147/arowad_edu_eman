# Generated by Django 5.0.4 on 2024-06-11 13:39

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0003_rename_semester_id_semester_academic_year_semester_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='academic_year_semester_id',
        ),
        migrations.RemoveField(
            model_name='academic_years',
            name='no_of_semester',
        ),
        migrations.RemoveField(
            model_name='academic_years',
            name='semester_name',
        ),
        migrations.AddField(
            model_name='semester',
            name='no_of_quarters',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Academic_Year_Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('active', models.IntegerField(default=1)),
                ('ip_address', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('academic_year_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='academic.academic_years')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_semester_user', to=settings.AUTH_USER_MODEL)),
                ('semster_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='academic.semester')),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_semester_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Academic_Year_Semesters',
        ),
    ]
