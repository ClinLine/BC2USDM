import requests
# try:
#     from html import unescape # python 3.4+
# except ImportError:
#     try:
#         from html.parser import HTMLParser # python 3.x (<3.4)
#     except ImportError:
#         from HTMLParser import HTMLParser # python 2.x
#     unescape = HTMLParser().unescape

# import json
from dotenv import dotenv_values
import pandas
import numpy as np

from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory


__secrets = dotenv_values(".env.dev")
__api_key = __secrets["PRIMARY_KEY"]
__headers = {
        "cache-Control": "no-cache",
        "api-key": __api_key,
        }



def get_latest_biomedical_concept_categories():
    url: str = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/categories"
    try:
        req = requests.get(url, headers=__headers, timeout=10)
        # unescaped = unescape(req.json())
        categories_json = req.json()["_links"]["categories"]
        
        # category_names = []
        # for category in categories:
        #     category_names.append(category["name"])
        # return category_names
        return categories_json
    except requests.Timeout as e:
        print(e)

# print(get_latest_biomedical_concept_categories())

def get_biomedical_concepts_list(category: str=None):
    endpoint: str = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts"
    url = endpoint
    if(category is not None and category != ""):
        if category in get_latest_biomedical_concept_categories():
            url = f"{endpoint}?category="
    try:
        req = requests.api.get(url, headers=__headers, timeout=10)
        bcs = req.json()["_links"]["biomedicalConcepts"]
        result = []
        for bc in bcs:
            element = (bc["title"],bc["href"].split("/")[-1], bc["href"],bc )
            result.append(element)
        return pandas.DataFrame(result, columns=["title","id","href","json"])
    except requests.Timeout as e:
        print(e)
    except requests.HTTPError as httpe:
        print(httpe)

def get_biomedical_concept_package_list():
    endpoint = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages"
    try:
        req = requests.api.get(endpoint,headers=__headers, timeout=10)
        # print(req.json()["_links"]["packages"])
        packages_data = req.json()["_links"]["packages"]
        result = []
        for package_data in packages_data:
            title = package_data["title"]
            href = package_data["href"]
            id_ = package_data["href"].split(sep="/")[-2] # sub-final substring
            result.append({"id":id,"title":title,"href":href,"json":package_data})
        return pandas.DataFrame(result)
    except Exception as e:
        print(e)

def get_biomedical_concept_list_for_package(package_identifier):
    endpoint = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages"

    if package_identifier is None or package_identifier == "":
        raise Exception("Please provide a package id (data)")
    if not np.where(get_biomedical_concept_package_list()["id"] == package_identifier):
        raise Exception("The provided package was not found")
    endpoint = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages/{package_identifier}/biomedicalconcepts"
    try:
        req = requests.api.get(endpoint, headers=__headers, timeout=10)
        if req.status_code == 422:
            raise Exception("Unprocessable Entity") 
        bcs = req.json()["_links"]["biomedicalConcepts"]
        biomedical_concepts = []
        for bc in bcs:
            id_ = bc["href"].split(sep="/")[-1] # final substring
            biomedical_concepts.append({"id":id_,"title":bc["title"], "href":bc["href"],"type":bc["type"],"json":bc})
        return pandas.DataFrame(biomedical_concepts)
    except Exception as e:
        print(e)

def get_latest_biomedical_concept(biomedical_concept_id):
    endpoint: str = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts/{biomedical_concept_id}"

    if biomedical_concept_id is None or biomedical_concept_id == "":
        raise Exception("please provide a valid id for the biomedical concept")

    try:
        req = requests.api.get(endpoint,headers=__headers, timeout=10)
        if req.status_code == 422:
            raise Exception("Unprocessable Entity")
        
        if req.status_code == 404:
            raise Exception(req.json()["detail"])
        json_data: str = req.json()
        print(req)
        raise NotImplementedError("Implementation of this endpoint will finish after a datatype has been made")
    except Exception as e:
        print(e)

# TODO implement this method
def get_biomedical_concept_for_package(biomedicalconcept_id: str, package_id: str):
    endpoint: str = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages/{package_id}/biomedicalconcepts/{biomedicalconcept_id}"

    if biomedicalconcept_id is None or biomedicalconcept_id == "":
        raise ValueError("Please provide a valid id for the Biomedical Concept")
    if package_id is None or package_id == "":
        raise ValueError("Please provide a valid package id")

    raise NotImplementedError("Getting a biomedical concept by package is not implemented yet")
