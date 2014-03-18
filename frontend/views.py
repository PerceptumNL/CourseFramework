from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from course.models import *

# Create your views here.
def interface(request):
    return HttpResponse('Interface')

def course(request, course_id):
    courses = Course.objects.all()
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return HttpResponseRedirect("/")
    return render(request, 'frontend/course.html', {
        "courses": courses,
        "course": course
    })
