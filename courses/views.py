from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import DataError, IntegrityError

from .models import Course, Section
from users.models import User
from users.decorators import get_request_user
from assignments.models import Assignment

@get_request_user
def course(request, user, id, errormsg=None):
    try:
        course = Course.objects.get(id=id)
        if user and user.is_admin():
            teacher_list = User.teachers.all()
        else:
            teacher_list = []
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courses/detail.html', {'course': course, 'user': user, 'errormsg':errormsg, 'teacher_list': teacher_list })

@get_request_user
def section_detail(request, user, id, errormsg=None):
    try:
        section = Section.objects.get(id=id)
        assignments_list = Assignment.objects.filter(section=id)
        if user.is_admin():
            student_list = User.students.all()
        else:
            student_list = None
    except Section.DoesNotExist:
        raise Http404("Section does not exist")
    context = { 'section': section,
                'user':user, 
                'assignments_list': assignments_list, 
                'student_list': student_list,
                'errormsg': errormsg,}
    return render(request, 'section/section.html', context)
    
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
                section_teacher = user
            elif user.is_admin():
                teacher_id = request.POST['teacher_id']
                section_teacher = User.objects.get(id=teacher_id)
                if section_teacher.role != User.TEACHER:
                    errormsg = "Selected user is not a teacher"
                    save_data = False
            else:
                errormsg = "You must be an admin or teacher to add a section"
                save_data = False
            
            if save_data:
                new_section = Section(name=section_name, course_id=course_id, teacher=section_teacher) 
                new_section.save()
                if user.is_teacher():
                    return HttpResponseRedirect(reverse('courses:section_detail', args=(new_section.id,)))
                else:
                    return HttpResponseRedirect(reverse('courses:detail', args=(course_id,)))

        except KeyError:
            errormsg = "Invalid request to add_section"
        except DataError:
            errormsg = "Invalid data supplied"
    else:
        errormsg = "Not logged in"

    return course(request, user, id=course_id, errormsg=errormsg)
    
@get_request_user
def enroll(request, user, section_id):
    save_data = True 
    try:
        section = Section.objects.get(id=section_id)
    except DataError:
        errormsg = "Invalid data supplied"
        save_data = False
    if user and user.is_student():
        student = user
    elif user and user.is_admin():
        try:
            student_id = request.POST['student_id']
            student = User.students.get(id=student_id)
        except KeyError:
            errormsg = "Invalid request to enroll"
            save_data = False
        except User.DoesNotExist:
            errormsg = "Invalid student to enroll"
            save_data = False
    else:
        errormsg = "Must be logged in as a student or admin to change enrollment"
        save_data = False
    
    if save_data:
        section.students.add(student)
        return HttpResponseRedirect(reverse('courses:section_detail', args=(section.id,)))
    else:
        return section_detail(request, section_id, errormsg) 
        
@get_request_user
def withdraw(request, user, section_id):
    pass
