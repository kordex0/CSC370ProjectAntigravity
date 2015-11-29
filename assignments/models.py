from django.db import models
from django.utils import timezone


class Assignment(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey('courses.Section', related_name='assignments')
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return str(self.section) + " - " + self.name

class Submission(models.Model):
    assignment = models.ForeignKey('Assignment', related_name='submissions')
    students = models.ManyToManyField('users.User', related_name='submissions')
    submission = models.TextField(null = True)
    submitted = models.DateTimeField(default = timezone.now)

