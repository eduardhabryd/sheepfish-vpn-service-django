from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectMultiple

from vpn_app.models import Site


class SiteSearchForm(forms.Form):
    site_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by site name",
                "class": "form-control me-3",
                "type": "search",
                "aria-label": "Search",
            }
        ),
    )


class SiteCreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class SiteUpdateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
