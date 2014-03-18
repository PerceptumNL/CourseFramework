from django.contrib import admin
from django.forms.widgets import NumberInput
from course.models import *
from adminsortable.admin import SortableInlineAdminMixin

class CourseContentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Course.lessons.through

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "index":
            kwargs['widget'] = NumberInput()
        return super(CourseContentsInline, self).formfield_for_dbfield(
                db_field, **kwargs)

class CourseAdmin(admin.ModelAdmin):
    inlines = [ CourseContentsInline ]

class LessonContentsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Lesson.items.through

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "index":
            kwargs['widget'] = NumberInput()
        return super(LessonContentsInline, self).formfield_for_dbfield(
                db_field, **kwargs)

class LessonAdmin(admin.ModelAdmin):
    inlines = [ LessonContentsInline ]

class ExternalResourceAdmin(admin.ModelAdmin):
    exclude = ('body', 'related')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Resource)
admin.site.register(ExternalResource, ExternalResourceAdmin)
admin.site.register(Test)
