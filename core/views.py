from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View

from core.models import Channel, Content


def home(request):
    return redirect('/channels')


class Channels(View):
    template_name = 'channels.html'

    def get(self, request, channel_id=False):
        """
        View that shows the list of all root channels or the subchannel list of a channel if channel_id is present
        :param request: HTTP request
        :param channel_id: channel id if necessary
        :return: HTTP response
        """

        if not channel_id:
            channels = Channel.objects.filter(parent_channel=None).exclude(title='deleted')
            channel_name = 'All channels'

        else:
            try:
                parent = Channel.objects.get(id=channel_id)

            except Channel.DoesNotExist:
                return HttpResponseNotFound('<h1>Channel not found<h1>')

            channels = Channel.objects.filter(parent_channel=parent)
            channel_name = parent.title
            if not channels:
                return redirect('/channels/' + str(channel_id) + '/content')

        return render(request, self.template_name, {'channels': channels, 'channel_name': channel_name})


class Contents(View):
    template_name = 'content.html'

    def get(self, request, channel_id):
        """
        View that shows the list of a channel's content
        :param request: Http request
        :param channel_id: channel id
        :return: Http response
        """
        if not channel_id:
            return HttpResponseNotFound('<h1>Channel not found<h1>')

        try:
            channel = Channel.objects.get(id=channel_id)

        except Channel.DoesNotExist:
            return HttpResponseNotFound('<h1>Channel not found<h1>')

        contents = Content.objects.filter(channel=channel)

        return render(request, self.template_name, {'contents': contents, 'channel_name': channel.title})


