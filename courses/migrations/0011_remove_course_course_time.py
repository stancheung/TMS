# Generated by Django 4.2.11 on 2024-07-15 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_course_course_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_time',
        ),
    ]