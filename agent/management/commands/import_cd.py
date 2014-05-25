import csv
import os

from django.core.management.base import BaseCommand, CommandError

from mezzanine.utils.urls import slugify

from agent.models import Agent

from settings import TEMPLATE_DIRS, PROJECT_ROOT

class Command(BaseCommand):
    help = 'Import local data to production'

    def handle(self, *args, **options):

        reader = csv.reader(open('{0}/docs/agents/CurrList_Comma_Delimited6.txt'.format(PROJECT_ROOT), 'r'), delimiter=',')
#         reader = csv.reader(open('/home/mattym/webapps/vba/docs/CurrList_Comma_Delimited.txt', 'rU'), delimiter=',')
#         reader = csv.reader(open(TEMPLATE_DIRS[0] + '/agents.csv', 'rU'), delimiter=',')
        reader.next() # Skip first line
#        col[1] lastname_primary or corp name
#        col[2] firstname_secondary
#        col[3] name_suffix
#        col[4] lic_number
#        col[5] lic_type
#        col[6] lic_status
#        col[7] lic_effective_date
#        col[8] lic_expiration_date
#        col[9] rel_lic_number  (employing broker of agent etc...)
#        col[10] empl_lastname_primary  (agent's employer last name / Corp name)
#        col[11] empl_firstname_secondary (agent's employer first name / Corp name)
#        col[12] empl_name_suffix
#        col[13] officerlastname
#        col[14] officerfirstname
#        col[15] officersuffixname
#        col[16] rel_lic_type (employer type of license)
#        col[17] address_1
#        col[18] address_2
#        col[19] city
#        col[20] state
#        col[21] zip_code
#        col[22] foreign_nation
#        col[23] foreign_postal_info
#        col[24] county_code
#        col[25] county_name
#        col[26] restricted_flag
#        col[27] misc_indicator
#        col[28] ethics_and_agency_ind

        from dateutil import parser


        for col in reader:
            dt_lic_effective_date = parser.parse(col[7])
            dt_lic_expiration_date = parser.parse(col[8])

            if col[5] != 'Salesperson':
                clean_lic_type = col[5]
            else:
                clean_lic_type = "Agent"

            the_title = '{0} {1} Real Estate {2} {3} {4}'.format(col[2],
                                                                 col[1],
                                                                 clean_lic_type,
                                                                 col[19],
                                                                 col[20]
                                                                 )

            full_name = "{0} {1} {2}".format(col[2], col[1], col[3])

            full_name_officer = "{0} {1} {2}".format(col[14], col[13], col[15])

            employer = "{0} {1}".format(col[10], col[11])

            try:
                agent = Agent.objects.get(license_id=col[4])
                agent.in_sitemap = False
                agent.licence_type = col[5]
                agent.license_issue_date = dt_lic_effective_date
                agent.license_exp_date = dt_lic_expiration_date
                agent.employing_broker = col[9]
                agent.licensed_officers = unicode(full_name_officer.strip()).encode("utf-8")
                agent.save()
                print 'Agent exists: {0}'.format(agent.title)
            except Agent.DoesNotExist:
                agent = Agent.objects.create(
                    title=unicode(the_title).encode("utf-8"),
                    slug=slugify(unicode(the_title).encode("utf-8")),
                    status=2,
                    full_name=unicode(full_name.strip()).encode("utf-8"),
                    first_name=unicode(col[2].strip()).encode("utf-8"),
                    last_name=unicode(col[1].strip()).encode("utf-8"),
                    mailing_address=unicode(col[17]).encode("utf-8"),
                    licensed_officers=unicode(full_name_officer.strip()).encode("utf-8"),
                    mailing_city=col[19],
                    mailing_state=col[20],
                    mailing_zip=col[21],
                    slugged_city=col[19],
                    slugged_state=col[20],
                    license_id=col[4],
                    license_type=col[5],
                    license_status=col[6],
                    license_issue_date=dt_lic_effective_date,
                    license_exp_date=dt_lic_expiration_date,
                    employing_broker=unicode(employer).encode("utf-8"),
                    in_sitemap=False,


            #        # affiliated_corporations= col[34],
            #        # licensed_officers = col[35]
            #         # main_office_address= col[30],
            #         # branches = col[32],
            #         # dba = col[33],
            #         # former_names = col[36],
            #         # salespersons_employed= col[37],
            #         # public_comment = col[38],

                )
                print "Created Agent: {0}".format(unicode(agent).encode("utf-8"))

        print 'Finished importing agents'






  