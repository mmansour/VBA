import csv
import os
import requests

from django.core.management.base import BaseCommand, CommandError

from mezzanine.utils.urls import slugify

from agent.models import Agent

from settings import TEMPLATE_DIRS, PROJECT_ROOT

class Command(BaseCommand):
    help = 'Import local data to production'

    def handle(self, *args, **options):
        '''
        Vendor:       Mansour, Matt
        Name:         CARMANSOURMATT
        Password:     carets7CTNe5wm
        Permission:   IDX/Public Feed
        User Agent:   CARETS-General/1.0
        RETS Version: RETS/1.7
        Re-Enabled:   28-Apr-2014
        URL:          http://carets.retscure.com:6103/platinum/login

        '''

        test_mls = requests.get('http://carets.retscure.com:6103/platinum/login',
                                auth=('CARMANSOURMATT', 'carets7CTNe5wm'),
                                headers={'User-Agent': 'CARETS-General/1.0'})


        print 'Hitting the MLS {0}'.format(test_mls.status_code)






  