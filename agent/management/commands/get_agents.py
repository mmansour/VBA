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
    help = 'Get REA'
    def handle(self, *args, **options):
        # URL TO GET ALL AGENTS
        #http://www2.dre.ca.gov/PublicASP/pplinfo.asp?NAV=1&LicenseeName=MANSOUR

        # NUM Pages = total num results/25
        # NAV=PAGE NUM

#        payload = {
#            'NAV':'1',
#            'LicenseeName':'aa',
#        }
#        alpha_a = [
#                    'aa',
#                   'ab',
#                   'ac',
#                   'ad',
#                    'ae',
#                    'af',
#                    'ag',
#                    'ah',
#                    'ai',
#                   'aj',
#                   'al',
#                   'am',
#                   'an',
#                   'ao',
#                    'ap',
#                   'aq',
#                    'ar',
#                   'as',
#                    'at',
#                    'au',
#                    'av',
#'aw',
#'ax', 'ay', 'az',]

#        alpha_b = [
#        'baz',
#        'bb', 'bc', 'bd',
#        'bez',
#        'bf', 'bg', 'bh',
#        'bi',
#        'bj', 'bk', 'bl', 'bm', 'bn', 'bo',
#        'bp', 'bq',
#        'bru',
#        'bs', 'bt',
#        'buz',
#        'bv', 'bw', 'bx',
#        'by', 'bz',
#        ]

        alpha_c = [
                   # 'cal',
                   # 'cb', 'cc', 'cd', 'ce', 'cf',
                   # 'cf', 'cg', 'ci', 'cj', 'ck',
                   # 'che',
                   # 'cl', 'cm', 'cn', 'cp', 'cq', 'cr', 'cs', 'ct', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz',
                   'cot',

                   ]

        for l in alpha_c:
            # GET NUM OF PAGES (THERE ARE 25 RESULTS PER PAGE)
            def get_num_pages():
                agentlist = requests.get(DATA_LOCATION,
                                         params={'NAV':'1','LicenseeName':l,},
                                         headers=UA)
                agentsoup=BeautifulSoup(agentlist.text)
                table = agentsoup.find('table')
                rows = table.findAll('tr')
                for rowcount, tr in enumerate(rows):
                    row = tr.findAll('a',text=True)

                    if rowcount == 1:
                        string_parts = row[3].split(' ')
                        totalnum = string_parts[4]
                        num_of_pages = ceil(float(totalnum)/float(25))
                        print "{0} pages".format(num_of_pages)
                        return num_of_pages


            for p in enumerate(range(int(get_num_pages())),1):
                time.sleep(2)
                agentlist = requests.get(DATA_LOCATION,
                                         params={'NAV':'{0}'.format(p[0]),'LicenseeName':l,},
                                         headers=UA)
                agentsoup=BeautifulSoup(agentlist.text)
                table = agentsoup.find('table')
                rows = table.findAll('tr')

                for rowcount, tr in enumerate(rows):
                    row = tr.findAll('a',text=True)

                    clean_agt_id = row[0].strip()
                    clean_title = row[1].strip()
                    # Logic to pull populated titles and licenses
                    if clean_title != 'Name':
                        if clean_title:
                            try:
                                agt = Agent.objects.get(license_id=clean_agt_id)
                                print 'Already got agt'
                            except Agent.DoesNotExist:
                                agt = Agent(
                                    title = clean_title,
                                    full_name = clean_title,
                                    license_id = clean_agt_id,
                                )
                                agt.save()
                                print 'Added agt {0}, {1}'.format(clean_agt_id, clean_title)
            #                    print rowcount, clean_agt_id, clean_title, row[2], row[3]

                print 'Page {0} Done -------------------------------------------------------'.format(p[0])

        print 'Done Getting All -------------------------------------------------------'









        


  