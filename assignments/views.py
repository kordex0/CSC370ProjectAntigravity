
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseForbidden

from .models import Assignment
from users.models import User
from users.decorators import get_request_user
from courses.models import Course, Section
from .forms import NewAssignmentForm

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
def new_assignment(request, user, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        raise Http404("No such section!")
    if section.teacher != user
        return HttpResponseForbidden("<h1>Not your class!</h1>")
    if request.method == 'POST':
        form = NewAssignmentForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            try:
                assignment = Assignment(name=formdata['name'], description=formdata['description'], due_date=formdata['due_date'], section=section)
                assignment.save()
                return HttpResponseRedirect(reverse('users:user_profile'))
            except (IntegrityError, DataError):
                form.add_error(None, "Sorry, couldn't create that assignment.")
    else:
        form = NewAssignmentForm()
    return render(request, 'section/new_assignment.html', {'form': form, 'section_id': section_id})


@get_request_user
def submit_assignment(request, user):
    pass

@get_request_user
def extend(request, assignment):
    """Grant a 2 day extension to an assignment"""
    pass

