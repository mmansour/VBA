from django.db import models
from mezzanine.core.models import Displayable, RichTextField
from mezzanine.generic.fields import CommentsField, RatingField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import autoslug


class ActiveRegion(models.Model):
    country = models.CharField(max_length=40, verbose_name="Country", blank=True, null=True)
    region = models.CharField(max_length=40, verbose_name="Region", blank=True, null=True)
    region_abbr = models.CharField(max_length=3, verbose_name="Region abbreviation", blank=True, null=True)
    slugged_region = autoslug.AutoSlugField(max_length=400, verbose_name="Slugged Region", blank=True, null=True)
    slugged_region_abbr = autoslug.AutoSlugField(max_length=40, verbose_name="Slugged Region Abbr", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slugged_region = self.region
        self.slugged_region_abbr = self.region_abbr
        super(ActiveRegion, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.region

class Agent(Displayable):
    user = models.OneToOneField(User, null=True, blank=True)
    referring_agent = models.ForeignKey(User, null=True, blank=True, related_name="referring_agent")
    full_name = models.CharField(max_length=400, verbose_name="Full Name", blank=True, null=True)
    first_name = models.CharField(max_length=400, verbose_name="First Name", blank=True, null=True)
    last_name = models.CharField(max_length=400, verbose_name="Last Name", blank=True, null=True)
    mailing_address = models.CharField(max_length=400, verbose_name="Mailing Address", blank=True, null=True)
    mailing_city = models.CharField(max_length=400, verbose_name="Mailing City", blank=True, null=True)
    mailing_state = models.CharField(max_length=400, verbose_name="Mailing State", blank=True, null=True)
    mailing_zip = models.CharField(max_length=400, verbose_name="Mailing Zipcode", blank=True, null=True)
    slugged_city = autoslug.AutoSlugField(max_length=400, verbose_name="Slugged City", blank=True, null=True)
    slugged_state = autoslug.AutoSlugField(max_length=400, verbose_name="Slugged State", blank=True, null=True)
    license_id = models.CharField(max_length=400, verbose_name="License ID", blank=True, null=True)
    license_type = models.CharField(max_length=400, verbose_name="License Type", blank=True, null=True)
    license_status = models.CharField(max_length=400, verbose_name="License Status", blank=True, null=True)

    # OLD
    license_expiration_date = models.CharField(max_length=400, verbose_name="License Expiration Date", blank=True, null=True)
    salesperson_license_issue_date = models.CharField(max_length=400, verbose_name="Salesperson License Issue Date", blank=True, null=True)
    broker_license_issue_date = models.CharField(max_length=400, verbose_name="Broker License Issue Date", blank=True, null=True)
    corp_license_issue_date = models.CharField(max_length=400, verbose_name="Corporate License Issue Date", blank=True, null=True)
    # END OLD

    license_issue_date = models.DateTimeField(blank=True, null=True)
    license_exp_date = models.DateTimeField(blank=True, null=True)
    main_office_address = models.CharField(max_length=400, verbose_name="Main Office Address", blank=True, null=True)
    employing_broker = models.CharField(max_length=400, verbose_name="Employing Broker", blank=True, null=True)
    branches = models.TextField(verbose_name="Branches", blank=True, null=True)
    dba = models.TextField(verbose_name="DBA", blank=True, null=True)
    affiliated_corporations = models.TextField(verbose_name="Affiliated Corporations", blank=True, null=True)
    licensed_officers = models.TextField(verbose_name="Licensed Officers", blank=True, null=True)
    former_names = models.TextField(verbose_name="Former Names", blank=True, null=True)
    salespersons_employed = models.TextField(verbose_name="Salespersons Employed", blank=True, null=True)
    public_comment = models.TextField(verbose_name="Public Comments", blank=True, null=True)

#    Fields that can be modified by agents:
    profile_image = models.ImageField(upload_to="uploads", blank=True, default='uploads/default.png')
    hero_image = models.ImageField(upload_to="uploads", blank=True, default='uploads/default-real-estate-hero.jpg')
    about_me = models.TextField(verbose_name="About Me", blank=True, null=True)
    specialties = models.TextField(verbose_name="Specialties", blank=True, null=True)
    certifications_awards = models.TextField(verbose_name="Certifications and Awards", blank=True, null=True)
    mls_association = models.CharField(max_length=400, verbose_name="MLS Association", blank=True, null=True)
    website = models.URLField(max_length=400, verbose_name="Website", blank=True, null=True)
    facebook = models.URLField(max_length=400, verbose_name="Facebook", blank=True, null=True)
    twitter = models.URLField(max_length=400, verbose_name="Twitter", blank=True, null=True)
    linkedin = models.URLField(max_length=400, verbose_name="Linked In", blank=True, null=True)
    youtube = models.URLField(max_length=400, verbose_name="Youtube Channel", blank=True, null=True)
    pinterest = models.URLField(max_length=400, verbose_name="Youtube Channel", blank=True, null=True)
    profile_claimed = models.BooleanField(verbose_name="Agent claimed profile?", blank=True, default=False)

    bar_graph_one = models.IntegerField(verbose_name="Residential", blank=True, default=5,
                                        help_text="Rate your skill level from 1 to 10. 10 is the most skilled")
    bar_graph_two = models.IntegerField(verbose_name="Commercial", blank=True, default=5,
                                        help_text="Rate your skill level from 1 to 10. 10 is the most skilled")
    bar_graph_three = models.IntegerField(verbose_name="Land", blank=True, default=5,
                                          help_text="Rate your skill level from 1 to 10. 10 is the most skilled")
    bar_graph_four = models.IntegerField(verbose_name="Investors", blank=True, default=5,
                                         help_text="Rate your skill level from 1 to 10. 10 is the most skilled")
    #
    # show_education = models.BooleanField(default=True)
    # show_bar_graph_skillset = models.BooleanField(default=True)
    # show_state_reported_comments = models.BooleanField(default=True)
    # show_certification_and_awards = models.BooleanField(default=True)
    #
    # education_start_year = models.CharField(max_length=4, verbose_name="Start Year", blank=True, null=True)
    # education_end_year = models.CharField(max_length=4, verbose_name="End Year", blank=True, null=True)
    # education_University = models.CharField(max_length=100, verbose_name="College / University", blank=True, null=True)
    # education_degree = models.CharField(max_length=100, verbose_name="Degree Earned", blank=True, null=True)
    # education_awards = models.CharField(max_length=100, verbose_name="Awards / Accolades", blank=True, null=True)

    def get_clean_main_office_address(self):
        if self.main_office_address:
            return "<address><small>{0}</small></address>".format(self.main_office_address.replace('u', '')
                                                          .replace('[', '').replace("'", '').replace(']', ''))
        else:
            return "No office address reported for this licensee"

    def get_clean_dba(self):
        if self.dba:
            return self.dba\
                .replace("[[u'",'[')\
                .replace("']]", "]").replace("u'","")
        else:
            return "No DBAs reported for this licensee."

    def get_clean_branches(self):
        if self.branches:
            thebranches = self.branches\
                .replace("[[u'", '[')\
                .replace("']]", "]").replace("u'", "")
            if thebranches == "[NO CURRENT BRANCHES']":
                thebranches = "No branches reported for this licensee."
            return thebranches
        else:
            return "No branches reported for this licensee."

    def get_clean_affiliated_corps(self):
        if self.affiliated_corporations:
            aff_corps = self.affiliated_corporations\
                .replace("[[u'",'[')\
                .replace("']]", "]").replace("u'","")
        else:
            aff_corps = "No affiliated corporations reported for this licensee."
        return aff_corps

    def get_clean_public_comments(self):
        if self.public_comment:
            pub_com = self.public_comment\
                .replace("[[u'",'[')\
                .replace("']]", "]").replace("u'", "")
            if pub_com == "[NO DISCIPLINARY ACTION'], [>>>> Public information request complete <<<<]":
                pub_com = "No public comments or public disciplinary action reported"
            return pub_com
        else:
            return "No public / state department comments or public disciplinary action reported"


    def get_clean_salesperson_employing_broker(self):
        if self.employing_broker:
            employing_broker_data = Agent.objects.get(license_id=self.employing_broker)
            return "{0}: License ID {1}"\
                .format(employing_broker_data.full_name, employing_broker_data.license_id)
           
    def get_clean_salesperson_employing_broker_url(self):
        if self.employing_broker:
            employing_broker_data = Agent.objects.get(license_id=self.employing_broker)
            return "agent/{0}/{1}".format(employing_broker_data.slug, employing_broker_data.license_id)

    def get_data_for_license_type(self):

        if self.license_type == "SALESPERSON" or self.license_type == "Salesperson":
            license_type_dict = {'license_type': 'Agent'}
        if self.license_type == "BROKER" or self.license_type == "Broker":
            license_type_dict = {'license_type': 'Broker'}
        if self.license_type == "CORPORATION" or self.license_type == "Corporation":
            license_type_dict = {'license_type': 'Corporation'}
        if self.license_type == "Officer":
            license_type_dict = {'license_type': 'Officer'}

        return license_type_dict

    def get_agents_for_employing_broker(self):
        return Agent.objects.filter(employing_broker=self.license_id)

    @models.permalink
    def get_absolute_url(self):
        return ('agent.views.agent_details', [self.slug, self.license_id])

    def __unicode__(self):
        return self.title


class AgentLead(models.Model):
    agent = models.ForeignKey(Agent, null=True, blank=True)
    name = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email_address = models.EmailField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=500, default='Lead from Real Estate Agent Lookup')
    message = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.subject
