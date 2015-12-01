from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone

from .models import Assignment, Submission
from users.models import User
from courses.models import Course, Section

import datetime

def now_plus_days(daycount):
    def inner():
        return timezone.localtime(timezone.now()) + timezone.timedelta(days=daycount)
    return inner

class NewAssignmentForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateField(widget=SelectDateWidget, initial=now_plus_days(7))
    due_time = forms.TimeField(initial=datetime.time(17))

class AssignmentSubmissionForm(forms.Form):
    submission = forms.CharField(widget=forms.Textarea)
