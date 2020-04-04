# -*- coding: utf-8 -*-
from .models import Country
import csv

CSV_FILE_FULLNAME = \
        '/home/ektshowa/mobile_apps/mobile_apps/core_app/list_of_countries.csv'
CONTINENTS = ['America', 'Africa', 'Europe', 'Asia', 'Oceania']


def load_countries():
    csvFile = open(CSV_FILE_FULLNAME)
    csvReader = csv.reader(csvFile)

    for row in csvReader:
        row = row[0].split(";")
        #print(row)
        try:
            englishName = row[0].strip()
        except Exception:
            englishName = ""
        try:
            frenchName = row[1].strip()
        except Exception:
            frenchName = ""
        try:
            localName = row[2].strip()
        except Exception:
            localName = ""
        try:
            region = row[3].strip()
        except Exception:
            region = ""

        continent = ''
        for cont in CONTINENTS:
            if cont in region:
                continent = cont
                break
        
        country = Country(english_name=englishName,
                            french_name=frenchName,
                            local_name=localName,
                            region=region,
                            continent=continent)
        country.save()
        print(country.__dict__)

    csvFile.close()