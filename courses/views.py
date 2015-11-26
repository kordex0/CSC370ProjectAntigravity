from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import DataError, IntegrityError

from .models import Course, Section
from users.models import User
from users.decorators import get_request_user
from assignments.models import Assignment

@get_request_user
def course(request, user, id, errormsg=None):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courses/detail.html', {'course': course, 'user': user, 'errormsg':errormsg })

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
    except (User.DoesNotExist, AttributeError):
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

@get_request_user
def add_course(request, user):
    #TODO: Ensure only logged-in admins can get here
    #Can we write a decorator to do the required test?
    if user is not None:
        try:
            if user.is_admin():
                coursename = request.POST['course_name']
                new_course = Course(name = coursename)
                new_course.save()
                return HttpResponseRedirect(reverse('courses:index'))
            else:
                errormsg = "Must have admin access to add courses"
        except KeyError:
            errormsg = "Invalid request to add_course"
        except DataError:
            errormsg = "Invalid course name"
    else:
        errormsg = "Not logged in"

    return index(request, errormsg=errormsg)

@get_request_user
def delete_course(request, user, course_id):
    if user is not None:
        try:
            if user.is_admin():
                try:
                    course = Course.objects.get(id=course_id)
                    course.delete() 
                except Course.DoesNotExist:
                    errormsg = "Invalid course id"
                else:
                    return HttpResponseRedirect(reverse('courses:index'))
            else:
                errormsg = "Must have admin access to delete courses"
        except KeyError:
            errormsg = "Invalid request to delete_course"
    else:
        errormsg = "Not logged in"

    return index(request, errormsg=errormsg)


@get_request_user
def add_section(request, user, course_id):
    if user is not None:
        try:
            save_data = True
            section_name = request.POST['section_name']
            if user.is_teacher():
                course_teacher = user
            elif user.is_admin():
                teacher_id = request.POST['teacher_id']
                course_teacher = User.objects.get(id=teacher_id)
                if course_teacher.role != User.TEACHER:
                    errormsg = "Selected user is not a teacher"
                    save_data = False
            else:
                errormsg = "You must be an admin or teacher to add a section"
                save_data = False
            
            if save_data:
                new_section = Section(name=section_name, course=course_id, teacher=course_teacher) 
                new_section.save()
                if user.is_teacher():
                    return HttpResponseRedirect(reverse('courses:section_detail', new_section.id))
                else:
                    return HttpResponseRedirect(reverse('courses:detail', course_id))

        except KeyError:
            errormsg = "Invalid request to add_section"
        except DataError:
            errormsg = "Invalid data supplied"
    else:
        errormsg = "Not logged in"

    return course(request, user, course_id, errormsg=errormsg)
    
