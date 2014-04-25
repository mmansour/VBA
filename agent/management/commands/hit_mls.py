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
        RETS Prod URL: http://carets.retscure.com:6103/platinum/login
        UserID: CARMANSOURMATT
        Password: carets1121
        User Agent: MRIS Conduit/2.0

        CARETS Test (PTEST) URL: http://ptest.mris.com:6103/ptest/login
        Security Credentials to the Test Server (PTEST) are as follows:
        UserID: CARETSTEST
        Password: PCARETSTEST
        User Agent: MRIS Conduit/2.0

        '''

        test_mls = requests.get('http://ptest.mris.com:6103/ptest/login',
                                headers={'User-Agent': 'CARETS-General/1.0'})


        print 'Hitting the MLS {0}'.format(test_mls.status_code)






  