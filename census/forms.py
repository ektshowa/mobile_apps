# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.http import int_to_base36
from django.utils.translation import ugettext, ugettext_lazy as _


class CensusAgentForm(forms.Form):
    zone_type = forms.CharField(label=_("Type de zone"),
                    widget=forms.TextInput(),
                    required=True)
    team_province = forms.CharField(label=_("Equipe Province"),
                    widget=forms.Select(
                        attrs={"id": "team_province"},
                        choices=(("", "Choisissez la province"),),),
                    help_text=_("Choisissez la province"))
    team_city = forms.CharField(label=_("Equipe Ville"),
                    widget=forms.Select(
                        attrs={"id": "team_city"},
                        choices=(("", "Choisissez la ville"),),))
    team_commune = forms.CharField(label=_("Equipe Commnue"),
                    widget=forms.Select(
                        attrs={"id": "commune_choice"},
                        choices=(("", "Choisissez la Commune"),),),
                    required = True,
                    help_text=_("Entrez le nom de la commune"))