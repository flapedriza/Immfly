from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Export channel ratings to CSV'

    def add_arguments(self, parser):
        pass

