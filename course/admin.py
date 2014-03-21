from django.contrib import admin
from django import forms
from course.models import *
from adminsortable.admin import SortableInlineAdminMixin
from django_summernote.admin import SummernoteModelAdmin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

############
# Question #
############
class MCOptionsInline(admin.TabularInline):
    model = QuestionOption
    extra = 1
    verbose_name = "Choice"
    verbose_name_plural = "Choices"

class MCQuestionAdmin(PolymorphicChildModelAdmin,
        SummernoteModelAdmin):
    base_model = MultipleChoiceQuestion
    exclude = ('options',)
    inlines = [MCOptionsInline]

class RegularQuestionAdmin(PolymorphicChildModelAdmin, SummernoteModelAdmin):
    base_model = RegularQuestion

class QuestionParentAdmin(PolymorphicParentModelAdmin):
    base_model = Question
    child_models = (
        (RegularQuestion, RegularQuestionAdmin),
        (MultipleChoiceQuestion, MCQuestionAdmin),
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
class ResourceAdmin(PolymorphicChildModelAdmin, SummernoteModelAdmin):
    base_model = Resource
    filter_horizontal = ('related',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "related":
            kwargs["queryset"] = Item.objects.instance_of(Resource,
                    ExternalResource)
        return super(ResourceAdmin,self).formfield_for_foreignkey(
                db_field, request, **kwargs)

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
    list_filter = ('item_type',)
    list_select_related = True
    search_fields = ('title',)

##########
# Lesson #
##########
class LessonContentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Lesson.items.through

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "item":
            kwargs["queryset"] = Item.objects.instance_of(Resource)
            kwargs["label"] = "Resource"
        return super(LessonContentsInline,self).formfield_for_foreignkey(
                db_field, request, **kwargs)

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
