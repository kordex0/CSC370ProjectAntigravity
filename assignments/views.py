# views.py -> convention to put in functions that take a Web request and return a Web response

from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core import serializers

from .models import Assignment

def assignment(request, id):
    try:
	#first id -> which parameter for the function get, second id -> parameter of function course
        assignment = Assignment.objects.get(id=id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'assignments/detail.html', {'assignment': assignment})
    
def index(request):
    do_json = request.GET.get('json', False)
    assignments_list = Assignment.objects.order_by('name')
    if do_json :
        json_object = []
        for assignment in assignments_list:
            json_object.append({'id':assignment.id, 'name':assignment.name})
        return JsonResponse(json_object, safe=False)
    else:
        # dictionary mapping template variable that names to Python objects
        context = {'assignments_list': assignments_list,}
        # first: request object (given parameter)
        # second: template name
        # third: dictionary (optimal)
        return render(request, 'assignments/index.html', context)
