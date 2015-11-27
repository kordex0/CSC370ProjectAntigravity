
from django.shortcuts import render
from django.http import Http404, JsonResponse

from .models import Assignment
from users.models import User
from users.decorators import get_request_user
from courses.models import Course, Section

def assignment_detail(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        raise Http404("Assignment does not exist")
    return render(request, 'assignments/detail.html', {'assignment': assignment})
    
def assignment_index(request):
    assignments = Assignment.objects.order_by('name')
    context = {'assignments': assignments,}
    return render(request, 'assignments/index.html', context)

@get_request_user
def add_assignment(request, user):
    pass

@get_request_user
def submit_assignment(request, user):
    pass

@get_request_user
def extend(request, assignment):
    """Grant a 2 day extension to an assignment"""
    pass

