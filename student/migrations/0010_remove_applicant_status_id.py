# Generated by Django 5.0.4 on 2024-05-28 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_rename_applicant_previous_school_data_applicantpreviousschooldata_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='status_id',
        ),
    ]
