from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from schedulify.models import Project, Task, Dependency, Recource, Exclusion
import datetime

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

        self.faker = Faker('en_GB')
        dir(self.faker)

    def create_testcase(self):
        Project.object.create(
            name = "Test project"
            description = "test project"
            start_date = datetime.datetime.now()
        )

    def handle(self, *args, **options):
        self.create_testcase()
