from django.core.management.base import BaseCommand, CommandError
from BeautifulSoup import BeautifulSoup
from agent.models import Agent
import urllib2
import datetime
import pprint
from math import ceil
import time
import requests
from mezzanine.utils.urls import slugify
from settings import UA, DATA_LOCATION

class Command(BaseCommand):
    help = 'Get REA'
    def handle(self, *args, **options):


        all_agents = Agent.objects.filter(id__gte=186777)
#        all_agents = Agent.objects.all()

        agent_dict = {
            
#            'License Type:':'',
#            'Name:':'',
#            'Mailing Address:':'',
#            'License ID:':'',
#            'Expiration Date:':'',
#            'License Status':'',
#            'Salesperson License Issued':'',
#            'Corporation License Issued:':'',
#            'Broker License Issued':'',
#            'Former Name(s):':'',
#            'Employing Broker:':'',
#            'Main Office:':'',
#            'DBA':'',
#            'Branches:':'',
#            'Affiliated Licensed Corporation(s):':'',
#            'Comment':'',
        }

        errcount = 0
        concat_value = []
        for a in all_agents:
            time.sleep(2)

#            BROKER
#            agent_raw_data = requests.get('http://www2.dre.ca.gov/PublicASP/pplinfo.asp',
#                                             params={'License_id':'00811105',},
#                                             headers=UA)

##            SALESPERSON
#            agent_raw_data = requests.get('http://www2.dre.ca.gov/PublicASP/pplinfo.asp',
#                                             params={'License_id':'01027681',},
#                                             headers=UA)

#            CORP
#            agent_raw_data = requests.get('http://www2.dre.ca.gov/PublicASP/pplinfo.asp',
#                                             params={'License_id':'01154618',},
#                                             headers=UA)

