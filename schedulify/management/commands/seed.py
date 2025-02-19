from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from schedulify.models import Project, Task, Dependency, Employee, Exclusion
import datetime

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

        self.faker = Faker('en_GB')
        dir(self.faker)


    def clear_data(self):
        """Deletes all the table data"""
        Project.objects.all().delete()

    def create_testcase(self):
        test_project = Project.objects.create(
            name = "Test project",
            description = "test project",
            start_date = datetime.datetime.now()
        )

        begin = Task.objects.create(
            name = "begin",
            project = test_project,
            duration = 4
        )
        a = Task.objects.create(
            name = "a",
            project = test_project,
            duration = 3
        )
        b = Task.objects.create(
            name = "b",
            project = test_project,
            duration = 4
        )
        e = Task.objects.create(
            name = "e",
            project = test_project,
            duration = 1
        )
        g = Task.objects.create(
            name = "g",
            project = test_project,
            duration = 2
        )
        c = Task.objects.create(
            name = "c",
            project = test_project,
            duration = 3
        )
        h = Task.objects.create(
            name = "h",
            project = test_project,
            duration = 7
        )
        d = Task.objects.create(
            name = "d",
            project = test_project,
            duration = 5
        )
        p = Task.objects.create(
            name = "p",
            project = test_project,
            duration = 4
        )
        f = Task.objects.create(
            name = "f",
            project = test_project,
            duration = 6
        )
        q = Task.objects.create(
            name = "q",
            project = test_project,
            duration = 2
        )
        end = Task.objects.create(
            name = "end",
            project = test_project,
            duration = 3
        )

        Dependency.objects.create(
            project = test_project,
            dependent_task = a,
            precedent_task = begin
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = b,
            precedent_task = begin
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = e,
            precedent_task = begin
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = g,
            precedent_task = a
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = g,
            precedent_task = e
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = c,
            precedent_task = a
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = c,
            precedent_task = g
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = c,
            precedent_task = b
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = h,
            precedent_task = g
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = d,
            precedent_task = c
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = p,
            precedent_task = d
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = p,
            precedent_task = c
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = p,
            precedent_task = h
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = f,
            precedent_task = d
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = q,
            precedent_task = p
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = q,
            precedent_task = h
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = end,
            precedent_task = f
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = end,
            precedent_task = q
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = end,
            precedent_task = p
        )
        Exclusion.objects.create(
            project = test_project,
            task1 = a,
            task2 = b
        )
        Exclusion.objects.create(
            project = test_project,
            task1 = c,
            task2 = g
        )


    def handle(self, *args, **options):
        self.clear_data()
        self.create_testcase()
