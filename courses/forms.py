from django import forms
from .models import Course

class CourseCreateForm(forms.ModelForm): 
    class Meta:
        model = Course
        fields = "__all__"

        widgets = {
            "course_date": forms.DateInput(attrs={'type': 'date'}),
            "course_start": forms.TimeInput(format="%H:%M", attrs={'type': 'time'}),
            "course_end": forms.TimeInput(format="%H:%M", attrs={'type': 'time'})
        }
