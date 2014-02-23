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

class Command(BaseCommand):
    help = 'Delete REA'
    def handle(self, *args, **options):
        agt = Agent.objects.all()
        for a in agt:
            a.delete()
        print 'Deleted all agents'
















