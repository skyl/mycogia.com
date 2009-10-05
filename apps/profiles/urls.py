from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^map/$', 'profiles.views.map', name="profile_map"),
    url(r'^username_autocomplete/$', 'misc.views.username_autocomplete_all', name='profile_username_autocomplete'),
    url(r'^$', 'profiles.views.profiles', name='profile_list'),
    url(r'^(?P<username>[\w\._-]+)/$', 'profiles.views.profile', name='profile_detail'),
)
