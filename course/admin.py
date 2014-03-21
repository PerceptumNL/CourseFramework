from django.contrib import admin
from django import forms
from course.models import *
from adminsortable.admin import SortableInlineAdminMixin
from django_summernote.admin import SummernoteModelAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

############
# Question #
############
class QuestionOptionForm(forms.ModelForm):
    label = forms.CharField(label='Label:')
    value = forms.CharField(label='Answer:')

    class Meta:
        model = QuestionOption

class QuestionOptionAdmin(admin.ModelAdmin):
    model = QuestionOption
    form = QuestionOptionForm

class NormalQuestionAdmin(PolymorphicChildModelAdmin):
    base_model = Question

class MCOptionsInline(admin.TabularInline):
    model = QuestionOption
    form = QuestionOptionForm
    exclude = ('questionoption',)
    verbose_name = "Choice"
    verbose_name_plural = "Choices"

class MultipleChoiceQuestionAdmin(PolymorphicChildModelAdmin):
    base_model = MultipleChoiceQuestion
    exclude = ('options',)
    inlines = [MCOptionsInline]

class QuestionParentAdmin(PolymorphicParentModelAdmin):
    base_model = Question
    child_models = (
        (Question, NormalQuestionAdmin),
        (MultipleChoiceQuestion, MultipleChoiceQuestionAdmin),
    )

########
# Test #
########
class TestContentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Test.questions.through
    extra = 1
    verbose_name = 'Test question'
    verbose_name_plural = 'Test questions'

class TestInline(admin.StackedInline):
    model = Test

class TestAdmin(PolymorphicChildModelAdmin):
    base_model = Test
    inlines = [TestContentsInline]

############
# Resource #
############
class ResourceInline(admin.StackedInline):
    model = Resource

class ResourceAdmin(PolymorphicChildModelAdmin, SummernoteModelAdmin):
    base_model = Resource
    def get_queryset(self, request):
        qs = super(ResourceAdmin, self).get_queryset(request)
        return qs.exclude(resource_type=Resource.TYPE_EXTERNAL)

class ExternalResourceAdmin(PolymorphicChildModelAdmin):
    base_model = ExternalResource


########
# Item #
########
class ItemAdmin(PolymorphicParentModelAdmin):
    base_model = Item
    child_models = (
        (Resource, ResourceAdmin),
        (ExternalResource, ExternalResourceAdmin),
        (Test, TestAdmin),
    )

##########
# Lesson #
##########
class LessonContentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Lesson.items.through

class LessonAdmin(admin.ModelAdmin):
    inlines = [ LessonContentsInline ]

##########
# Course #
##########
class CourseContentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Course.lessons.through

class CourseAdmin(admin.ModelAdmin):
    inlines = [ CourseContentsInline ]

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Question, QuestionParentAdmin)
