from django.shortcuts import render
from django import forms
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError, DataError

from .models import User
from courses.models import Section
from assignments.models import Assignment

from .forms import NewUserForm

@login_required
def user_profile(request):

    try:
        sections_list = []
        assignments_list = []
        user = request.user.user
        if user.is_teacher():
            sections_list = Section.objects.filter(teacher=user.id)
            return render(request, 'users/profile.html', {'user': user, 'sections_list': sections_list})
        elif user.is_student():
            due_assignments_list = []
            sections_list = Section.objects.filter(students=user.id)
            for section in sections_list:
                assignments_list.extend(Assignment.objects.filter(section=section))
            #assignments_list.sort()
            for assignment in assignments_list:
                if assignment.due_date > timezone.now():
                    due_assignments_list.append(assignment)
            print(assignments_list)
            return render(request, 'users/profile.html', {'user': user, 'sections_list': sections_list, 'assignments_list': assignments_list, 'due_assignments_list': due_assignments_list})
    except User.DoesNotExist:
        user = False #quick fix.
    return render(request, 'users/profile.html', {'user': user})

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

        

                
                

