from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView
from .forms import StudentsCreationForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Student
from tools import is_ajax, decodeRequest, model_to_dict_verbose
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

def CreateStudents(request):
    if request.method == 'POST':
        form = StudentsCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student profile created successfully.')
            return redirect('Homepage')
    else:
        form = StudentsCreationForm()
    context = {'form': form}
    return render(request, 'students/create-students.html', context)

class StudentProfileView(LoginRequiredMixin, View):
    template_name = "students/search-students.html"

    def get(self, request):
        print("get")
        return render(request, template_name = self.template_name, context={})

    def post(self, request):
        if is_ajax(request):
            print("ajax post")
            phone_num = None
            requestBody = decodeRequest(request)
            if requestBody:
                phone_num = requestBody.get('input')
            context = {}
                
            try:
                student_obj = Student.objects.get(studentContactNumber=phone_num)
                #enrolled_classes = Enrollment.objects.filter(student_id = student_obj)
                context = model_to_dict_verbose(student_obj)
                print(context)
            except Student.DoesNotExist:
                not_found_message = "Student profile not found."
                context = {'not_found_message': not_found_message}
            return JsonResponse(context)

class StudentProfileUpdateView(UpdateView):
    model = Student
    fields = '__all__'
    success_url = '/student-profile/search/'
    template_name = 'students/student-profile.html'

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)

class StudentProfileDeleteView(DeleteView):
    model = Student
    success_url = '/student-profile/search/'
    template_name = 'students/delete-student.html'
