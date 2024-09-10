# Generated by Django 5.0.4 on 2024-06-13 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_applicant_is_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='status',
            old_name='category',
            new_name='category_lng1',
        ),
        migrations.RenameField(
            model_name='status',
            old_name='name',
            new_name='category_lng2',
        ),
        migrations.AddField(
            model_name='status',
            name='name_lng1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='status',
            name='name_lng2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
