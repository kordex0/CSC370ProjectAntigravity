from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Assignment, Submission
from users.models import User
from courses.models import Course, Section

import datetime

class NewAssignmentForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateField(widget=SelectDateWidget)
    due_time = forms.TimeField(default=datetime.time(17))

class AssignmentSubmissionForm(forms.Form):
    submission = forms.CharField(widget=forms.Textarea)
