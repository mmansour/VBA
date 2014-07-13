from django import forms
from haystack.forms import SearchForm


class ClaimForm(forms.Form):
    license_id = forms.CharField(required=True,)


class NotesSearchForm(SearchForm):
    def no_query_found(self):
        return self.searchqueryset.all()


class AgentProfileEditForm(forms.Form):
    about_me = forms.CharField(widget=forms.Textarea, required=False,)
    specialties = forms.CharField(widget=forms.Textarea, required=False,)
    certifications_awards = forms.CharField(widget=forms.Textarea, required=False,)
    mls_association = forms.CharField(required=False,)
    website = forms.URLField(required=False,)
    facebook = forms.URLField(required=False,)
    youtube = forms.URLField(required=False,)
    twitter = forms.URLField(required=False,)
    linkedin = forms.URLField(required=False,)
    pinterest = forms.URLField(required=False,)
    residential_skills = forms.IntegerField(required=False, min_value=1, max_value=10,
                                            help_text="From 1 to 10 rate your skill level in residential real estate. "
                                            "10 indicates the most skilled.")
    commercial_skills = forms.IntegerField(required=False, min_value=1, max_value=10,
                                           help_text="From 1 to 10 rate your skill level in commercial real estate. "
                                           "10 indicates the most skilled.")
    land_skills = forms.IntegerField(required=False, min_value=1, max_value=10,
                                     help_text="From 1 to 10 rate your skill level in land transactions. "
                                     "10 indicates the most skilled.")
    investor_skills = forms.IntegerField(required=False, min_value=1, max_value=10,
                                         help_text="From 1 to 10 rate your skill level in working with "
                                                   "real estate investors. 10 indicates the most skilled.")
    show_education = forms.BooleanField(initial=True, required=False)
    show_bar_graph_skillset = forms.BooleanField(initial=True, required=False)
    show_state_reported_comments = forms.BooleanField(initial=True, required=False)
    show_certification_and_awards = forms.BooleanField(initial=True, required=False)

    education_start_year = forms.CharField(required=False,
                                           help_text="Enter year you started university. 4 digits e.g. 1995")
    education_end_year = forms.CharField(required=False,
                                         help_text="Enter year you graduated. 4 digits e.g. 1999")
    university = forms.CharField(required=False,)
    degree = forms.CharField(required=False,)
    awards = forms.CharField(required=False, help_text="Enter accolades, GPA, scholarships, etc...")


class AgentProfileImageForm(forms.Form):
    profile_image = forms.ImageField(required=False,)
    # profile_background_image = forms.ImageField(required=False,)


class AgentLeadCaptureForm(forms.Form):
    name = forms.CharField(required=True,)
    phone_number = forms.CharField(required=False,)
    email_address = forms.EmailField(required=True,)
    subject = forms.CharField(required=True,)
    message = forms.CharField(required=False, widget=forms.Textarea)
