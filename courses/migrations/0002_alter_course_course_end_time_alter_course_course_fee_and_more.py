# Generated by Django 4.2.11 on 2024-03-24 14:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]