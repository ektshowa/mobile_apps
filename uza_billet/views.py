from django.shortcuts import render
from django.http import HttpResponse
from django.template.response import TemplateResponse
from rest_framework.response import Response




def index(request, template="uza_billet/index.html",
                                            extra_context=None):
    context = {"title": "Uza Billet"}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def login(request, template="uza_billet/login.html", extra_context=None):
    context = {}
    return TemplateResponse(request, template, context)

"""
def create_business(request, template="uza_billet/create_business.html"
                                                    , extra_context=None):
    context = {}
    address_data = {
        "street": request.POST.get("street"),
        "select_province": request.POST.get("select_province"),
        "select_city": request.POST.get("select_city"),
        "select_commune": request.POST.get("select_commune")
    }
    address = save_address(**address_data)
    print(address)
    return TemplateResponse(request, template, context)"""





