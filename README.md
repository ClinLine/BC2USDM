# BC2USDM
Selection of CDISC Biomedical Concepts, add data capture features and store in USDM format

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