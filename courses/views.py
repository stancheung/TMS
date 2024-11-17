import json
from datetime import datetime
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from courses.models import Course, Enrollment, Student
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
        enrollmentList = []
        enroll_dict = {}

        course = Course.objects.filter(pk=courseID).first()
        if course:
            course_date = course.course_date.strftime('%d/%m/%Y')
            course_start = course.course_start.strftime('%I:%M %p')
            course_end = course.course_end.strftime('%I:%M %p')
            course_title = f"{course.course_title} {course_date} {course_start} - {course_end}"
            enroll_dict['course_title'] = course_title

        for e in enrollments:
            enroll_obj = model_to_dict(e)
            student_obj = Student.objects.filter(pk=enroll_obj['student_id']).first()
            enrollment_pk = e.pk

            phone_num = getattr(student_obj, 'studentContactNumber')
            student_name = f'{getattr(student_obj, 'studentFirstName')} {getattr(student_obj, 'studentLastName')}'

            enrollmentDetails = {}
            enrollmentDetails['enrollment_pk'] = enrollment_pk
            enrollmentDetails['phone_num'] = phone_num
            enrollmentDetails['student_name'] = student_name
            enrollmentList.append(enrollmentDetails)

            enroll_dict['enrollmentList'] = enrollmentList

        enroll_arr.append(enroll_dict)
        return JsonResponse(enroll_arr, safe=False)

    def createEnrollment(self, requestBody):
        phoneNum = requestBody.get('phoneNum')
        courseID = requestBody.get('classID')
        res = {}

        if len(phoneNum) != 8 or not phoneNum.isnumeric():
            res = {'enroll_response': 'Phone number can only be 8 digits.'}
            return JsonResponse(res)
        
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
                return JsonResponse(res)
            print("enroll")
            newEnrollment = Enrollment(
                student_id = student,
                course_id = course,
            )

            newEnrollment.save()
            res = {'enroll_response': 'Student added to class successfully.'}
        return JsonResponse(res) 

class ClassAttendanceView(ListView):
    template_name = "class-details.html"
    context_object_name = "enrollments"

    def get_queryset(self):
        requestBody = decodeRequest(self.request)
        print(requestBody)
        if requestBody:
            course_id = requestBody.get("classID")
        return Enrollment.objects.filter(course_id=course_id)

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

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print("timetable post")
        return response
