from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponseBadRequest, HttpResponseNotFound

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
        answer = request.POST.get(question.pk, None)
        if question.answer == answer:
            score += 1.0
            feedback[question.pk] = {
                "correct": True,
                "feedback": question.positive_feedback.body
            }
        else:
            feedback[question.pk] = {
                "correct": False,
                "feedback": question.negative_feedback.body
            }
    score /= total
    return HttpResponse({"score":score, "feedback":feedback})
