from django.contrib import admin
from .models import Student, LessonPlan
from django.contrib.auth.admin import UserAdmin

class studentsAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'studentGender', 'studentContactNumber')

    def student_name(self, obj):
        return f"{obj.studentFirstName} {obj.studentLastName}"

admin.site.register(Student, studentsAdmin)
admin.site.register(LessonPlan)
