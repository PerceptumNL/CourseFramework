from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now=True, editable=False)
    items = models.ManyToManyField('Item', through='CourseContent')

class CourseContent(models.Model):
    course = models.ForeignKey('Course')
    item = models.ForeignKey('Item')
    index = models.PositiveIntegerField()

class Item(models.Model):
    TYPE_RESOURCE = 're'
    TYPE_TEST = 'te'
    TYPES = (
        (TYPE_RESOURCE, "Resource"),
        (TYPE_TEST, "Test")
    )
    item_type = models.CharField(max_length=2, choices=TYPES, editable=False)
    title = models.CharField(max_length=255)

    def downcast(self):
        if self.item_type == TYPE_RESOURCE:
            return self.resource
        elif self.item_type == TYPE_TEST:
            return self.test
        return self

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return str(self)

    def __str__(self):
        return self.title

class Resource(Item):
    TYPE_RESOURCE = ''
    TYPE_EXTERNAL = 'ex'
    TYPES = (
        (TYPE_RESOURCE, "Resource"),
        (TYPE_EXTERNAL, "External Resource")
    )
    body = models.TextField(null=True, blank=True)
    resource_type = models.CharField(max_length=2, choices=TYPES,
            editable=False, default=TYPE_RESOURCE)
    related = models.ManyToManyField('self', null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(item_type=Item.TYPE_RESOURCE, *args, **kwargs)

class ExternalResource(Resource):
    url = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(ExternalResource, self).__init__(
                resource_type='ex', *args, **kwargs)

class Test(Item):
    questions = models.ManyToManyField('Question')
    datetime = models.DateTimeField(auto_now=True, editable=False)

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(item_type='te', *args, **kwargs)

class Question(models.Model):
    title = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

class MultipleChoiceQuestion(Question):
    options = models.ManyToManyField('QuestionOption')

class QuestionOption(models.Model):
    value = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
