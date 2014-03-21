from django.db import models
from polymorphic import PolymorphicModel

class Course(models.Model):
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now=True, editable=False)
    lessons = models.ManyToManyField('Lesson', through='CourseContent')

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'%s' % (self.__str__(),)

    def __str__(self):
        return self.title

class CourseContent(models.Model):
    course = models.ForeignKey('Course')
    lesson = models.ForeignKey('Lesson')
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now=True, editable=False)
    items = models.ManyToManyField('Item', through='LessonContent')

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'%s' % (self.__str__(),)

    def __str__(self):
        return self.title

class LessonContent(models.Model):
    lesson = models.ForeignKey('Lesson')
    item = models.ForeignKey('Item')
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

class Item(PolymorphicModel):
    TYPE_RESOURCE = 're'
    TYPE_TEST = 'te'
    TYPE_EXTERNAL = 'ex'
    TYPES = (
        (TYPE_RESOURCE, "Resource"),
        (TYPE_EXTERNAL, "External resource"),
        (TYPE_TEST, "Test")
    )
    item_type = models.CharField(max_length=2, choices=TYPES, editable=False)
    title = models.CharField(max_length=255)

    def downcast(self):
        if self.item_type == self.TYPE_RESOURCE:
            return self.resource
        elif self.item_type == self.TYPE_TEST:
            return self.test
        return self

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'%s' % (self.__str__(),)

    def __str__(self):
        return self.title

class Resource(Item):
    body = models.TextField(null=True, blank=True)
    related = models.ManyToManyField('self', null=True, blank=True)

    class Meta:
        verbose_name = "Resource"

    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(item_type=Item.TYPE_RESOURCE, *args, **kwargs)

    def downcast(self):
        if self.resource_type == self.TYPE_EXTERNAL:
            return self.externalresource
        return self

class ExternalResource(Item):
    url = models.URLField(max_length=255)

    class Meta:
        verbose_name = "External resource"

    def __init__(self, *args, **kwargs):
        super(ExternalResource, self).__init__(
                item_type='ex', *args, **kwargs)

class Test(Item):
    questions = models.ManyToManyField('Question', through='TestContents')
    datetime = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Test"

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(item_type='te', *args, **kwargs)

class TestContents(models.Model):
    test = models.ForeignKey('Test')
    question = models.ForeignKey('Question')
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']

class Question(PolymorphicModel):
    title = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    positive_feedback = models.ForeignKey('Resource', null=True, blank=True,
            related_name='+')
    negative_feedback = models.ForeignKey('Resource', null=True, blank=True,
            related_name='+')

    class Meta:
        verbose_name = "Regular question"
        verbose_name_plural = "Regular questions"

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'%s' % (self.__str__(),)

    def __str__(self):
        return self.title

class MultipleChoiceQuestion(Question):
    class Meta:
        proxy = True
        verbose_name = "Multiple-choice question"
        verbose_name_plural = "Multiple-choice questions"

class QuestionOption(models.Model):
    value = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
    question = models.ForeignKey('MultipleChoiceQuestion',
            related_name='options')
