# Generated by Django 4.2.11 on 2024-03-24 14:19

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('students', '0004_alter_student_emergencycontactname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_title', models.CharField(max_length=20)),
                ('course_date', models.DateField(default=datetime.datetime.today)),
                ('course_start_time', models.CharField(default='', max_length=4, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_time', message='Time can only be 4 digits.', regex='^[0-9]+$')])),
                ('course_end_time', models.CharField(default='', max_length=4, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_time', message='Time can only be 4 digits.', regex='^[0-9]+$')])),
                ('course_fee', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enroll_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.student')),
            ],
        ),
    ]
