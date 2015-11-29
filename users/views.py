from django.shortcuts import render
from django import forms
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db import IntegrityError, DataError

from .models import User
from courses.models import Section
from assignments.models import Assignment

from users.decorators import get_request_user

from .forms import NewUserForm

@login_required
@get_request_user
def user_profile(request, user):

    sections = []
    assignments = []
    if user.is_teacher():
        sections = Section.objects.filter(teacher=user.id)
        context = {'user': user, 'sections': sections}
    elif user.is_student():
        due_assignments = []
        sections = Section.objects.select_related('course')\
            .prefetch_related('assignments').filter(students=user.id)
        for section in sections:
            assignments.extend(section.assignments.all())
        for assignment in assignments:
            if assignment.due_date > timezone.now():
                due_assignments.append(assignment)
        context = {'user': user, 'sections': sections, 'assignments': assignments, 'due_assignments': due_assignments}
    else:
        context = {'user': user}

    return render(request, 'users/profile.html', context)

def new_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            if formdata['password'] != formdata['password_retyped']:
                form.add_error('password', "Password must match retyped")
            else:
                try:
                    django_user = DjangoUser.objects.create_user(formdata['username'], password=formdata['password'])
                    django_user.first_name = formdata['first_name']
                    django_user.last_name = formdata['last_name']
                    django_user.save()
                    user = User(django_user=django_user, role=formdata['role'])
                    user.save()
                    user = authenticate(username=formdata['username'], password=formdata['password'])
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:user_profile'))
                except (IntegrityError, DataError):
                    form.add_error(None, "Sorry, couldn't create that user.")
    else:
        form = NewUserForm()
    return render(request, 'registration/new_user.html', {'form': form})
