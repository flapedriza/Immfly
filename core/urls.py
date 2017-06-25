from django.conf.urls import url

from core.views import Channels, home, Contents

app_name = 'core'

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^channels/$', Channels.as_view(), name='channels'),
    url(r'^channels/(?P<channel_id>[0-9]+)$', Channels.as_view(), name='channel_id'),
    url(r'^channels/(?P<channel_id>[0-9]+)/content$', Contents.as_view(), name='cahnnel_content')
]