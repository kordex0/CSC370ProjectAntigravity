from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core import serializers

from .models import Course

def course(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courses/detail.html', {'course': course})
    
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
