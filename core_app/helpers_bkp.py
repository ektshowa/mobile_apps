# -*- coding: utf-8 -*-
from django.conf import settings
from sorl.thumbnail import get_thumbnail
from django.db.models.fields.files import ImageFieldFile
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
import sys
import traceback
import os
import csv
import errno
import io, PyPDF2
from builtins import FileNotFoundError
import boto3
from boto3.exceptions import S3UploadFailedError
import requests, bs4
from .models import Region, City, Commune, Country
import string
from random import *

#from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
#from django.core.files import File


# The file_type parameter is "file" or "image"
# This is used to set the upload folder
def set_uploaded_folder(file_type):
    folder = ""
    if file_type == "image":
        folder = settings.CHAINEDULIVRE_IMAGES_FOLDER
    elif file_type == "file":
        folder = settings.CHAINEDULIVRE_PRODUCTS_FOLDER
    return folder


def cast_to_num(data):
    """Use to convert the input to an int checking
        by the way that the input is ok.
    """
    try:
        return int(data)
    except Exception:
        return None


def generate_random_password():
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    return password


def handle_uploaded_file(f, file_type):
    if f:
        try:
            file_path = set_uploaded_folder(file_type) + "/" + f.name
            with open(file_path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            return f.name
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            return None
    return None


def get_thumbnail_for_quality(image, geometry_string, crop, quality):
    if isinstance(quality, int):
        im = get_thumbnail(image, geometry_string, crop, quality)
    else:
        im = get_thumbnail(image, geometry_string)
    return im


def get_image_thumbnail(image, geometry_string=None, crop=None, quality=None):
    if not geometry_string:
            raise Exception("Get Image Thumbnail: No Geometry_String provided")

    im = None

    if isinstance(image, ImageFieldFile):
        try:
            im = get_thumbnail_for_quality(image, geometry_string, crop,
                                                                        quality)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)

    elif isinstance(image, str):
        #image_path = "%s/%s" % (settings.CHAINEDULIVRE_IMAGES_FOLDER, image)
        image_path = \
        "https://stdominfoservices.s3.us-east-2.amazonaws.com/static/media/uploads/images/chainedulivre/%s" % image
        im = None
        if os.path.isfile(image_path):
            try:
                im = get_thumbnail_for_quality(image_path, geometry_string,
                                                                crop, quality)
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
    return im


def set_bucket_prefix(file_type=""):
    """parm file_type is image for all image files"""
    prefix = ""
    # The prefix values set below have to move to settings
    if file_type == "image":
        prefix = "static/media/uploads/images/chainedulivre"
    else:
        prefix = "static/media/uploads/products/chainedulivre"
    return prefix


def get_s3_resource():
    session = boto3.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                            )
    s3 = session.resource("s3")
    return s3


def upload_file_to_s3(aws_access_key_id, aws_secret_access_key, bucket,
                                                uploaded_file, content_type=None):

    result = {"success": None, "cause": ""}
    prefix = set_bucket_prefix(content_type)
    session = boto3.Session(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)
    s3 = session.resource("s3")
    #file_name_parts = uploaded_file.split("/")
    #key = file_name_parts[len(file_name_parts) - 1]

    full_key_name = prefix + "/" + uploaded_file.name

    print("UPLOADED FILE FULL NAME")
    print(full_key_name)

    try:
        s3.Bucket(bucket).put_object(Key=full_key_name, Body=uploaded_file)
        result["success"] = True
    except S3UploadFailedError:
        result["success"] = False
        result["cause"] = "failed upload"
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    except:
        result["success"] = False
        result["cause"] = "other"
        print("Unexpected error: ", sys.exc_info()[0])
        raise

    return result


def load_countries_from_html_page(page_link):
    page = requests.get(page_link)
    page_text = bs4.BeautifulSoup(page.text)
    rows = page_text.select("table#codelist tr")
    for row in rows:
        country = Country()
        td_list = row.find_all("td")
        if td_list:
            country.english_name = td_list[1].get_text()
            country.code = td_list[3].get_text()
            print("PRINTING COUNTRIES")
            print(country.english_name)
            country.save()
    return


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
        return None


def load_wiki_provinces():
    province_file = open("localcore/congo_provinces.html")
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


def get_nontranslated_text(in_text):
    if not isinstance(in_text, str):
        with translation.override('en'):
            out_text = str(in_text)
    else:
        out_text = in_text
    return out_text


def set_message_text(in_message, in_text):
    out_message = get_nontranslated_text(in_message)
    text = get_nontranslated_text(in_text)
    out_message += text
    out_message = _(out_message)
    return out_message


def get_product_file_from_s3(file_name):
    prefix = set_bucket_prefix()
    file_full_name = prefix + "/" + file_name
    print("IN GET_PRODUCT_FILE_FROM_S3")
    print("PREFIX: %s FILE_FULL_NAME: %s" % (prefix, file_full_name))
    s3 = get_s3_resource()
    file_obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, file_full_name).get()
    return file_obj


def get_pdf_from_s3_object(s3_object):
    file_content = s3_object["Body"].read()
    print(len(file_content))
    pdf_content = io.BytesIO(file_content)
    print(type(pdf_content))
    pdf_reader = PyPDF2.PdfFileReader(pdf_content)
    print(type(pdf_reader))
    pdf_writer = PyPDF2.PdfFileWriter()
    pdf_output_file = open("newpdfoutfile.pdf", "wb")

    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        pdf_writer.addPage(page_obj)

    pdf_writer.write(pdf_output_file)
    return pdf_output_file


def output_pdf_test():
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100,100, "Hello world")
    can.showPage()
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    # read your existing PDF
    f = open("/home/ektshowa/Documents/jj_piece_estimate.pdf", "rb")
    existing_pdf = PyPDF2.PdfFileReader(f)
    output = PyPDF2.PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file

    outfile = open("/home/ektshowa/Documents/jj_piece_newpdf.pdf", "wb")
    output.write(outfile)


def download_file_on_local_storage(aws_access_key_id, aws_secret_access_key,
                                                    aws_storage_bucket_name):
    session = boto3.Session(aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
    s3 = session.resource("s3")
    s3.Bucket(aws_storage_bucket_name).download_file(
                        "media/uploads/images/chainedulivre/logo.png",
                        "/home/ektshowa/Downloads/s3_test_download_file.png")


def merge_dictionaries(dict1, dict2):
    return (dict1.update(dict2))

