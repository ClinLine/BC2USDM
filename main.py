import requests
import json
from dotenv import dotenv_values
import pandas
secrets = dotenv_values(".env.dev")
api_key = secrets["PRIMARY_KEY"]

def get_latest_categories():
    headers_ = {
        "cache-Control": "no-cache",
        "api-key": api_key,
        }


    url: str = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/categories"
    try:
        req = requests.get(url, headers=headers_, timeout=10)
        categories = req.json()["_links"]["categories"]
        category_names = []
        for category in categories:
            category_names.append(category["name"])
        return category_names
        
    except Exception as e:
        print(e)
# get_latest_categories()

def get_biomedical_concepts_list(category: str=None):
    headers_ = {
        "Cache-Control":"no-cache",
        "api-key": api_key
    }
    endpoint: str = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts"
    url = endpoint
    if(category is not None and category != ""):
        if category in get_latest_categories():
            url = f"{endpoint}?category="
    try:
        req = requests.api.get(url, headers=headers_, timeout=10)
        bcs = req.json()["_links"]["biomedicalConcepts"]
        result = []
        for bc in bcs:
            element = (bc["title"],bc["href"].split("/")[-1], bc["href"],bc )
            result.append(element)
        return pandas.DataFrame(result, columns=["title","id","href","json"])
    except Exception as e:
        print(e)

def getBiomedicalConceptPackageList():
    headers_ = {
        "cache-Control": "no-cache",
        "api-key": api_key,
        }
    endpoint = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages"
    try:
        req = requests.api.get(endpoint,headers=headers_, timeout=10)
        print(req.json()["_links"]["packages"])
        packages_data = req.json()["_links"]["packages"]
        result = []
        for package_data in packages_data:
            title = package_data["title"]
            href = package_data["href"]
            id_ = package_data["href"].split(sep="/")[-2] # sub-final substring
            result.append((title,id_,href,package_data))
        return pandas.DataFrame(result,columns=["title","id","href", "json"])
    except Exception as e:
        print(e)

def getBiomedicalConceptListForPackage(package):
    headers_ = {
        "cache-Control": "no-cache",
        "api-key": api_key,
        }
    endpoint = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages"
    
    if package is None or package == "":
        raise Exception("Please provide a package id (data)")
    print(getBiomedicalConceptPackageList()["id"])
    if not package in getBiomedicalConceptPackageList()["id"]:
        raise Exception("The provided package was not found")
    endpoint = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages/{package}/biomedicalconcepts"
    try:
        req = requests.api.get(endpoint, headers=headers_, timeout=10)
        print(req.json["_links"])
    except Exception as e:
        print(e)

getBiomedicalConceptListForPackage("2022-10-26")