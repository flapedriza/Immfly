from django.core.management import call_command
from django.test import TestCase
# Create your tests here.
from django.utils.six import StringIO

from core.models import *


class CSVTestCase(TestCase):
    def setUp(self):
        root1 = Channel.objects.create(title='root1')
        root2 = Channel.objects.create(title='root2')
        root3 = Channel.objects.create(title='root3')

        root2_1 = Channel.objects.create(title='root2_1', parent_channel=root2)
        root2_2 = Channel.objects.create(title='root2_2', parent_channel=root2)

        root3_1 = Channel.objects.create(title='root3_1', parent_channel=root3)
        root3_2 = Channel.objects.create(title='root3_2', parent_channel=root3)

        root3_1_1 = Channel.objects.create(title='root3_1_1', parent_channel=root3_1)
        root3_1_2 = Channel.objects.create(title='root3_1_2', parent_channel=root3_1)

        cont1 = Content.objects.create(title='root1_1', file='channel_files/default.png', metadata='{"":""}',
                                       channel=root1)
        cont1.rating.count = 12
        cont1.rating.total = 53
        cont1.rating.average = Decimal(4.42)
        cont1.rating.save()
        cont1 = Content.objects.create(title='root1_2', file='channel_files/default.png', metadata='{"":""}',
                                       channel=root1)
        cont1.rating.count = 16
        cont1.rating.total = 84
        cont1.rating.average = Decimal(5.25)
        cont1.rating.save()
        cont1 = Content.objects.create(title='root1_3', file='channel_files/default.png', metadata='{"":""}',
                                       channel=root1)
        cont1.rating.count = 15
        cont1.rating.total = 83
        cont1.rating.average = Decimal(5.53)
        cont1.rating.save()

        cont1 = Content.objects.create(title='root2_1_1', file='channel_files/default.png', metadata='{"":""}',
                                       channel=root2_1)
        cont1.rating.count = 12
        cont1.rating.total = 114
        cont1.rating.average = Decimal(9.5)
        cont1.rating.save()
        cont1 = Content.objects.create(title='root2_2_1', file='channel_files/default.png', metadata='{"":""}',
                                       channel=root2_2)
        cont1.rating.count = 21
        cont1.rating.total = 174
        cont1.rating.average = Decimal(8.3)
        cont1.rating.save()

        cont1 = Content.objects.create(title='root3_1_1_1', file='channel_files/default.png', metadata='{"":""}',
                                       channel=root3_1_1)
        cont1.rating.count = 28
        cont1.rating.total = 147
        cont1.rating.average = Decimal(5.25)
        cont1.rating.save()
        cont1 = Content.objects.create(title='root3_1_2_1', file='channel_files/default.png', metadata='{"":""}',
                                       channel=root3_1_2)
        cont1.rating.count = 24
        cont1.rating.total = 147
        cont1.rating.average = Decimal(6.13)
        cont1.rating.save()
        cont1 = Content.objects.create(title='root3_2_1', file='channel_files/default.png', metadata='{"":""}',
                                       channel=root3_2)
        cont1.rating.count = 45
        cont1.rating.total = 414
        cont1.rating.average = Decimal(9.2)
        cont1.rating.save()
        Content.objects.create(title='root3_2_2', file='channel_files/default.png', metadata='{"":""}',
                               channel=root3_2)

    def test_channel_ratings(self):
        out = StringIO()
        call_command('exportCSV', stdout=out)
        self.assertIn('root1: 5.12', out.getvalue())
        self.assertIn('root2: 8.74', out.getvalue())
        self.assertIn('root2_1: 9.5', out.getvalue())
        self.assertIn('root2_2: 8.30', out.getvalue())
        self.assertIn('root3: 7.30', out.getvalue())
        self.assertIn('root3_1: 5.66', out.getvalue())
        self.assertIn('root3_1_1: 5.25', out.getvalue())
        self.assertIn('root3_1_2: 6.13', out.getvalue())
        self.assertIn('root3_2: 9.20', out.getvalue())
