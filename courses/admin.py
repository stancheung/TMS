from django.contrib import admin
from .models import Course, Enrollment, RegularClass

class coursesAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_date', 'course_time', 'course_fee')

    def course_date(self, obj):
        return f"{obj.course_date}"

    def course_time(self, obj):
        return f"{obj.course_start.strftime("%H:%M")} - {obj.course_end.strftime("%H:%M")}"

class regClassesAdmin(admin.ModelAdmin):
    list_display = ('regClass_title', 'regClass_date', 'regClass_time', 'regClass_fee')

    def regClass_date(self, obj):
        return f"{obj.regClass_date}"

    def regClass_time(self, obj):
        return f"{obj.regClass_start.strftime("%H:%M")} - {obj.regClass_end.strftime("%H:%M")}"

admin.site.register(Course, coursesAdmin)
admin.site.register(Enrollment)
admin.site.register(RegularClass, regClassesAdmin)
