# Generated by Django 4.2.11 on 2024-03-24 14:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_course_course_end_time_alter_course_course_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_end_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_start_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]