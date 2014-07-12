from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from mezzanine.core.views import direct_to_template

urlpatterns = patterns('agent.views',
    url(r'^agent_lookup/$', "states", name="states"),
    url(r'^agent_lookup/(?P<agent_state_slug>[\w-]+)/$', "cities", name="cities"),
    url(r'^agent_lookup/(?P<agent_state_slug>[\w-]+)/(?P<agent_city_slug>[\w-]+)/$', "agents", name="agents"),
    url(r'^agent/(?P<agent_data>[\w-]+)/(?P<license_id>\d+)/$', "agent_details", name="agent_details"),
    url(r'^agent/claimprofile/$', "agent_claim", name="agent_claim"),
    url(r'^agent/claimprofile/error/$', "agent_claim_error", name="agent_claim_error"),
    url(r'^agent/profile/edit/(?P<agent_id>\d+)/$', "agent_edit_profile", name="agent_edit_profile"),
    url(r'^agent/profile/edit-headshot/(?P<agent_id>\d+)/$', "agent_edit_profile_headshot", name="agent_edit_profile_headshot"),
    url("^$", "home", name="home"),
)