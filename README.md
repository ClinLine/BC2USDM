# BC2USDM
This tool shows how CDISC Biomedical Concepts obtained form CDISCs BC library can be selected and configured for the purpose of a flexible metadata repository. It will include the ability to add new properties and response values based on the rquirements from the company and therapeutic area. Note that a CDISC API is needed for the BC library which can be retrieved based on CDISC membership.


To run the tool:

Make sure you set up a virtual environement and all packages are installed using:
```
pip install -r /path/to/requirements.txt
```

Most of these packages should come standard with python already.


Furthermore, make sure the workspace/root folder has a file called ".env.dev" containing the following:

PRIMARY_KEY = [your primary cdisk api key] 
SECONDARY_KEY = [your secondary cdisk api key]

This file should be included in .gitignore, so it will NOT be submitted to github.

The application can be initiated by running: python .\app.py -__name__ __main__    
