from datetime import datetime
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

# from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory


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
        categories_json = req.json()["_links"]["categories"]
        return categories_json
    except requests.Timeout as e:
        print(e)


def get_biomedical_concepts_list(category: str=None, categories: list[str]=None):
    endpoint: str = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts"
    url = endpoint
    if(category is not None and category != ""): # TODO add else state
        if categories is None:
            categories = [c["name"] for c in get_latest_biomedical_concept_categories()]
        if category in categories:
            url = f"{endpoint}?category={category}"
        else:
            print("category not found!")
    else:
        print("Category can't be None or \"\"")
        raise ValueError(f"Proviced {category.__qualname__} can't be None or \"\"")
    
    try:
        req = requests.api.get(url, headers=__headers, timeout=10)
        if req.json()["_links"] is None:
            print("json:")
            print(req.json())
            AttributeError("Expected _links object not found")
            
        bcs = req.json()["_links"]["biomedicalConcepts"]
        return bcs
    except requests.Timeout as e:
        print(e)
    except requests.HTTPError as httpe:
        print(httpe)
    except Exception as e:
        now = datetime.now()
        file = open(f"ErrorLog_{now}.txt", "x+t",encoding="utf-8")
        file.write(f"{e.__cause__} while getting BiomedicalConcepts in category\n")
        print(f"{e.__cause__} while getting BiomedicalConcepts in category\n")
        file.write(f"File {__file__} in {__name__}")
        print(f"File {__file__} in {__name__}")
        for arg in e.args:
            print(f"\t{arg}")
            file.write(f"\t{arg}")
        print(e.__context__)
        file.write(e.__context__)
        file.close()

def get_biomedical_concept_package_list():
    endpoint = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages"
    try:
        req = requests.api.get(endpoint,headers=__headers, timeout=10)
        packages_data = req.json()["_links"]["packages"]
        result = []
        for package_data in packages_data:
            title = package_data["title"]
            href = package_data["href"]
            id_ = package_data["href"].split(sep="/")[-2] # sub-final substring
            result.append({"id":id_,"title":title,"href":href,"json":package_data})
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
        # return pandas.DataFrame(biomedical_concepts)
        return biomedical_concepts
    except Exception as e:
        print(e)

def get_latest_biomedical_concept(biomedical_concept_code):
    endpoint: str = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts/{biomedical_concept_code}"
    if biomedical_concept_code is None or biomedical_concept_code == "":
        raise ValueError("please provide a valid id for the biomedical concept")
    try:
        req = requests.api.get(endpoint,headers=__headers, timeout=10)
        if req.status_code == 422:
            raise Exception("Unprocessable Entity")
        if req.status_code == 404:
            print(f"request for bc with code: {biomedical_concept_code} resulted in a {req.status_code} error")
            raise Exception(req.json()["detail"])
            
        json_data = req.json()
    except Exception as e:
        print(f"API.getLatestBiomedicalConcept encountered an unexpected error: {e}")
    else: 
        return json_data

# TODO implement this method
def get_biomedical_concept_for_package(biomedicalconcept_id: str, package_id: str):
    endpoint: str = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages/{package_id}/biomedicalconcepts/{biomedicalconcept_id}"

    if biomedicalconcept_id is None or biomedicalconcept_id == "":
        raise ValueError("Please provide a valid id for the Biomedical Concept")
    if package_id is None or package_id == "":
        raise ValueError("Please provide a valid package id")

    raise NotImplementedError("Getting a biomedical concept by package is not implemented yet")
