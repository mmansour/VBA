from agent.models import *
from django.contrib.auth.models import User
from cities_light.models import City, Region, Country

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django import forms
from django.http import HttpResponse, Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django.utils.translation import ugettext_lazy as _

from haystack.forms import SearchForm

from mezzanine.utils.views import paginate


# FORMS
class ClaimForm(forms.Form):
    license_id = forms.CharField(required=True,)


class NotesSearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()


class AgentProfileEditForm(forms.Form):
    profile_image = forms.ImageField(required=False,)
    about_me = forms.CharField(widget=forms.Textarea, required=False,)
    specialties = forms.CharField(widget=forms.Textarea, required=False,)
    certifications_awards = forms.CharField(widget=forms.Textarea, required=False,)
    mls_association = forms.CharField(required=False,)
    website = forms.URLField(required=False,)
    facebook = forms.URLField(required=False,)
    youtube = forms.URLField(required=False,)
    twitter = forms.URLField(required=False,)
    linkedin = forms.URLField(required=False,)
    pinterest = forms.URLField(required=False,)



# New Email Function
def email_profile_claimed(request_user, agent_title, agent_url):

    current_site = Site.objects.get_current()

    #TO Admin
    subject = 'Profile claimed by {0}'.format(request_user)
    text_content = 'Profile claimed by {0}, Agent Title {1}'.format(request_user, agent_title)
    html_content = 'Profile claimed by {0}: Agent Title <a href="http://{1}{2}" target="_blank">{3}</a>'.format(request_user, current_site.domain, agent_url, agent_title)

    from_email='realestateagentlookup@gmail.com'
    to='slackbabbath@gmail.com'

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)


def abbreviate_slugged_state(region):
    if region == 'california':
        return 'ca'
    if region == 'michigan':
        return 'mi'

    
def is_profile_claimed(request_user):
    profile_claimed = False
    profile_id = 0
    if request_user.is_authenticated():
        allagents = Agent.objects.filter(user=request_user)
        if len(allagents) > 0:
            profile_claimed = True
            for agt in allagents:
                profile_id = agt.id

    return profile_claimed, profile_id


import gc
def queryset_iterator(queryset, chunksize=50000):
    '''
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    '''
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        for row in queryset.filter(pk__gt=pk)[:chunksize]:
            pk = row.pk
            yield row
        gc.collect()


def agents(request, agent_state_slug, agent_city_slug):
    agents = queryset_iterator(Agent.objects.filter(slugged_state=abbreviate_slugged_state(agent_state_slug),
                               slugged_city=agent_city_slug))
    # agents = get_list_or_404(Agent, slugged_state=abbreviate_slugged_state(agent_state_slug),
    #                          slugged_city=agent_city_slug)

    agent_list = []
    for ag in agents:
        agent_list.append(ag)

    agents = paginate(agent_list,
                      request.GET.get("page", 1),
                      100, 10)

    profile_claimed = is_profile_claimed(request.user)

    if request.GET.get("page") == '1':
        return HttpResponsePermanentRedirect(reverse('agent.views.agents',
                                                     args=[agent_state_slug, agent_city_slug]))

    return render_to_response('pages/agents.html',
                              {'agents': agents,
                               'agent_state_slug': agent_state_slug,
                               'agent_city_slug': agent_city_slug,
                               'profile_claimed': profile_claimed}, context_instance=RequestContext(request))

@login_required
def agent_claim(request):
    form = ClaimForm(auto_id=True)
    if request.method == "POST":
        form = ClaimForm(request.POST, auto_id=True)

        if form.is_valid():
            provided_license_id = form.cleaned_data['license_id']
            try:
                agent = Agent.objects.get(license_id=provided_license_id)
                if agent.user:
                    redirect = '/agent/claimprofile/error/?errortype=alreadyclaimed'
                    return HttpResponseRedirect(redirect)
                else:
                    agent.user = request.user
                    agent.save()
                    email_profile_claimed(request.user, agent.title, agent.get_absolute_url())
                    redirect = agent.get_absolute_url()
                    return HttpResponseRedirect(redirect)
            except IntegrityError:
                redirect = '/agent/claimprofile/error/?errortype=multipleprofiles'
                return HttpResponseRedirect(redirect)

    return render_to_response('pages/claimform.html',{'form':form},
                context_instance=RequestContext(request))


@login_required
def agent_claim_error(request):
    return render_to_response('integrityerror.html', {},
                              context_instance=RequestContext(request))


