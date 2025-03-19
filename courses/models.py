from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save
from students.models import Student
from datetime import datetime, timedelta
from django.utils import timezone

class Course(models.Model):

    COURSES_CHOICES = (
        ("Kids Parkour", "Kids Parkour"),
        ("Adults Parkour", "Adults Parkour")
    )

    #course_title = models.CharField(max_length=20)
    course_title = models.CharField('Class', max_length=20, choices = COURSES_CHOICES)
    course_date = models.DateField(default=datetime.now)
    course_start = models.TimeField(default=datetime.now)
    course_end = models.TimeField(default=datetime.now)
    course_fee = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.course_title} {self.course_date} {self.course_start.strftime("%H:%M")}-{self.course_end.strftime("%H:%M")}"

    def save(self, *args, **kwargs):
        self.course_start = self.course_start.replace(second=0)
        self.course_end = self.course_end.replace(second=0)
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     if self.course_start_time >= self.course_end_time:
    #         raise ValidationError("Course start time must be before course end time.")
    #     super().save(*args, **kwargs)

class Enrollment(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    enroll_date = models.DateTimeField(default=timezone.now)
    session_number = models.IntegerField(default=1, blank=True)
    payday = models.BooleanField(default=False)
    attendance = models.BooleanField(default=False)
    # session_number = models.IntegerField(default=1, blank=True)
    # first_session_pointer = models.IntegerField(null=True, blank=True)

class RegularClass(models.Model):
    RegularClass_CHOICES = (
        ("Kids Parkour", "Kids Parkour"),
        ("Adults Parkour", "Adults Parkour")
    )

    #course_title = models.CharField(max_length=20)
    regClass_title = models.CharField('Class', max_length=20, choices = RegularClass_CHOICES)
    regClass_date = models.DateField(default=datetime.now)
    regClass_start = models.TimeField(default=datetime.now)
    regClass_end = models.TimeField(default=datetime.now)
    regClass_fee = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.regClass_title} {self.regClass_date} {self.regClass_start.strftime("%H:%M")}-{self.regClass_end.strftime("%H:%M")}"

    def save(self, *args, **kwargs):
        self.regClass_start = self.regClass_start.replace(second=0)
        self.regClass_end = self.regClass_end.replace(second=0)
        super().save(*args, **kwargs)


'''
@receiver(post_save, sender=Enrollment)
def auto_create_enrollment(sender, instance, created, **kwargs):
    course = Course.objects.filter(course_date = instance.course_id.course_date + timedelta(days=7)).first()
    if instance.session_number != 4 and course:
        i = Enrollment(
            course_id = course,
            student_id = instance.student_id,
            enroll_date = instance.enroll_date,
            session_number = instance.session_number + 1,
            payday = instance.payday
        )

        if i.session_number == 3:
            i.payday = True
        else:
            i.payday = False

        i.save()
'''
# @receiver(post_save, sender=Enrollment)
# def auto_create_enrollment(sender, instance, **kwargs):
#     pass

# @receiver(post_save, sender=Course)
# def auto_create_class(sender, instance, created, **kwargs):

#     if created:
#         #define the last day of each month
#         loop_month_date = instance.course_start
#         month_end_date = loop_month_date.replace(day=1) + timedelta(days=32)
#         month_end_date = month_end_date.replace(day=1) - timedelta(days=1)

#         #assign the start date of the first created object to an individual variable
#         start_date = instance.course_start

#         #set class_date to 1 day ahead of the first manually created instance so it doesnt duplicate
#         loop_month_date = instance.course_start + timedelta(days=1)

#         while loop_month_date <= month_end_date:

#             if loop_month_date.strftime('%A') == instance.course_start.strftime('%A'):
#                 #add a week every time the condition and the if statement are fulfilled
#                 start_date += timedelta(days=7)
#                 #get the last object created
#                 last_obj_created = Course.objects.last()
#                 if last_obj_created.session_number == 1:
#                     last_obj_created.first_session_pointer = last_obj_created.pk
#                     last_obj_created.save()

#                 pointer = last_obj_created.first_session_pointer

#                 #make sure the updated start_date is larger than the last object created start_date before creating next object
#                 if last_obj_created.session_number == 4:
#                     break

#                 if start_date > last_obj_created.course_start:
#                     #print(start_date)
#                     i = Course(
#                         course_title=instance.course_title,
#                         course_start=instance.course_start + timedelta(days=7),
#                         course_end = instance.course_end + timedelta(days=7),
#                         course_fee = instance.course_fee,
#                         session_number = last_obj_created.session_number + 1,
#                         first_session_pointer = pointer
#                     )
#                     i.save()
#             loop_month_date += timedelta(days=1)
