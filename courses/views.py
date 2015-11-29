from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.db import IntegrityError, DataError

from .models import Course, Section
from users.models import User
from users.decorators import get_request_user
from assignments.models import Assignment

from assignments.forms import NewAssignmentForm

@get_request_user
def course_index(request, user, errormsg=None):
    courses = Course.objects.order_by('name')
    context = {'courses': courses, 'user': user, 'errormsg': errormsg}
    return render(request, 'courses/index.html', context)

@get_request_user
def course_detail(request, user, course_id, errormsg=None):
    course = get_object_or_404(Course, id=course_id)
    teachers = []
    if user and user.is_admin():
        teachers = User.teachers.all()
    context = {'course': course, 'user': user, 'errormsg':errormsg, 'teachers': teachers}
    return render(request, 'courses/detail.html', context)

@get_request_user
def section_detail(request, user, id, errormsg=None):
    section = get_object_or_404(Section, id=id)
    assignments = Assignment.objects.filter(section=id)
    students = []
    if user and user.is_admin():
        students = User.students.all()
    context = { 'section': section,
                'user':user,
                'assignments': assignments,
                'students': students,
                'errormsg': errormsg,}
    return render(request, 'section/section.html', context)

def assignment_index(request, section_id):
    assignments = Assignment.objects.filter(section=section_id)
    assignments.order_by('name')
    context = {'assignments': assignments}
    return render(request, 'assignments/index.html', context)

def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    context = {'assignment': assignment}
    return render(request, 'assignments/detail.html', context)

@get_request_user
def add_course(request, user):
    if user is not None:
        try:
            if user.is_admin():
                coursename = request.POST['course_name']
                new_course = Course(name=coursename)
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

    return course_index(request, errormsg=errormsg)

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

    return course_index(request, errormsg=errormsg)


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
                section_teacher = get_object_or_404(User, id=teacher_id)
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

    return course_detail(request, user, course_id=course_id, errormsg=errormsg)

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
def new_assignment(request, user, section_id):
    try:
        section = Section.objects.get(id=section_id)
    except Section.DoesNotExist:
        raise Http404("No such section!")
    if section.teacher != user:
        return HttpResponseForbidden("<h1>Not your class!</h1>")

    if request.method == 'POST':
        form = NewAssignmentForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            try:
                assignment = Assignment(name=formdata['name'], description=formdata['description'], due_date=formdata['due_date'], section=section)
                assignment.save()
                return HttpResponseRedirect(reverse('assignments:detail', args=(assignment.id,)))
            except (IntegrityError, DataError):
                form.add_error(None, "Sorry, couldn't create that assignment.")
    else:
        form = NewAssignmentForm()
    return render(request, 'section/new_assignment.html', {'form': form, 'section_id': section_id})

