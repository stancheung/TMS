# Generated by Django 4.2.11 on 2024-04-14 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_course_course_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='session_number',
            field=models.IntegerField(default=1),
        ),
    ]