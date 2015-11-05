from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Course

def course(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courses/detail.html', {'course': course})
    
def index(request):
    courses_list = Course.objects.order_by('name')
    context = {'courses_list': courses_list,}
    return render(request, 'courses/index.html', context)