@login_required
def agent_edit_profile(request, agent_id):

    agent = Agent.objects.get(pk=agent_id)

    if request.user != agent.user:
        return HttpResponseRedirect('/agent/claimprofile/error/?errortype=forbidden')

    init_data = {
        'profile_image': agent.profile_image,
        'about_me':agent.about_me,
        'specialties':agent.specialties,
        'certifications_awards':agent.certifications_awards,
        'mls_association':agent.mls_association,
        'website':agent.website,
        'facebook':agent.facebook,
        'youtube':agent.youtube,
        'twitter':agent.twitter,
        'linkedin':agent.linkedin,
        'pinterest':agent.pinterest,
    }

    form = AgentProfileEditForm(auto_id=True, initial=init_data)
    if request.method == "POST":
        form = AgentProfileEditForm(request.POST, request.FILES, auto_id=True)

        if form.is_valid():

            profile_image = form.cleaned_data['profile_image']
            about_me = form.cleaned_data['about_me']
            specialties = form.cleaned_data['specialties']
            certifications_awards = form.cleaned_data['certifications_awards']
            mls_association = form.cleaned_data['mls_association']
            website = form.cleaned_data['website']
            facebook = form.cleaned_data['facebook']
            youtube = form.cleaned_data['youtube']
            twitter = form.cleaned_data['twitter']
            linkedin = form.cleaned_data['linkedin']
            pinterest = form.cleaned_data['pinterest']

            agent.profile_image = profile_image
            agent.about_me = about_me
            agent.specialties = specialties
            agent.certifications_awards = certifications_awards
            agent.mls_association = mls_association
            agent.website = website
            agent.facebook = facebook
            agent.youtube = youtube
            agent.twitter = twitter
            agent.linkedin = linkedin
            agent.pinterest = pinterest

            agent.save()
            redirect = agent.get_absolute_url()
            return HttpResponseRedirect(redirect)

    return render_to_response('pages/agent_edit_profile.html',{'agent':agent, 'form':form,},
                context_instance=RequestContext(request))


def get_percentage(number):
    return int((float(number) / float(10)) * 100)


def agent_details(request, agent_data, license_id):
    agent = get_object_or_404(Agent, slug=agent_data, license_id=license_id)

    percent_residential = get_percentage(agent.bar_graph_one)
    percent_commercial = get_percentage(agent.bar_graph_two)
    percent_land = get_percentage(agent.bar_graph_three)
    percent_investors = get_percentage(agent.bar_graph_four)

    print percent_residential

    profile_claimed = is_profile_claimed(request.user)
    
    active_region = ActiveRegion.objects.get(slugged_region_abbr=agent.slugged_state)
    return render_to_response('pages/agent_theme1.html',
                              {'agent': agent, 'active_region': active_region,
                               'profile_claimed': profile_claimed,
                               'percent_residential': percent_residential,
                               'percent_commercial': percent_commercial,
                               'percent_land': percent_land,
                               'percent_investors': percent_investors},
                              context_instance=RequestContext(request))


def states(request):
    active_regions = ActiveRegion.objects.all()
    profile_claimed = is_profile_claimed(request.user)
    return render_to_response('pages/states.html',
            {'active_regions':active_regions, 'profile_claimed':profile_claimed},
              context_instance=RequestContext(request))


def cities(request, agent_state_slug):
    active_region = get_object_or_404(ActiveRegion, slugged_region=agent_state_slug)

    agent = Agent.objects.filter(slugged_state=abbreviate_slugged_state(agent_state_slug))\
        .values('mailing_city').distinct().order_by('mailing_city')

    profile_claimed = is_profile_claimed(request.user)
    
    return render_to_response('pages/cities_by_state.html',
                              {'agent': agent,
                               'active_region': active_region,
                               'profile_claimed': profile_claimed}, context_instance=RequestContext(request))


def get_percentage(number):
    return (float(number) / float(10)) * 100


def home(request):
    active_region = ActiveRegion.objects.all()
    most_recent_agents = Agent.objects.filter(license_type='Salesperson').order_by('-publish_date')[:10]

    profile_claimed = is_profile_claimed(request.user)

    return render_to_response('index.html', {'active_region': active_region,
                                             'most_recent_agents': most_recent_agents,
                                             'profile_claimed': profile_claimed},
                              context_instance=RequestContext(request))




