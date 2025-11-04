from tkinter import Menu, filedialog
from tkinter import DISABLED

from utils.io.FileWriter import FileWriter



class MenuBar(Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, kwargs)
        self.menu_file = FileMenu(self)
        self.menu_edit = Menu(self)
        self.add_cascade(menu=self.menu_file, label="File")
        # self.add_cascade(menu=self.menu_file, label="Edit")
        # self.pack(side="TOP",fill='x',expand=True)
        
class FileMenu(Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, kwargs)
        self.add_command(label="New", command=self.newFile)
        self.entryconfig("New", state=DISABLED)
        self.add_command(label="Open...", command=self.openFile)
        self.entryconfig("Open...", state=DISABLED)
        self.export = ExportMenu(self)
        self.add_cascade(menu=self.export, label=f"Export")


    def newFile(self):
        print("Creating file")
        raise NotImplementedError("New file has not been implemented")

    def openFile(self):
        print("opening file")
        raise NotImplementedError("Opening files has not been implemented")

class ExportMenu(Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, kwargs)
        self.add_command(label="JSON", command=self.on_json_click)

    def on_json_click(self):
        testString:str = f"this is a test string"
        print(f"converting data to json")
        print(f"picking file location")
        print(f"saving file to disk")
        
        file_location = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            defaultextension=".json",
            filetypes=("text {.txt}", "JSON {.json}", "csv {.csv}"),
            parent=self,
            title="Export to JSON",
            typevariable=testString
        )
        if file_location is None:
            pass
        else:
            json_string = testString
            FileWriter.write(file_location, json_string)


        # if (fname:= dialog.selection["text"]) is None: pass
        # else:
            # print(fname)
            # FileWriter.write(dialog.directory,fname, json_string)
        # dirname = dialog.directory
        # json_string=testString
        print(f"Done!")
