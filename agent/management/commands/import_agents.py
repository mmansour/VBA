from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from agent.models import Agent
import urllib2
import csv
import re
import time
from urlparse import urlparse
import datetime

from settings import TEMPLATE_DIRS

class Command(BaseCommand):
    help = 'Import local data to production'
    def handle(self, *args, **options):

#         reader = csv.reader(open('/users/mattmansour/django/sites/dev/socialtracker/docs/social-tracker-raw-data.csv', 'rU'), delimiter=',')
#         reader = csv.reader(open('/home/mattym/webapps/vba/docs/CurrList_Comma_Delimited.txt', 'rU'), delimiter=',')
        reader = csv.reader(open(TEMPLATE_DIRS[0] + '/agents.csv', 'rU'), delimiter=',')
        reader.next() # Skip first line
#        col[3] title
#        col[6] desc
#        col[8] status
#        col[9] pubdate
#        col[14] full name
#        col[15] first name
#        col[16] last name
#        col[17] mailing address
#        col[18] mailing city
#        col[19] mailing state
#        col[20] mailing zip
#        col[21] slugged city
#        col[22] slugged state
#        col[23] license id
#        col[24] license type
#        col[25] license status
#        col[26] license expiration
#        col[27] salesperson license issue date
#        col[28] broker license issue date
#        col[29] corp license issue date
#        col[30] main office address
#        col[31] employing broker
#        col[32] branches
#        col[33] dba
#        col[34] affiliated corps
#        col[35] licensed officers
#        col[36] former names
#        col[37] salespersons employed
#        col[38] public comments                 


        for col in reader:
#            print col[17],
            try:
                agent = Agent.objects.get(license_id=col[23])
                print 'Agent exists: {0}'.format(agent.title)
            except Agent.DoesNotExist:
                agent = Agent(
                    title = col[3],
                    status = col[8],
#                    publish_date = col[9],
                    full_name = col[14],
                    first_name = col[15],
                    last_name = col[16],
                    mailing_address = col[17],
                    mailing_city = col[18],
                    mailing_state = col[19],
                    mailing_zip = col[20],
                    slugged_city = col[21],
                    slugged_state = col[22],
                    license_id = col[23],
                    license_type = col[24],
                    license_status = col[25],
                    license_expiration_date = col[26],
                    salesperson_license_issue_date = col[27],
                    broker_license_issue_date = col[28],
                    corp_license_issue_date= col[29],
                    main_office_address= col[30],
                    employing_broker= col[31],
                    branches = col[32],
                    dba = col[33],
                    affiliated_corporations= col[34],
                    licensed_officers = col[35],
                    former_names = col[36],
                    salespersons_employed= col[37],
                    public_comment = col[38],
                )
                agent.save()

                print "Created Agent: {0}".format(agent)

        print 'Finished importing agents'






  