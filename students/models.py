import datetime
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    studentFirstName = models.CharField('First Name', max_length = 20)

    studentLastName = models.CharField('Last Name', max_length = 20)

    studentGender = models.CharField('Gender', max_length = 1, choices = GENDER_CHOICES)

    studentDOB = models.DateField('Date of Birth', default=datetime.date.today)

    studentContactNumber = models.CharField(
        'Contact Number', 
        max_length=8, 
        validators=[RegexValidator(regex=r'^[0-9]+$', message='Phone number must contain only digits.', code='invalid_phone_number')],
        unique=True,
        default=''
    )

    emergencyContactName = models.CharField('Emergency Contact Name', max_length = 20)

    emergencyContactNumber = models.CharField(
        'Emergency Contact Number', 
        max_length=8, 
        validators=[RegexValidator(regex=r'^[0-9]+$', message='Phone number must contain only digits.', code='invalid_phone_number')],
        unique=True,
        default=''
    )

    def __str__(self):
        return f"{self.studentFirstName} {self.studentLastName}"

class LessonPlan(models.Model):
    PLAN_CHOICES = (
        ('8', '8 Lessons'),
        ('4', '4 Lessons'),
        ('1', '1 Lesson')
    )

    lessonPlan = models.CharField('Lesson Plan', max_length = 1, choices = PLAN_CHOICES)
    remainingLessons = models.IntegerField(default = 0)
    planOwner = models.ForeignKey(Student, on_delete = models.CASCADE)

    def save(self, *args, **kwargs):
        print(self.lessonPlan)
        
        if self.lessonPlan == "8":
            self.remainingLessons = 8

        super().save(*args, **kwargs)
