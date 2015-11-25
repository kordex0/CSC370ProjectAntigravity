from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import Course, Section
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
    
def index(request):
    do_json = request.GET.get('json', False)
    courses_list = Course.objects.order_by('name')
    if do_json :
        json_object = []
        for course in courses_list:
            json_object.append({'id':course.id, 'name':course.name})
        return JsonResponse(json_object, safe=False)
    else:
        context = {'courses_list': courses_list,}
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


