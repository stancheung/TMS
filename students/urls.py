from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.StudentProfileView.as_view(), name="SearchStudents"),
    path("update/<pk>/", views.StudentProfileUpdateView.as_view(), name="UpdateStudentProfile")
]