#            ALL
            agent_raw_data = requests.get(DATA_LOCATION,
                                             params={'License_id':a.license_id,},
                                             headers=UA)

            agentsoup=BeautifulSoup(agent_raw_data.text)
    #        print agentsoup.prettify()

            try:
                table = agentsoup.find('table')
                rows = table.findChildren(['th', 'tr'])

                for rownum, row in enumerate(rows):
                    cells = row.findChildren('td')
                    agent_attribute = cells[0].findAll('font', text=True)
                    agent_attribute_value = cells[1].findAll('font', text=True)

                    try:
                        concat_value = []
                        agent_dict[agent_attribute[0]] = agent_attribute_value
                        errcount = 0
                    except IndexError:
                        errcount += 1
                        cell_header = rows[rownum - errcount].findChildren('td')
                        agent_attribute = cell_header[0].findAll('font', text=True)
                        concat_value.append(agent_attribute_value)
                        agent_dict[agent_attribute[0]] = [cell_header[1].findAll('font', text=True)] + concat_value

                if agent_dict['License Type:'][0] == "SALESPERSON":
                    try:
                        try:
                            name_parts = agent_dict['Name:'][0].split(',')
                            city_state_parts = agent_dict['Mailing Address:'][1].split(',')
                            state_zip_parts = city_state_parts[1].split(' ')
                            print "License Type", agent_dict['License Type:'][0].strip()
                            print "Full name",  agent_dict['Name:'][0].strip()
    #                        print "First Name", name_parts[1].strip()
    #                        print "Last Name", name_parts[0].strip()
    #                        print "Mailing Addr", agent_dict['Mailing Address:'][0].strip()
    #                        print "City", city_state_parts[0].strip()
    #                        print "State", state_zip_parts[1].strip()
    #                        print "zip", state_zip_parts[3].strip()
    #                        print "Lic ID", agent_dict['License ID:'][0].strip()
    #                        print "Sales Lic Issued:", agent_dict['Salesperson License Issued'][0].strip()
    #                        print "Lic Expiration:", agent_dict['Expiration Date:'][0].strip()
    #                        print "Lic Status", agent_dict['License Status'][0].strip()
    #                        print "Former Name", agent_dict['Former Name(s):']
                            if len(agent_dict['Employing Broker:']) > 1:
                                employing_broker = agent_dict['Employing Broker:'][1].strip()
                            else:
                                employing_broker = 'No Employing Broker'
    #                        print "Employing Broker", employing_broker
    #                        print "Comments", agent_dict['Comment']

                            a.title = '{0} {1} Real Estate Agent {2} {3}'.format(name_parts[1].strip(),
                                                           name_parts[0].strip(),
                                                           city_state_parts[0].strip(),
                                                           state_zip_parts[1].strip())
                            a.slug = slugify(a.title)
                            a.full_name = agent_dict['Name:'][0].strip()
                            a.first_name = name_parts[1].strip()
                            a.last_name = name_parts[0].strip()
                            a.mailing_address = agent_dict['Mailing Address:'][0].strip()
                            a.mailing_city = city_state_parts[0].strip()
                            a.mailing_state = state_zip_parts[1].strip()
                            a.slugged_city = city_state_parts[0].strip()
                            a.slugged_state = state_zip_parts[1].strip()
                            a.mailing_zip = state_zip_parts[3].strip()
                            a.license_type = agent_dict['License Type:'][0].strip()
                            a.salesperson_license_issue_date = agent_dict['Salesperson License Issued'][0].strip()
                            a.license_status = agent_dict['License Status'][0].strip()
                            a.license_expiration_date = agent_dict['Expiration Date:'][0].strip()
                            a.employing_broker = employing_broker
                            a.former_names = str(agent_dict['Former Name(s):'])
                            a.public_comment = str(agent_dict['Comment'])
                            a.save()
                            agent_dict.clear()
                        except IndexError, e:
                            name_parts = agent_dict['Name:'][0].split(',')
                            print "License Type", agent_dict['License Type:'][0].strip()
                            print "Full name",  agent_dict['Name:'][0].strip()
    #                        print "First Name", name_parts[1].strip()
    #                        print "Last Name", name_parts[0].strip()
    #                        print "Mailing Addr", agent_dict['Mailing Address:']
    #                        print "City", "N/A"
    #                        print "State", "N/A"
    #                        print "zip", "N/A"
    #                        print "Lic ID", agent_dict['License ID:'][0].strip()
    #                        print "Sales Lic Issued:", agent_dict['Salesperson License Issued'][0].strip()
    #                        print "Lic Status", agent_dict['License Status'][0].strip()
    #                        print "Lic Expiration:", agent_dict['Expiration Date:'][0].strip()
    #                        print "Former Name", agent_dict['Former Name(s):']
                            if len(agent_dict['Employing Broker:']) > 1:
                                employing_broker = agent_dict['Employing Broker:'][1].strip()
                            else:
                                employing_broker = 'No Employing Broker'
    #                        print "Employing Broker", employing_broker
    #                        print "Comments", agent_dict['Comment']

                            a.title = '{0} {1} Real Estate Agent'.format(name_parts[1].strip(),
                                                           name_parts[0].strip())
                            a.slug = slugify(a.title)
                            a.full_name = agent_dict['Name:'][0].strip()
                            a.first_name = name_parts[1].strip()
                            a.last_name = name_parts[0].strip()
                            a.mailing_address = agent_dict['Mailing Address:']
        #                    a.mailing_city = "N/A"
        #                    a.mailing_state = "N/A"
        #                    a.mailing_zip = "N/A"
                            a.license_type = agent_dict['License Type:'][0].strip()
                            a.salesperson_license_issue_date = agent_dict['Salesperson License Issued'][0].strip()
                            a.license_status = agent_dict['License Status'][0].strip()
                            a.license_expiration_date = agent_dict['Expiration Date:'][0].strip()
                            a.employing_broker = employing_broker
                            a.former_names = str(agent_dict['Former Name(s):'])
                            a.public_comment = str(agent_dict['Comment'])
                            a.save()
                            agent_dict.clear()
                    except KeyError, e:
                        print 'Keyerror for Salesperson'
                elif agent_dict['License Type:'][0] == "BROKER":
                    try:
                        name_parts = agent_dict['Name:'][0].split(',')
                        city_state_parts = agent_dict['Mailing Address:'][1].split(',')
                        state_zip_parts = city_state_parts[1].split(' ')

                        print "License Type", agent_dict['License Type:'][0].strip()
                        print "Full name",  agent_dict['Name:'][0].strip()
    #                    print "First Name", name_parts[1].strip()
    #                    print "Last Name", name_parts[0].strip()
    #                    print "Mailing Addr", agent_dict['Mailing Address:'][0].strip()
    #                    print "City", city_state_parts[0].strip()
    #                    print "State", state_zip_parts[1].strip()
    #                    print "zip", state_zip_parts[3].strip()
    #                    print "Lic ID", agent_dict['License ID:'][0].strip()

                        try:
                            salespersonlic =  agent_dict['Salesperson License Issued'][0].strip()
                        except KeyError:
                            salespersonlic =  "N/A"

    #                    print "Salesperson Lic Issued", salespersonlic
    #                    print "Broker Lic Issued", agent_dict['Broker License Issued'][0].strip()
    #                    print "Lic Status", agent_dict['License Status'][0].strip()
    #                    print "Lic Expiration:", agent_dict['Expiration Date:'][0].strip()
    #                    print "Former Name", agent_dict['Former Name(s):']
    #                    print "Main Office", ' '.join(agent_dict['Main Office:'])
    #                    print "DBA", agent_dict['DBA']
    #                    print "Branches", agent_dict['Branches:']
    #                    print "Affiliated Licensed Corps", agent_dict['Affiliated Licensed Corporation(s):']
    #                    print "Comments", agent_dict['Comment']

                        a.title = '{0} {1} Real Estate Broker {2} {3}'.format(name_parts[1].strip(),
                                                       name_parts[0].strip(),
                                                       city_state_parts[0].strip(),
                                                       state_zip_parts[1].strip())
                        a.slug = slugify(a.title)
                        a.full_name = agent_dict['Name:'][0].strip()
                        a.first_name = name_parts[1].strip()
                        a.last_name = name_parts[0].strip()
                        a.mailing_address = agent_dict['Mailing Address:'][0].strip()
                        a.mailing_city = city_state_parts[0].strip()
                        a.mailing_state = state_zip_parts[1].strip()
                        a.slugged_city = city_state_parts[0].strip()
                        a.slugged_state = state_zip_parts[1].strip()
                        a.mailing_zip = state_zip_parts[3].strip()
                        a.license_type = agent_dict['License Type:'][0].strip()
                        a.salesperson_license_issue_date = salespersonlic
                        a.broker_license_issue_date = agent_dict['Broker License Issued'][0].strip()
                        a.license_status = agent_dict['License Status'][0].strip()
                        a.license_expiration_date = agent_dict['Expiration Date:'][0].strip()
                        a.main_office_address = agent_dict['Main Office:']
                        a.dba = str(agent_dict['DBA'])
                        a.branches = str(agent_dict['Branches:'])
                        a.former_names = str(agent_dict['Former Name(s):'])
                        a.public_comment = str(agent_dict['Comment'])
                        a.save()
                        agent_dict.clear()
                    except IndexError:
                        name_parts = agent_dict['Name:'][0].split(',')
                        print "License Type", agent_dict['License Type:'][0].strip()
                        print "Full name",  agent_dict['Name:'][0].strip()
    #                    print "First Name", name_parts[1].strip()
    #                    print "Last Name", name_parts[0].strip()
    #                    print "Mailing Addr", agent_dict['Mailing Address:']
    #                    print "City", "N/A"
    #                    print "State", "N/A"
    #                    print "zip", "N/A"
    #                    print "Lic ID", agent_dict['License ID:'][0].strip()

                        try:
                            salespersonlic =  agent_dict['Salesperson License Issued'][0].strip()
                        except KeyError:
                            salespersonlic =  "N/A"

    #                    print "Sales Lic Issued:", salespersonlic
    #                    print "Broker Lic Issued", agent_dict['Broker License Issued'][0].strip()
    #                    print "Lic Status", agent_dict['License Status'][0].strip()
    #                    print "Lic Expiration:", agent_dict['Expiration Date:'][0].strip()
    #                    print "Former Name", agent_dict['Former Name(s):']
    #                    print "Main Office", ' '.join(agent_dict['Main Office:'])
    #                    print "DBA", agent_dict['DBA']
    #                    print "Branches", agent_dict['Branches:']
    #                    print "Affiliated Licensed Corps", agent_dict['Affiliated Licensed Corporation(s):']
    #                    print "Comments", agent_dict['Comment']

                        a.title = '{0} {1} Real Estate Broker'.format(name_parts[1].strip(),
                                                       name_parts[0].strip(),
                                                       )
                        a.slug = slugify(a.title)
                        a.full_name = agent_dict['Name:'][0].strip()
                        a.first_name = name_parts[1].strip()
                        a.last_name = name_parts[0].strip()
                        a.mailing_address = agent_dict['Mailing Address:'][0].strip()
    #                    a.mailing_city = "N/A"
    #                    a.mailing_state = "N/A"
    #                    a.mailing_zip = "N/A"
                        a.license_type = agent_dict['License Type:'][0].strip()
                        a.salesperson_license_issue_date = salespersonlic
                        a.broker_license_issue_date = agent_dict['Broker License Issued'][0].strip()
                        a.license_status = agent_dict['License Status'][0].strip()
                        a.license_expiration_date = agent_dict['Expiration Date:'][0].strip()
                        a.main_office_address = agent_dict['Main Office:']
                        a.dba = str(agent_dict['DBA'])
                        a.branches = str(agent_dict['Branches:'])
                        a.former_names = str(agent_dict['Former Name(s):'])
                        a.public_comment = str(agent_dict['Comment'])
                        a.save()
                        agent_dict.clear()
                elif agent_dict['License Type:'][0] == "CORPORATION":
                    try:
                        city_state_parts = agent_dict['Mailing Address:'][1].split(',')
                        state_zip_parts = city_state_parts[1].split(' ')

                        print "License Type", agent_dict['License Type:'][0].strip()
                        print "Name: ", agent_dict['Name:'][0].strip()
    #                    print "Full name",  agent_dict['Name:'][0].strip()
    #                    print "Mailing Addr", unicode(agent_dict['Mailing Address:'][0].strip().encode("utf-8"))
    #                    print "City", city_state_parts[0].strip()
    #                    print "State", state_zip_parts[1].strip()
    #                    print "zip", state_zip_parts[3].strip()
    #                    print "Lic ID", agent_dict['License ID:'][0].strip()
    #                    print "Corp License Issued", agent_dict['Corporation License Issued:'][0].strip()
    #                    print "Lic Status", agent_dict['License Status'][0].strip()
    #                    print "Lic Expiration:", agent_dict['Expiration Date:'][0].strip()
    #                    print "Former Name", agent_dict['Former Name(s):']
    #                    print "Main Office", ' '.join(agent_dict['Main Office:'])
    #                    print "Licensed Officer(s):", agent_dict['Licensed Officer(s):']
    #                    print "DBA", agent_dict['DBA']
    #                    print "Branches", agent_dict['Branches:']

                        try:
                            employed_agents = str(agent_dict['Salespersons:'])
                        except KeyError:
                            employed_agents = "N/A"

                        print "Employed Agents", employed_agents
                        print "Comments", agent_dict['Comment']

                        a.title = '{0} Real Estate Corporation'.format(agent_dict['Name:'][0].strip())
                        a.slug = slugify(a.title)
                        a.full_name = agent_dict['Name:'][0].strip()
    #                    a.first_name = "N/A"
    #                    a.last_name = "N/A"
                        a.mailing_address = agent_dict['Mailing Address:'][0].strip()
                        a.mailing_city = city_state_parts[0].strip()
                        a.mailing_state = state_zip_parts[1].strip()
                        a.slugged_city = city_state_parts[0].strip()
                        a.slugged_state = state_zip_parts[1].strip()
                        a.mailing_zip = state_zip_parts[3].strip()
                        a.license_type = agent_dict['License Type:'][0].strip()
                        a.corp_license_issue_date = agent_dict['Corporation License Issued:'][0].strip()
                        a.license_status = agent_dict['License Status'][0].strip()
                        a.license_expiration_date = agent_dict['Expiration Date:'][0].strip()
                        a.main_office_address = agent_dict['Main Office:']
                        a.dba = str(agent_dict['DBA'])
                        a.branches = str(agent_dict['Branches:'])
                        a.licensed_officers = str(agent_dict['Licensed Officer(s):'])
                        a.former_names = str(agent_dict['Former Name(s):'])
                        a.salespersons_employed = employed_agents
                        a.public_comment = str(agent_dict['Comment'])
                        a.save()
                        agent_dict.clear()
                    except IndexError:
                        print "License Type", agent_dict['License Type:'][0].strip()
                        print "Full name",  agent_dict['Name:'][0].strip()
    #                    print "Name: ", agent_dict['Name:'][0].strip()
    #                    print "Mailing Addr", unicode(agent_dict['Mailing Address:'][0].strip().encode("utf-8"))
    #                    print "City", "N/A"
    #                    print "State", "N/A"
    #                    print "zip", "N/A"
    #                    print "Lic ID", agent_dict['License ID:'][0].strip()
    #                    print "Corp License Issued", agent_dict['Corporation License Issued:'][0].strip()
    #                    print "Lic Status", agent_dict['License Status'][0].strip()
    #                    print "Lic Expiration:", agent_dict['Expiration Date:'][0].strip()
    #                    print "Former Name", agent_dict['Former Name(s):']
    #                    print "Main Office", ' '.join(agent_dict['Main Office:'])
    #                    print "Licensed Officer(s):", agent_dict['Licensed Officer(s):']
    #                    print "DBA", agent_dict['DBA']
    #                    print "Branches", agent_dict['Branches:']

                        try:
                            employed_agents = str(agent_dict['Salespersons:'])
                        except KeyError:
                            employed_agents = "N/A"

                        a.title = '{0} Real Estate Corporation'.format(agent_dict['Name:'][0].strip())
                        a.slug = slugify(a.title)
                        a.full_name = agent_dict['Name:'][0].strip()
    #                    a.first_name = "N/A"
    #                    a.last_name = "N/A"
                        a.mailing_address = agent_dict['Mailing Address:'][0].strip()
    #                    a.mailing_city = "N/A"
    #                    a.mailing_state = "N/A"
    #                    a.mailing_zip = "N/A"
                        a.license_type = agent_dict['License Type:'][0].strip()
                        a.corp_license_issue_date = agent_dict['Corporation License Issued:'][0].strip()
                        a.license_status = agent_dict['License Status'][0].strip()
                        a.license_expiration_date = agent_dict['Expiration Date:'][0].strip()
                        a.main_office_address = agent_dict['Main Office:']
                        a.dba = str(agent_dict['DBA'])
                        a.branches = str(agent_dict['Branches:'])
                        a.licensed_officers = str(agent_dict['Licensed Officer(s):'])
                        a.former_names = str(agent_dict['Former Name(s):'])
                        a.salespersons_employed = employed_agents
                        a.public_comment = str(agent_dict['Comment'])
                        a.save()
                        agent_dict.clear()
                else:
                    print 'Other type of agent', agent_dict['License Type:'][0].strip(), agent_dict['License ID:'][0].strip()

                print 'Saved Agent'

    #                agent_dict['Former Name(s):'] = '<li>{0}</li>'.format('</li><li>'.join([''.join(i).strip() for i in agent_dict['Former Name(s):']]))
                print '------------------------------------------------------------------------------------------------'
            except AttributeError, e:
                print "Attribute Error for {0}, {1}, Response status code {2}".format(a, e, agent_raw_data.status_code)

        print 'Done getting agents letter A'


















        


  