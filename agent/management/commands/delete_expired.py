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
    help = 'Delete Expired'
    def handle(self, *args, **options):
        agt = Agent.objects.filter(Q(license_status='EXPIRED')|Q(license_status='REVOKED')|Q(license_status='DECEASED'))
#        User.objects.filter(Q(income__gte=5000) | Q(income=0))
        for a in agt:
            print "Deleting: {0}, {1}".format(a, a.license_status)
            a.delete()
        print '---------------------------------------'
        print 'Deleted expired, revoked and deceased agents'
















  