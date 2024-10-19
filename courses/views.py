import json
from datetime import datetime
from django.views import View
from django.views.generic import CreateView, DeleteView
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from courses.models import Course, Enrollment, Student
from students.views import is_ajax
from .forms import CourseCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from tools import DateEncoder, is_ajax, decodeRequest

class TimetableView(LoginRequiredMixin, View):
    template_name = 'courses/timetableTest.html'
    def get(self, request):
        # if is_ajax(request):
        #     return self.showAllEnrollments(request)   
        return self.showTimetable(request)
    
    def post(self, request):
        if is_ajax(request):
            requestBody = decodeRequest(request)
            if requestBody and not requestBody.get('phoneNum'):
                return self.showAllEnrollments(requestBody)
            return self.createEnrollment(requestBody)
        return self.showTimetable(request)

    def showTimetable(self, request):
        event_arr = []
        all_courses = Course.objects.all()
        for i in all_courses:
            event_dict = {}
            event_dict['id'] = i.pk
            event_dict['title'] = i.course_title
            event_dict['start'] = datetime.combine(i.course_date, i.course_start)
            event_dict['end'] = datetime.combine(i.course_date, i.course_end)
            # event_dict['extendedProps'] = {'sessionNumber': i.session_number}
            event_arr.append(event_dict)
        events_dataset = json.dumps(event_arr, cls=DateEncoder)
        context = {
            'events': events_dataset,
        }
        return render(request, self.template_name, context)
    
    def showAllEnrollments(self, requestBody):
        courseID = requestBody.get('classID')
        enrollments = Enrollment.objects.filter(course_id=courseID)
        enroll_arr = []

        for e in enrollments:
            enroll_obj = model_to_dict(e)
            student_obj = Student.objects.filter(pk=enroll_obj['student_id']).first()
            enrollment_pk = e.pk
            phone_num = getattr(student_obj, 'studentContactNumber')
            student_name = f'{getattr(student_obj, 'studentFirstName')} {getattr(student_obj, 'studentLastName')}'
            enroll_obj['enrollment_pk'] = enrollment_pk
            enroll_obj['student_name'] = student_name
            enroll_obj['phone_num'] = phone_num
            enroll_arr.append(enroll_obj)

        return JsonResponse(enroll_arr, safe=False)

    def createEnrollment(self, requestBody):
            phoneNum = requestBody.get('phoneNum')
            courseID = requestBody.get('classID')

            res = {}

            if len(phoneNum) != 8 or not phoneNum.isnumeric():
                res = {'enroll_response': 'Phone number can only be 8 digits.'}
                return res
            
            try:
                student_id = Student.objects.filter(studentContactNumber = phoneNum).first()
                course_id = Course.objects.filter(id=courseID).first()
                Enrollment.objects.get(student_id = student_id, course_id = course_id)
                res = {'enroll_response': 'Enrollment already exists.'}

            except Enrollment.DoesNotExist:
                course = Course.objects.filter(id=courseID).first()
                student = Student.objects.filter(studentContactNumber = phoneNum).first()

                if not student:
                    res = {'enroll_response': 'Student does not exist.'}
                    return res
                
                newEnrollment = Enrollment(
                    student_id = student,
                    course_id = course,
                )

                newEnrollment.save()
                res = {'enroll_response': 'Student added to class successfully.'}
            return JsonResponse(res) 
    
class ClassCreateView(CreateView):
    model = Course
    success_url = '/'
    form_class = CourseCreateForm

class ClassDeleteView(DeleteView):
    model = Course
    success_url = '/'
    template_name = 'courses/delete-class.html'

class EnrollmentDeleteView(DeleteView):
    model = Enrollment
    success_url = '/'
    template_name = 'courses/delete-enrollment.html'
