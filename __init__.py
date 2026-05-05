# from BC2USDM.app import App
__name__="BC2USDM"
__package__="BC2USDM"

import app

if __name__ == "BC2USDM":
    print("starting")
    app.App_Instance = app.App()
    app.App_Instance.start()