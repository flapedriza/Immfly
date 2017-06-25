import csv
from decimal import Decimal

from django.core.management import BaseCommand

from core.models import Channel


class Command(BaseCommand):
    help = 'Export channel ratings to CSV'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        rats = {}

        channels = Channel.objects.exclude(title='deleted')

        def get_rating(chan: Channel) -> (Decimal, int):
            if chan.title not in rats:
                avg = Decimal(0.0)
                count = 0
                subch = chan.subchannels.all()

                if not subch:
                    for cont in chan.content_set.all():
                        avg = self.add_averages(avg, count, cont.rating.average, cont.rating.count)
                        count += cont.rating.count

                for subch in subch:
                    avg2, count2 = get_rating(subch)
                    avg = self.add_averages(avg, count, avg2, count2)
                    count += count2

                rats[chan.title] = (avg, count)

            return rats[chan.title]

        for ch in channels:
            get_rating(ch)

        with open('channels.csv', 'w', encoding='utf8', newline='') as channels_csv:
            TWOPLACES = Decimal(10) ** -2
            writer = csv.writer(channels_csv)
            writer.writerow(["Channel", "Rating"])
            for title, vals in rats.items():
                writer.writerow([title, vals[0].quantize(TWOPLACES)])

    @staticmethod
    def add_averages(avg1: Decimal, nval1: int, avg2: Decimal, nval2: int) -> Decimal:
        average = (float(avg1 * nval1) + float(avg2 * nval2)) / max(nval1 + nval2, 1)
        return Decimal(average)
