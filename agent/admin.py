from agent.models import *
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin

class AgentAdmin(DisplayableAdmin):

    fieldsets = [
        ("Title",                       {'fields': ['title']}),
        ("Published Date",              {'fields': ['publish_date']}),
        ("Published Status",            {'fields': ['status']}),
        ("Agent",            {'fields': ['user', 'profile_claimed', 'referring_agent', 'first_name',
                                         'last_name', 'full_name', 'mailing_address', 'mailing_city',
                                         'mailing_state', 'mailing_zip', 'slugged_city', 'slugged_state', 'license_id',
                                         'main_office_address', 'license_type', 'employing_broker', 'license_status','license_expiration_date',
                                         'salesperson_license_issue_date', 'broker_license_issue_date',
                                         'corp_license_issue_date', 'dba', 'branches',
                                         'affiliated_corporations','former_names',
                                         'licensed_officers', 'salespersons_employed','public_comment',
                                         'profile_image', 'about_me','specialties','certifications_awards','mls_association',
                                         'website', 'facebook', 'twitter', 'linkedin']}),
    ]


    list_display = ('title', 'user','referring_agent', 'first_name', 'last_name', 'full_name', 'mailing_city', 'mailing_state', 'license_type', 'license_status', 'status')
#    list_display_links = ('user',)
#    list_editable = ('is_order_closed',)
#    list_filter = ['order_submission_status','is_order_closed', 'publish_date',]
    search_fields = ['title',]
    date_hierarchy = 'publish_date'


class ActiveRegionAdmin(admin.ModelAdmin):
    list_display = ('region','country',)
    list_display_links = ('region',)
#    list_editable = ('email_address',)

admin.site.register(Agent, AgentAdmin)
admin.site.register(ActiveRegion, ActiveRegionAdmin)

