from django import forms
from .models import Student

class StudentsCreationForm(forms.ModelForm):
    studentDOB = forms.DateField(
        label="Date of Birth", 
        required=True, 
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}), 
        input_formats=["%Y-%m-%d"]
    )
    class Meta:
        model = Student
        fields = '__all__'