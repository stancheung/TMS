from django.contrib import admin
from .models import Course, Enrollment

class coursesAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_date', 'course_time', 'course_fee')

    def course_date(self, obj):
        return f"{obj.course_date}"

    def course_time(self, obj):
        return f"{obj.course_start.strftime("%H:%M")} - {obj.course_end.strftime("%H:%M")}"

admin.site.register(Course, coursesAdmin)
admin.site.register(Enrollment)