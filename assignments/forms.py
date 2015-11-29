from django import forms

from .models import Assignment, Submission
from users.models import User
from courses.models import Course, Section

class NewAssignmentForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    due_date = forms.DateTimeField()

class AssignmentSubmissionForm(forms.Form):
    submission = forms.CharField(widget=forms.Textarea)
