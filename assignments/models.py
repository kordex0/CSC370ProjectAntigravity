from django.db import models


class Assignment(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey('courses.Section')
    description = models.TextField()
    due_date = models.DateTimeField()

    def __str__(self):
        return str(self.section) + " - " + self.name

class Submission(models.Model):
    assignment = models.ForeignKey('Assignment')
    students = models.ManyToManyField('users.User')

