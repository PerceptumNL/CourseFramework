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
        "courses": Course.objects.all(),
        "course": course,
        "lessons": course.lessons.all()
    })

def help(request):
    return render(request, 'frontend/help.html', {
        "courses": Course.objects.all()
    })

def faq(request):
    return render(request, 'frontend/faq.html', {
        "courses": Course.objects.all()
    })

def item(request, course_id, lesson_id, item_index):
    item_index = int(item_index)
    try:
        course = Course.objects.get(pk=course_id)
        lesson = Lesson.objects.get(pk=lesson_id)
        rel = LessonContent.objects.get(
            lesson = lesson,
            order = item_index
        )
    except Course.DoesNotExist:
        return HttpResponseRedirect("/")
    except Lesson.DoesNotExist:
        return HttpResponseRedirect("/")
    except LessonContent.DoesNotExist:
        return HttpResponseRedirect("/")
    except LessonContent.MultipleObjectsReturned:
        return HttpResponseRedirect("/")

    button_list = []

    item = rel.item
    
    request.session["crumbs"] = []

    if item_index > 0:
        try:
            prev_res = LessonContent.objects.get(lesson=lesson, order=item_index-1)
            button = {'title': 'Previous', 'url': '/item/'+ str(course.pk) +'/'+ str(lesson.pk) +'/'+ str(prev_res.pk)}
            button_list.append(button)
        except LessonContent.DoesNotExist:
            prev_res = None
        except LessonContent.MultipleObjectsReturned:
            return HttpResponseRedirect("/")
    else:
        prev_res = None
    
    try:
        next_res = LessonContent.objects.get(lesson=lesson, order=item_index+1)
        button = {'title': 'Next', 'url': '/item/'+ str(course.pk) +'/'+ str(lesson.pk) +'/'+ str(next_res.pk)}
        button_list.append(button)
    except LessonContent.DoesNotExist:
        next_res = None
        button = {'title': 'Course Overview', 'url': '/course/' + str(course.pk) +'/lessons'}
        button_list.append(button)
    except LessonContent.MultipleObjectsReturned:
        return HttpResponseRedirect("/")

    return render(request, 'frontend/item.html', {
        "courses": Course.objects.all(),
        "course": course,
        "lesson": lesson,
        "item": item,
        "button_list": button_list,
        "crt_index": item_index,
        "crumbs": [item]
    })


def related(request, course_id, lesson_id, parent_id, related_id):
    parent_id = int(parent_id)
    try:
        course = Course.objects.get(pk=course_id)
        lesson = Lesson.objects.get(pk=lesson_id)
        item = Item.objects.get(pk=related_id)
        parent = LessonContent.objects.get(
            lesson = lesson,
            order = parent_id
        )
    except Course.DoesNotExist:
        return HttpResponseRedirect("/")
    except Lesson.DoesNotExist:
        return HttpResponseRedirect("/")
    except LessonContent.DoesNotExist:
        return HttpResponseRedirect("/")
    except LessonContent.MultipleObjectsReturned:
        return HttpResponseRedirect("/")

    crumbIds = request.session.get("crumbs", [parent_id])

    if item.pk in crumbIds:
        tmpIds = []
        for crumbId in crumbIds:
            if crumbId==item.pk:
                break
            tmpIds.append(crumbId)
        crumbIds = tmpIds
    
    crumbIds.append(item.pk)
    request.session["crumbs"] = crumbIds

    crumbs = []
    for crumbId in crumbIds:
        crumbs.append(Item.objects.get(pk=crumbId))
    
    parent = parent.item
    
    button_list = []
    button = {'title': "back to " + parent.title, 'url': '/item/'+ str(course.pk) +'/'+ str(lesson.pk) +'/'+ str(parent_id)}
    button_list.append(button)
    
    return render(request, 'frontend/item.html', {
        "courses": Course.objects.all(),
        "course": course,
        "lesson": lesson,
        "item": item,
        "button_list": button_list,
        "parent": parent_id,
        "crumbs": crumbs
    })


