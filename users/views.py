from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Enrollment, Course
import datetime
from tools import is_ajax, decodeRequest


class HomeView(LoginRequiredMixin, View):
    template_name = "users/home.html"

    def get(self, request):
        context = {}
        context["today_class_list"] = Course.objects.filter(course_date=datetime.date.today())
        context["payment_list"] = Enrollment.objects.filter(payday=True).filter(course_id__course_date=datetime.date.today())
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        if is_ajax(request):
            requestBody = decodeRequest(request)
            if requestBody:
                if not requestBody.get("phoneNum"):
                    return self.get(request)
        return self.get(request)
