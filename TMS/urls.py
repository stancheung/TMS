from re import template
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import courses
from users import views as users_views
from students import views as students_views
from courses import views as courses_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",auth_views.LoginView.as_view(template_name="users/login.html", redirect_authenticated_user=True),name="Login"),
    path("logout/",auth_views.LogoutView.as_view(template_name="users/logout.html"),name="Logout"),
    path('home/', users_views.HomeView.as_view(template_name='users/home.html'), name='Homepage'),
    path('delete-class/<int:pk>', courses_views.ClassDeleteView.as_view(), name='DeleteClass'),
    path("create-students/", students_views.CreateStudents, name="CreateStudents"),
    path("student-profile/", include("students.urls")),
    path('timetable/', courses_views.TimetableView.as_view(), name='Timetable'),
    path("new-class/",courses_views.ClassCreateView.as_view(template_name="courses/create-class.html"),name="CreateClass"),
    path("enrollment/delete/<int:pk>", courses_views.EnrollmentDeleteView.as_view(), name="DeleteEnrollment"),
    path("attendance/<pk>", courses_views.ClassAttendanceView.as_view(template_name="courses/attendance.html"), name="Attendance")
]
