from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from course.models import *

# Create your views here.
def landing(request):
    courses = Course.objects.all()
    return render(request, 'frontend/landing.html', {
        "courses": courses
    })

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

def lessons(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return HttpResponseRedirect("/")
    return render(request, 'frontend/lessons.html', {
        "course": course,
        "lessons": course.lessons.all()
    })

def resource(request, course_id, lesson_id, request_id):
    try:
        course = Course.objects.get(pk=course_id)
        lesson = Lesson.objects.get(pk=lesson_id)
        resource = Resource.objects.get(pk=resource_id)
    except Course.DoesNotExist:
        return HttpResponseRedirect("/")
    except Lesson.DoesNotExist:
        return HttpResponseRedirect("/")
    except Resource.DoesNotExist:
        return HttpResponseRedirect("/")

    resource = resource.downcast()
    return render(request, 'frontend/resource.html', {
        "course": course,
        "lessson": lesson,
        "resource": resource,
    })
