from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import DataError, IntegrityError

from .models import Course, Section
from users.models import User
from assignments.models import Assignment

def course(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courses/detail.html', {'course': course })

def section_detail(request, id):
    try:
        section = Section.objects.get(id=id)
        assignments_list = Assignment.objects.filter(section=id)
    except Section.DoesNotExist:
        raise Http404("Section does not exist")
    return render(request, 'section/section.html', {'section': section, 'assignments_list': assignments_list})
    
def index(request, errormsg=None):
    do_json = request.GET.get('json', False)
    courses_list = Course.objects.order_by('name')
    try:
        user = request.user.user
    except User.DoesNotExist:
        user = False
    if do_json :
        json_object = []
        for course in courses_list:
            json_object.append({'id':course.id, 'name':course.name})
        return JsonResponse(json_object, safe=False)
    else:
        context = {'courses_list': courses_list, 'user': user, 'errormsg': errormsg}
        return render(request, 'courses/index.html', context)

def assignment(request, section_id):
    do_json = request.GET.get('json', False)
    assignment_list = Assignment.objects.filter(section=section_id)
    assignment_list.order_by('name')
    if do_json :
        json_object = []
        for assignment in assignment_list:
            json_object.append({'id':assignment.id, 'name':assignment.name})
        return JsonResponse(json_object, safe=False)
    else:
        context = {'assignment_list': assignment_list,}
        return render(request, 'assignments/index.html', context)

def assignment_detail(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except Assignment.DoesNotExist:
        raise Http404("Assignment does not exist")
    return render(request, 'assignments/detail.html', {'assignment': assignment })

def add_course(request):
    #TODO: Ensure only logged-in admins can get here
    #Can we write a decorator to do the required test?
    try:
        if request.user.user.is_admin():
            coursename = request.POST['course_name']
            new_course = Course(name = coursename)
            new_course.save()
            return HttpResponseRedirect(reverse('courses:detail', args=[new_course.id]))
        else:
            errormsg = "Must have admin access to add courses"
    except KeyError:
        errormsg = "Invalid request to add_course"
    except User.DoesNotExist:
        errormsg = "Cannot add courses: not logged in"
    except DataError:
        errormsg = "Invalid course name"

    return index(request, errormsg=errormsg)


