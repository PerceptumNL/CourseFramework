from django.db import models
from polymorphic import PolymorphicModel

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
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

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'%s' % (self.__str__(),)

    def __str__(self):
        return "%s" % (self.lesson,)

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

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'%s' % (self.__str__(),)

    def __str__(self):
        return "%s:%s" % (self.lesson.title, self.item.title,)

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
    related = models.ManyToManyField('Item', null=True, blank=True,
            verbose_name = 'Related resources', related_name='resources')

    class Meta:
        verbose_name = "Resource"

    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(item_type=Item.TYPE_RESOURCE, *args, **kwargs)

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
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255, verbose_name="Correct Answer")
    positive_feedback = models.TextField(null=True, blank=True,
        verbose_name="Feedback on correct answer")
    negative_feedback = models.TextField(null=True, blank=True,
        verbose_name="Feedback on incorrect answer")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    @property
    def type(self):
        return 'question'

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'%s' % (self.__str__(),)

    def __str__(self):
        return self.question

class RegularQuestion(Question):
    class Meta:
        proxy = True
        verbose_name = "Regular question"
        verbose_name_plural = "Regular questions"

    @property
    def type(self):
        return 'regular_question'

class MultipleChoiceQuestion(Question):
    class Meta:
        proxy = True
        verbose_name = "Multiple-choice question"
        verbose_name_plural = "Multiple-choice questions"

    def save(self, *args, **kwargs):
        self.answer = ",".join([str(option.pk) for option in
            filter(lambda x: x.correct, self.options.all())])
        return super(MultipleChoiceQuestion, self).save(*args, **kwargs)

    @property
    def type(self):
        return 'mc_question'

class QuestionOption(models.Model):
    answer = models.CharField(max_length=100)
    correct = models.BooleanField()
    question = models.ForeignKey('MultipleChoiceQuestion',
            related_name='options')

    def save(self, *args, **kwargs):
        result = super(QuestionOption, self).save(*args, **kwargs)
        self.question.save()
        return result

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return u'%s' % (self.__str__(),)

    def __str__(self):
        return "Option: %s" % (self.answer,)
