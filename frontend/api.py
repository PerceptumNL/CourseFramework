from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, HttpResponseNotFound
import json
from course.models import *

def process_test_submission(request, test_id):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if not request.method == "POST":
        return HttpResponseBadRequest()
    try:
        test = Test.objects.get(pk=test_id)
    except Test.DoesNotExist:
        return HttpResponseNotFound()
    score = 0.0
    total = 0.0
    feedback = {}
    for question in test.questions.all():
        total += 1.0
        answer = ",".join(request.POST.getlist(str(question.pk)))
        if question.answer == answer:
            score += 1.0
            feedback[question.pk] = {
                "correct": True,
                "feedback": question.positive_feedback
            }
        else:
            feedback[question.pk] = {
                "correct": False,
                "feedback": question.negative_feedback
            }
    score /= total
    score *= 100
    return HttpResponse(json.dumps({"score": score, "feedback": feedback}),
            content_type = "application/json")
