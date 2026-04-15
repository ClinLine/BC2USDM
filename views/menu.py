from json import JSONEncoder
import json
from tkinter import Menu, filedialog
from tkinter import DISABLED
from datetime import date
from utils.io.FileWriter import FileWriter



class MenuBar(Menu):
    app = None
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, kwargs)
        self.app = app
        self.menu_file = FileMenu(self, app)
        self.menu_edit = Menu(self)
        self.add_cascade(menu=self.menu_file, label="File")
        # self.add_cascade(menu=self.menu_file, label="Edit")
        # self.pack(side="TOP",fill='x',expand=True)
        
class FileMenu(Menu):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, kwargs)
        self.add_command(label="New", command=self.newFile)
        self.entryconfig("New", state=DISABLED)
        self.add_command(label="Open...", command=self.openFile)
        self.entryconfig("Open...", state=DISABLED)
        self.export = ExportMenu(self, app)
        self.add_cascade(menu=self.export, label=f"Export")


    def newFile(self):
        print("Creating file")
        raise NotImplementedError("New file has not been implemented")

    def openFile(self):
        print("opening file")
        raise NotImplementedError("Opening files has not been implemented")

class ExportMenu(Menu):
    
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, kwargs)
        self.app = app
        self.add_command(label="JSON", command=self.on_json_click)

    def on_json_click(self):
        selection = self.app.get_repository()
        if selection is None:
            selection = f"this is a test string"
        
        today = date.today()
        date_str = f"{today.year}-{str(today.month).rjust(2,'0')}-{str(today.day).rjust(2,'0')}"

        file_location = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension="json",
            filetypes=("all {.*}", "json {.json}","text {.txt}"),
            initialfile=date_str,
            parent=self,
            title="Export repository - Choose file location",
            typevariable=(file_type:="json")
        )
        
        if file_location is None:
            pass
        elif file_location == "":
            print("Export canceled by user")
        else:
            FileWriter.writeJSON(selection, file_location)
            