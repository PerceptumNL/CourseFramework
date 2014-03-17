from django.contrib import admin
from django.forms.widgets import NumberInput
from course.models import *

class CourseContentsInline(admin.TabularInline):
    model = Course.items.through

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "index":
            kwargs['widget'] = NumberInput()
        return super(CourseContentsInline, self).formfield_for_dbfield(
                db_field, **kwargs)

class CourseAdmin(admin.ModelAdmin):
    inlines = [ CourseContentsInline ]


class ExternalResourceAdmin(admin.ModelAdmin):
    exclude = ('body', 'related')

admin.site.register(Course, CourseAdmin)
admin.site.register(Resource)
admin.site.register(ExternalResource, ExternalResourceAdmin)
admin.site.register(Test)
