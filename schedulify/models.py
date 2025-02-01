from django.db import models
from django.db.models import Model

class Project(Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()

class Task(Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    duration = models.IntegerField()

class Dependency(Model):
    id = models.AutoField(primary_key=True)
    dependant_task = models.ForeignKey(task, on_delete=models.CASCADE)
    precedant_task = models.ForeignKey(task, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    duration = models.IntegerField()