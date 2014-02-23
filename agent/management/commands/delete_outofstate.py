from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from agent.models import Agent
import urllib2
import datetime
import pprint
from math import ceil
import time
import requests
from settings import UA, DATA_LOCATION
from django.db.models import Q

class Command(BaseCommand):
    help = 'Delete Out Of State Licensees'
    def handle(self, *args, **options):
        agt = Agent.objects.exclude(mailing_state='CA')
#        User.objects.filter(Q(income__gte=5000) | Q(income=0))
        for a in agt:
            print "Deleting state:  {0}, {1}".format(a, a.mailing_state)
            a.delete()
        print '---------------------------------------'
        print 'Deleted all out of staters'
















    