from django import forms

from .models import Assignment, Submission
from users.models import User
from courses.models import Course, Section

class NewAssignmentForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.TextField()
    due_date = forms.DateTimeField()
