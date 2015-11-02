from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Course

def course(request, id):
    
    course = get_object_or_404(Course, id=id)
    return render(request, 'detail.html', {'course': course})
    
def index(request):
    courses_list = Course.objects.order_by('name')
    context = {'courses_list': courses_list,}
    return render(request, 'index.html', context)
