from django.core.management.base import BaseCommand, CommandError
from faker import Faker # type: ignore
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

    def create_large_testcase_helper(self, test_project, end):

        begin = Task.objects.create(
            name = "begin",
            project = test_project,
            min_estimated_duration = 4,
            max_estimated_duration = 6
        )
        if end:
            Dependency.objects.create(
                project = test_project,
                dependent_task = begin,
                precedent_task = end
            )

        a = Task.objects.create(
            name = "a",
            project = test_project,
            min_estimated_duration = 3,
            max_estimated_duration = 7

        )
        b = Task.objects.create(
            name = "b",
            project = test_project,
            min_estimated_duration = 4,
            max_estimated_duration = 4
        )
        e = Task.objects.create(
            name = "e",
            project = test_project,
            min_estimated_duration = 1,
            max_estimated_duration = 4
        )
        g = Task.objects.create(
            name = "g",
            project = test_project,
            min_estimated_duration = 2,
            max_estimated_duration = 3
        )
        c = Task.objects.create(
            name = "c",
            project = test_project,
            min_estimated_duration = 3,
            max_estimated_duration = 4
        )
        h = Task.objects.create(
            name = "h",
            project = test_project,
            min_estimated_duration = 7,
            max_estimated_duration = 13
        )
        d = Task.objects.create(
            name = "d",
            project = test_project,
            min_estimated_duration = 5,
            max_estimated_duration = 6
        )
        p = Task.objects.create(
            name = "p",
            project = test_project,
            min_estimated_duration = 4,
            max_estimated_duration = 11
        )
        f = Task.objects.create(
            name = "f",
            project = test_project,
            min_estimated_duration = 6,
            max_estimated_duration = 9
        )
        q = Task.objects.create(
            name = "q",
            project = test_project,
            min_estimated_duration = 2,
            max_estimated_duration = 3
        )
        end = Task.objects.create(
            name = "end",
            project = test_project,
            min_estimated_duration = 3,
            max_estimated_duration = 5
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
        return end

    def create_large_testcase(self):
        test_project = Project.objects.create(
            name = "Test project",
            description = "test project",
            start_date = datetime.datetime(2025, 1, 1)
        )

        Employee.objects.create(
            project = test_project,
            name = "John"
        )
        Employee.objects.create(
            project = test_project,
            name = "George"
        )

        end = None
        for i in range(100):
            end = self.create_large_testcase_helper(test_project, end)
            

    def create_testcase(self):
        test_project = Project.objects.create(
            name = "Test project",
            description = "test project",
            start_date = datetime.datetime(2025, 1, 1)
        )

        begin = Task.objects.create(
            name = "begin",
            project = test_project,
            min_estimated_duration = 4,
            max_estimated_duration = 6
        )
        a = Task.objects.create(
            name = "a",
            project = test_project,
            min_estimated_duration = 3,
            max_estimated_duration = 7

        )
        b = Task.objects.create(
            name = "b",
            project = test_project,
            min_estimated_duration = 4,
            max_estimated_duration = 4
        )
        e = Task.objects.create(
            name = "e",
            project = test_project,
            min_estimated_duration = 1,
            max_estimated_duration = 4
        )
        g = Task.objects.create(
            name = "g",
            project = test_project,
            min_estimated_duration = 2,
            max_estimated_duration = 3
        )
        c = Task.objects.create(
            name = "c",
            project = test_project,
            min_estimated_duration = 3,
            max_estimated_duration = 4
        )
        h = Task.objects.create(
            name = "h",
            project = test_project,
            min_estimated_duration = 7,
            max_estimated_duration = 13
        )
        d = Task.objects.create(
            name = "d",
            project = test_project,
            min_estimated_duration = 5,
            max_estimated_duration = 6
        )
        p = Task.objects.create(
            name = "p",
            project = test_project,
            min_estimated_duration = 4,
            max_estimated_duration = 11
        )
        f = Task.objects.create(
            name = "f",
            project = test_project,
            min_estimated_duration = 6,
            max_estimated_duration = 9
        )
        q = Task.objects.create(
            name = "q",
            project = test_project,
            min_estimated_duration = 2,
            max_estimated_duration = 3
        )
        end = Task.objects.create(
            name = "end",
            project = test_project,
            min_estimated_duration = 3,
            max_estimated_duration = 5
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
        # # Exclusion.objects.create(
        # #     project = test_project,
        # #     task1 = a,
        # #     task2 = b
        # # )
        # Exclusion.objects.create(
        #     project = test_project,
        #     task1 = c,
        #     task2 = g
        # )
        Employee.objects.create(
            project = test_project,
            name = "John"
        )
        Employee.objects.create(
            project = test_project,
            name = "George"
        )



    def create_resource_testcase(self):
        test_project = Project.objects.create(
            name = "Test project",
            description = "test project",
            start_date = datetime.datetime(2025, 1, 1)
        )
        a = Task.objects.create(
            name = "A",
            project = test_project,
            min_estimated_duration = 1,
            max_estimated_duration = 1
        )
        b = Task.objects.create(
            name = "B",
            project = test_project,
            min_estimated_duration = 2,
            max_estimated_duration = 4
        )
        c = Task.objects.create(
            name = "C",
            project = test_project,
            min_estimated_duration = 1,
            max_estimated_duration = 1
        )
        d = Task.objects.create(
            name = "D",
            project = test_project,
            min_estimated_duration = 1,
            max_estimated_duration = 1
        )
        e = Task.objects.create(
            name = "E",
            project = test_project,
            min_estimated_duration = 2,
            max_estimated_duration = 2
        )
        # f = Task.objects.create(
        #     name = "F",
        #     project = test_project,
        #     min_estimated_duration = 1,
        #     max_estimated_duration = 1
        # )
        # g = Task.objects.create(
        #     name = "G",
        #     project = test_project,
        #     min_estimated_duration = 1,
        #     max_estimated_duration = 1
        # )

        Dependency.objects.create(
            project = test_project,
            dependent_task = c,
            precedent_task = a
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = d,
            precedent_task = c
        )
        Dependency.objects.create(
            project = test_project,
            dependent_task = e,
            precedent_task = c
        )
        # Dependency.objects.create(
        #     project = test_project,
        #     dependent_task = f,
        #     precedent_task = e
        # )
        # Dependency.objects.create(
        #     project = test_project,
        #     dependent_task = g,
        #     precedent_task = b
        # )

        Employee.objects.create(
            project = test_project,
            name = "John"
        )
        Employee.objects.create(
            project = test_project,
            name = "George"
        )

    def handle(self, *args, **options):
        self.clear_data()
        self.create_testcase()
        # self.create_resource_testcase()
        # self.create_large_testcase()
