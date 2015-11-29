
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseForbidden

from .models import Assignment
from users.models import User
from users.decorators import get_request_user
from courses.models import Course, Section

@get_request_user
def assignment_detail(request, user, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        raise Http404("Assignment does not exist")
    return render(request, 'assignments/detail.html', {'assignment': assignment, 'user': user})
    
@get_request_user
def assignment_index(request, user):
    assignments = Assignment.objects.order_by('name')
    context = {'assignments': assignments, 'user': user}
    return render(request, 'assignments/index.html', context)

@get_request_user
def submit_assignment(request, user):
    pass

@get_request_user
def extend(request, assignment):
    """Grant a 2 day extension to an assignment"""
    pass

