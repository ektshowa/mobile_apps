from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse


def index(request, template="uza_billet/index.html",
                                            extra_context=None):
    context = {"title": "Uza Billet"}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def login(request, template="uza_billet/login.html", extra_context=None):
    context = {}
    return TemplateResponse(request, template, context)

