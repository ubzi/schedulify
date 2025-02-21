from django.db import models
from django.db.models import Model

class Project(Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    start_date = models.DateTimeField()

class Task(Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    min_estimated_duration = models.IntegerField()
    max_estimated_duration = models.IntegerField()

class Dependency(Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    dependent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name = "dependent_task")
    precedent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name = "precedent_task")

class Employee(Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    available_start_time = models.DateTimeField()
    available_end_time = models.DateTimeField()

class Exclusion(Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task1 = models.ForeignKey(Task, on_delete=models.CASCADE, related_name = "task1")
    task2 = models.ForeignKey(Task, on_delete=models.CASCADE, related_name = "task2")
