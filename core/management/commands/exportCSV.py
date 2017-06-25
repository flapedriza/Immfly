import csv
from decimal import Decimal

from django.core.management import BaseCommand

from core.management.utils.channel_rate import rate_channels
from core.models import Channel


class Command(BaseCommand):
    help = 'Export channel ratings to CSV'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        channels = Channel.objects.exclude(title='deleted')

        rats = rate_channels(channels)

        with open('channels.csv', 'w', encoding='utf8', newline='') as channels_csv:
            TWOPLACES = Decimal(10) ** -2
            writer = csv.writer(channels_csv)
            writer.writerow(["Channel Title", "Average Rating"])
            for title, vals in rats:
                writer.writerow([title, vals[0].quantize(TWOPLACES)])
