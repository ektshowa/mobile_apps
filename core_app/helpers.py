from django.conf import settings
#from sorl.thumbnail import get_thumbnail
from django.db.models.fields.files import ImageFieldFile
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
import sys
import traceback
import os
import csv
import errno
#import io, PyPDF2
#from builtins import FileNotFoundError
#import boto3
#from boto3.exceptions import S3UploadFailedError
import requests, bs4
from .models import Region, City, Commune, Country
import string
from random import *

#from io import BytesIO
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter
#from django.core.files import File


def load_right_provinces(page_link):
    # The page used here is:
    # "http://www.congo-autrement.com/page/les-26-provinces-de-la-rdc/"
    module_dir = os.path.dirname(os.path.realpath(__file__))
    csv_file_fullname = os.path.join(module_dir, "right_provinces.csv")
    print("CSV FILE FULLNAME")
    print(csv_file_fullname)
    page = requests.get(page_link)
    page_text = bs4.BeautifulSoup(page.text)
    fieldnames = ["province", "chef_lieu"]
    resultset = []

    if csv_file_fullname:
        csv_file = open(csv_file_fullname, 'w', newline='')
        csv_writer = csv.DictWriter(csv_file,
                        fieldnames=fieldnames,
                        delimiter=';',
                        quoting=csv.QUOTE_ALL)
        csv_writer.writeheader()
        rows = page_text.select("table tbody tr")

        for row in rows:
            province_dict = {}
            td_list = row.find_all("td")
            if len(td_list) == 5:
                province = td_list[1].get_text().strip()
                chef_lieu = td_list[2].get_text().strip()
                csv_row = [province, chef_lieu]
                csv_row_dict = dict(zip(fieldnames, csv_row))
                csv_writer.writerow(csv_row_dict)
                province_dict["province"] = td_list[1].get_text().strip()
                province_dict["chef_lieu"] = td_list[2].get_text().strip()
                resultset.append(province_dict)
        return resultset

    else:
        return 
        

def load_wiki_provinces():
    province_file = open("core_app/congo_provinces.html")
    province_content = province_file.read()
    parsed_province = bs4.BeautifulSoup(province_content)
    rows = parsed_province.select("table.wikitable tbody tr")
    #module_dir = os.path.dirname(os.path.realpath(__file__))
    #csv_file_fullname = os.path.join(module_dir, "right_provinces.csv")
    resultset = []

    for row in rows:
        province_dict = {}
        td_list = row.find_all("td")
        if len(td_list) == 5:
            province_dict["district_or_city"] = td_list[0].get_text().strip()
            province_dict["type"] = td_list[1].get_text().strip()
            province_dict["province"] = td_list[3].get_text().strip()
            province_dict["territories_or_communes"] = td_list[4].get_text().strip()
        elif len(td_list) == 2:
            province_dict["district_or_city"] = td_list[0].get_text().strip()
            province_dict["type"] = "District"
            province_dict["province"] = "Kinshasa"
            province_dict["territories_or_communes"] = td_list[1].get_text().strip()
        resultset.append(province_dict)

    return resultset


def populate_provinces():
    right_provinces = load_right_provinces(
            "http://www.congo-autrement.com/page/les-26-provinces-de-la-rdc/")
    wiki_provinces = load_wiki_provinces()
    country = Country.objects.get(id=1)
    #print("Country")
    #print(country)

    for right_prov in right_provinces:
        other_prov_name = ""
        province = right_prov["province"]
        if province == "ImageHaut-Katanga":
            province = "Haut-Katanga"
        if province == "Kasaï":
            province = "Kasai"
            other_prov_name = "Kasaï"
        if province == "Kasaï-Central":
            province = "Kasai-Central"
            other_prov_name = "Kasaï-Central"
        if province == "Kasaï-Oriental":
            province = "Kasai-Oriental"
            other_prov_name = "Kasaï-Oriental"
        try:
            region = Region()
            region.country = country
            if other_prov_name:
                region.name = other_prov_name
            else:
                region.name = province
            region.save()
            #print("REGION")
            #print(region)
        except Exception:
            region = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
        if region:
            some_provs = [pro for pro in wiki_provinces if 'province' in pro and
                        pro['province'].lower() == province.lower()]
            for some_pro in some_provs:
                try:
                    city = City(
                            name=some_pro["district_or_city"],
                            city_type=some_pro["type"],
                            country=country,
                            region=region)
                    city.save()
                    #print("CITY")
                    #print(city)
                except Exception:
                    city = None
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_exception(exc_type, exc_value, exc_traceback)
                communes = some_pro["territories_or_communes"].split()
                if city:
                    for com in communes:
                        try:
                            commune = Commune(
                                    name=com,
                                    city=city)
                            commune.save()
                            #print("COMMUNE")
                            #print(commune)
                        except Exception:
                            commune = None
                            exc_type, exc_value, exc_traceback = sys.exc_info()
                            traceback.print_exception(exc_type, exc_value, exc_traceback)
    return len(right_provinces)
