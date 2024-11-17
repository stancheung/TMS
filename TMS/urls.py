"""
URL configuration for TMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
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
    path("class-details/<int:pk>",  courses_views.ClassAttendanceView.as_view(), name="ClassAttendance")
]

