# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.http import int_to_base36
from django.utils.translation import ugettext, ugettext_lazy as _


class CensusAgentForm(forms.Form):
    team_zone_type = forms.CharField(label=_("Type de zone"),
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
                        attrs={"id": "team_commune"},
                        choices=(("", "Choisissez la Commune"),),),
                    required = True,
                    help_text=_("Entrez le nom de la commune"))
    team_territory = forms.CharField(label=_("Equipe territoire"),
                    widget=forms.Select(
                        attrs={"id": "team_territory"},
                        choices=(("", "Choisissez le Territoire"),),),
                    required = True,
                    help_text=_("Entrez le nom du territoire"))
    team_district = forms.CharField(label=_("Equipe District"),
                    widget=forms.Select(
                        attrs={"id": "team_district"},
                        choices=(("", "Choisissez le District"),),),
                    required = True,
                    help_text=_("Entrez le nom du dictrict"))
    first_name = forms.CharField(label=_("Prenom"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez le prenom"))
    last_name = forms.CharField(label=_("Nom"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez le Nom"))
    email = forms.CharField(label=_("Courriel"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez l'adresse courriel"))
    phone_number_1 = forms.CharField(label=_("Telephone Principal"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez votre telephone principal"))
    phone_number_2 = forms.CharField(label=_("Telephone secondaire"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez votre telephone secondaire"))
    password = forms.CharField(label=_("Mot de Passe"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez votre mot de passe"))
    password_confirm = forms.CharField(label=_("Confirmez le mot de passe"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez encore une fois le mot de passe"))
    agent_zone_type = forms.CharField(label=_("Type de zone"),
                    widget=forms.TextInput(),
                    required=True)
    select_province = forms.CharField(label=_("Province de l'agent"),
                    widget=forms.Select(
                        attrs={"id": "agent_province"},
                        choices=(("", "Choisissez la province"),),),
                    help_text=_("Choisissez la province"))
    select_city = forms.CharField(label=_("Ville"),
                    widget=forms.Select(
                        attrs={"id": "agent_city"},
                        choices=(("", "Choisissez la ville"),),))
    select_commune = forms.CharField(label=_("Commnue"),
                    widget=forms.Select(
                        attrs={"id": "agent_commune"},
                        choices=(("", "Choisissez la Commune"),),),
                    required = True,
                    help_text=_("Entrez le nom de la commune"))
    #select_territory = forms.CharField(label=_("Territoire"),
    #                widget=forms.Select(
    #                    attrs={"id": "agent_territory"},
    #                    choices=(("", "Choisissez le Territoire"),),),
    #                required = True,
    #                help_text=_("Entrez le nom du territoire"))
    #select_district = forms.CharField(label=_("Equipe District"),
    #                widget=forms.Select(
    #                    attrs={"id": "agent_district"},
    #                    choices=(("", "Choisissez le District"),),),
    #                required = True,
    #                help_text=_("Entrez le nom du dictrict"))
    neighborhood = forms.CharField(label=_("Quartier"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez le quartier"))
    avenue = forms.CharField(label=_("Avenue"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez l'avenue"))
    house_num = forms.CharField(label=_("Numero Residence"),
                    widget=forms.TextInput(),
                    required=True,
                    help_text=_("Entrez le numero"))