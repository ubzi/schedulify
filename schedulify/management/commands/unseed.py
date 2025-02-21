from schedulify.models import Project
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def clear_data(self):
        """Deletes all the table data"""
        Project.objects.all().delete()

    def handle(self, *args, **options):
        self.clear_data()