
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponseRedirect 
from django.core.urlresolvers import reverse

from .models import Assignment, Submission
from users.models import User
from users.decorators import get_request_user
from courses.models import Course, Section

from .forms import AssignmentSubmissionForm

from django.db import IntegrityError, DataError

@get_request_user
def assignment_detail(request, user, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        raise Http404("Assignment does not exist")
    can_submit=False
    submitted=False

    if user in assignment.section.students.all():
        if Submission.objects.filter(students=user, assignment=assignment).exists():
            submitted=True
        else:
            can_submit=True 
     
    return render(request, 'assignments/detail.html', {'assignment': assignment, 'user': user, 'can_submit': can_submit, 'submitted': submitted})
    
@get_request_user
def assignment_index(request, user):
    assignments = Assignment.objects.order_by('name')
    context = {'assignments': assignments, 'user': user}
    return render(request, 'assignments/index.html', context)

@get_request_user
def submission(request, user, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        raise Http404("No such section!")
    if user not in assignment.section.students.all():
        return HttpResponseForbidden("<h1>Not your class!</h1>")

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            try:
                submission = Submission(assignment = assignment)
                submission.save()
                submission.students.add(user)
                return HttpResponseRedirect(reverse('assignments:detail', args=(assignment.id,)))
            except (IntegrityError, DataError):
                form.add_error(None, "Sorry, couldn't submit")
    else:
        form = AssignmentSubmissionForm()
    return render(request, 'assignments/submit.html', {'form': form, 'assignment_id': assignment_id})
