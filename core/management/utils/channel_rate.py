from decimal import Decimal

from core.models import Channel


def add_averages(avg1: Decimal, nval1: int, avg2: Decimal, nval2: int) -> Decimal:
    average = (float(avg1 * nval1) + float(avg2 * nval2)) / max(nval1 + nval2, 1)
    return Decimal(average)


def rate_channels(channels: [Channel]) -> [(str, Decimal)]:

    rats = {}

    def get_rating(chan: Channel) -> (Decimal, int):
        if chan.title not in rats:
            avg = Decimal(0.0)
            count = 0
            subch = chan.subchannels.all()

            if not subch:
                for cont in chan.content_set.all():
                    avg = add_averages(avg, count, cont.rating.average, cont.rating.count)
                    count += cont.rating.count

            for subch in subch:
                avg2, count2 = get_rating(subch)
                avg = add_averages(avg, count, avg2, count2)
                count += count2

            rats[chan.title] = (avg, count)

        return rats[chan.title]

    [get_rating(chan) for chan in channels]

    return sorted(rats.items(), key=lambda x: x[1][0], reverse=True)