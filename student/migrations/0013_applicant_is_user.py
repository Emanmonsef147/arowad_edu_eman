# Generated by Django 5.0.4 on 2024-06-01 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_applicant_status_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='is_user',
            field=models.IntegerField(default=0),
        ),
    ]
