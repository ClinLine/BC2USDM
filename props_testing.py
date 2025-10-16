from tkinter import *
from uuid import uuid4 as guid
from tkinter import ttk
from typing import overload



# from main import App as instance

# from functools import lru_cache

dummyProperties = [{
            "id_":str(guid()).upper(),
            "label":"Testing Prop",
            "isRequired":1,
            "isEnabled":0,
            "dataType":"Blood sample",
            "code":"C2389",
            "notes":[f"Bla bla\n bla", f"Bla bla \n akj;sdf a;klsdjf ;akdjfa;leksjfa;kldjf;a kljsef;alksejf;aklsjef;aksjfj a;ske;fjkasd;fjk asej;fkasjf;lkasej;fkl asjef;k lasefj a;kslefj asklef ja;skejfa;klsfj a;selkj ;fjkasd;fjk asej;fkasjf;lkasej;fkl asjef;k lasefj a;kslefj asklef ja;skejfa;klsfj a;selkj f", "this is super important too"],
            "responseCode":[{
                "id":str(guid()).upper(),
                "name":"Blood letting",
                "label":"Blood letting2",
                "isEnabled":1,
                "code":"C651654",
            },{
                "id":str(guid()).upper(),
                "name":"Blood letting",
                "label":"Blood letting2",
                "isEnabled":0,
                "code":"C651654",
            },],
        # },
        # {
        #     "id_":str(guid()).upper(),
        #     "label":"Testing Prop 2",
        #     "isRequired":1,
        #     "isEnabled":0,
        #     "dataType":"Bs",
        #     "code":"C651549",
        #     "notes":["Bla bla bla", "This is a crutial note", "this is super important too"],
        #     "responseCode":[{
        #         "id":str(guid()).upper(),
        #         "name":"Blood letting",
        #         "label":"Blood letting2",
        #         "isEnabled":1,
        #         "code":"C65154",
        #     }],
        # },{
        #     "id_":str(guid()).upper(),
        #     "label":"Testing Prop",
        #     "isRequired":0,
        #     "isEnabled":1,
        #     "dataType":"Blood sample",
        #     "code":"C64165",
        #     "notes":["Bla bla bla", "This is a crutial note", "this is super important too"],
        #     "responseCode":[{
        #         "id":str(guid()).upper(),
        #         "name":"Blood letting",
        #         "label":"Blood letting2",
        #         "isEnabled":1,
        #         "code":"C65416541",
        #     }],
        }]

# @lru_cache(maxsize=1)
class PropertyDisplay():
    
    __default_height: int = 600
    __data_columns: int = 4
    __data_column_width = [200,300,300,200]
    __default_width: int = sum(__data_column_width)
    __data_column_height = __default_height
    # __instance: type["PropertyDisplay"]
    root:Tk

    __app_instance:"App"

    mainframe:ttk.Frame

    def __init__(self, master, title):
        self.setup_ui(master, title)
        # self.root.mainloop()
       
    def setup_ui(self,master, title):
        self.root = master
        self.root.title(title)
        # self.root.title("Property Testing")
        self.root.config(height=PropertyDisplay.__default_height,width=PropertyDisplay.__default_width)
        self.root.geometry(f"{PropertyDisplay.__default_width}x{PropertyDisplay.__default_height}")

        # self.root.config(bg="red")

        prop_frame = PropertiesFrame(self.root, properties=dummyProperties)

        # properties = LabelFrame(self.root, text="test frame")
        # testingFrame.place(anchor="nw",relheight=1,relwidth=1)
        
        ## Properties: ################################
        # Property:             [NAME           ] #[^]#
        # Property Id:          [ID             ] #[|]#
        # Code:                 [Code.code      ] #[|]#
        # Required:             [?] isRequired    #[ ]#
        # Enabled:              [x] isEnabled     #[ ]#
        # Property Datatype:    [dataType       ] #[ ]#
        ## Property Notes #########################[ ]#
        # ____________________________________    #[ ]#
        # |Property Notes:     [notes[0]     ][^]|#[ ]#
        # |                    [             ][|]|#[ ]#
        # |                    [notes[i]     ][ ]|#[ ]#
        # |____________________[_____________][v]|#[ ]#
        ###########################################[ ]#
        ## Response Codes:#########################[ ]#
        # ____________________________________    #[ ]#
        # |Label:               [label       ]|[^]#[ ]#
        # |Id:                  [ID          ]|[|]#[ ]#
        # |Name:----------------HIDDEN--------|[ ]#[ ]#
        # |Enabled:             [?] isEnabled |[ ]#[ ]#
        # |code:                [Code        ]|[ ]#[ ]#
        # |___________________________________|[ ]#[ ]#
        # |Label:               [label       ]|[ ]#[ ]#
        # |Id:                  [ID          ]|[ ]#[ ]#
        # |Name:----------------HIDDEN--------|[v]#[v]#
        ###############################################



class PropertiesFrame(Canvas):
    def __init__(self, parent=None, title:float|str="Properties:",/, properties=[]):
        # Label frame surrounding canvas:
        # self.title = title
        surrounding_frame = LabelFrame(parent, text=title)
        surrounding_frame.pack(expand=True,fill=BOTH)
        surrounding_frame.columnconfigure(0,weight=1)
        surrounding_frame.rowconfigure(0,weight=1)

        # Scrollbar:
        self.scrollbar = Scrollbar(surrounding_frame, orient=VERTICAL)
        # self.create_window((0,0),anchor="NW",window=surrounding_frame)
        # self.scrollbar.config(command=self.yview)
        
        # self.scrollbar.grid(expand=True, fill=Y,side=RIGHT)

        super().__init__(surrounding_frame)
        # print(surrounding_frame.__dict__)
        self.config(bg="red")
        self.grid(column=0,row=0,sticky="NESW")
        self.scrollbar.grid(column=1,row=0,sticky="NES")
        self.scrollbar.config(command=self.tScroll)
        
        for prop in properties:
            
            prop_window = PanedWindow(self,name=f"window_{prop["id_"]}".replace("-","_"), orient=VERTICAL)
            prop_window.pack(expand=True,fill=BOTH,)
            main_frame = Frame(prop_window,name=f"main_frame_{prop["id_"]}")
            main_frame.columnconfigure(1,weight=1)
            prop_window.add(main_frame)

            row_index = 0

            # Property Label
            label_var = StringVar(value=prop["label"])
            Label(main_frame,text="Property:").grid(row=row_index,column=0,sticky="NWS")
            # Note: (i:=i+1)-1 equates to i++ in c-like languages (++i would be (i:=i+1))
            Entry(main_frame,textvariable=label_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")
            

            # Property Id
            id_var = StringVar(value=prop["id_"])
            Label(main_frame,text="Property Id:").grid(row=row_index,column=0,sticky="NWS")
            Entry(main_frame, state=DISABLED, textvariable=id_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")
            
            # Property Code
            id_var = StringVar(value=prop["code"])
            Label(main_frame,text="Code:").grid(row=row_index,column=0,sticky="NWS")
            Entry(main_frame, state=DISABLED, textvariable=id_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")
           
            # isRequired
            Label(main_frame,text="Required").grid(row=row_index,column=0,sticky="NWS")
            required_var = IntVar(value=prop["isRequired"], name=f"isRequired{prop['id_']}")
            Checkbutton(main_frame,variable=required_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NSW")

            # isEnabled
            enabled_var = IntVar(value=prop["isEnabled"])
            Label(main_frame,text="Enabled").grid(row=row_index,column=0,sticky="NWS")
            Checkbutton(main_frame, variable=enabled_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NSW")

            # Property data-type
            label_var = StringVar(value=prop["dataType"])
            Label(main_frame,text="Data-type:").grid(row=row_index,column=0,sticky="NWS")
            Entry(main_frame,textvariable=label_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")

            # Property Notes
            notes_frame = NotesFrame(prop_window, notes=prop["notes"])
            prop_window.add(notes_frame)

            # Property Response Codes:
            response_code_frame = ResponseCodeFrame(prop_window, response_codes=prop["responseCode"])
            prop_window.add(response_code_frame)
        self.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar["command"] = self.yview
        self.configure(scrollregion=self.bbox("all"))

    def tScroll(self, *args):
        print("calling tScroll")
        for a in args:
            print(a)
        self.moveto(args[1])



class ScrollFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent) # Create a frame (self)

        # Place canvas on self
        self.canvas = Canvas(self, borderwidth=0, background="green")
        self.view_port = Frame(self.canvas, background="purple")
        self.v_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.v_scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas_window = self.canvas.create_window((4,4), 
                                                       window=self.view_port,
                                                       anchor=NW,
                                                       tags="self.view_port")
        
        
        self.view_port.bind("<Configure>", self._on_frame_configure)
        # print(self.view_port.bind("<Configure>"))
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        self.view_port.bind("<Enter>", self._bind_enter)
        self.view_port.bind("<Leave>", self._bind_leave)

        self._on_frame_configure(None)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        # whenever the size of the canvas changes
        # update the window size
        self.canvas.itemconfig(self.canvas_window,width=canvas_width)

    def _bind_enter(self, event):
        # Linux:
        # if platform.system() == "Linux":
            # self.canvas.bind_all("<Button-4>", self._on_mousewheel)
            # self.canvas.bind_all("<Button-5>", self._on_mousewheel)
        # else:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _bind_leave(self, event):
                # Linux:
        # if platform.system() == "Linux":
            # self.canvas.unbind_all("<Button-4>")
            # self.canvas.unbind_all("<Button-5>")
        # else:
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        # Windows Only
        self.canvas.yview_scroll(int(-1*(event.delta/120)), UNITS)
        # Darwin:
        # self.canvas.yview_scroll(int(1*(event.delta)), UNITS)
        # else:
        #     if event.num == 4:
        #         self.canvas.yview_scroll(-1,UNITS)
        #     elif event.num == 5:
        #         self.canvas.yview_scroll(1, UNITS)

class PropertiesMainFrame(Frame):
    def __init__(self, parent, properties={}, *args, **kwargs):
        super().__init__(parent)
        self.scroll_frame = ScrollFrame(self)


    

class NotesFrame(LabelFrame):
    def __init__(self, parent, lines=4, notes:list[str]=[""], *args, **kwargs):
        
        super().__init__(parent, text="Notes:")
        self.scroll_frame = ScrollFrame(self)
        
        self.note_boxes:list[Text]=[]
        self.note_vars:list[StringVar]=[]

        # Create a Textbox for each Note
        for note_index, note in enumerate(notes):
            
            # Create a StringVar to store each note in. note sure if Requried...
            self.note_vars.append(StringVar(value=note))
            # Create the Textbox
            text_box = Text(self.scroll_frame.view_port, name=f"notebox_{note_index}",height=lines)

            # Setting initial text:
            text_box.insert('end', self.note_vars[note_index].get())
            
            text_box.bind("<FocusOut>", self._bind_to_focus_out)
            text_box.pack(side=TOP, fill=BOTH, expand=TRUE)
            self.note_boxes.append(text_box)
        # when placing in the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=TRUE)

    def _bind_to_focus_out(self, event):
        self._on_focus_out(event)

    def _on_focus_out(self, event):
        text_index:int = int(event.widget._name[-1])
        text_dump:tuple[str] = event.widget.dump('0.0', 'end', text=True)
        textbox_contents:str = ""
        for _tuple in text_dump:
            # _tuple == ('text', 'CONTENTS', 'index:line.character')
            textbox_contents = textbox_contents + _tuple[1]
        if textbox_contents.endswith('\n'):
            # remove trailing \n
            textbox_contents = textbox_contents[:-1]
        self.note_vars[text_index].set(textbox_contents)

class ResponseCodeFrame(LabelFrame):
    def __init__(self, parent, response_codes:{}, *args, **kwargs):
        super().__init__(parent, text="Response Codes:")
        self.scroll_frame = ScrollFrame(self)
        self.scroll_frame.view_port.columnconfigure(1, weight=1, uniform=True)
        self.id_vars:list[StringVar] = []
        self.enabled_vars:list[BooleanVar] = []
        for i, response_code in enumerate(response_codes):
            # Id:
            Label(self.scroll_frame.view_port,text="Response code id:").grid(row=i*4, column=0, sticky="NSW")
            self.id_vars.append(StringVar(value=response_code["id"]))
            Entry(self.scroll_frame.view_port, textvariable=self.id_vars[i], state=DISABLED).grid(row=i*4, column=1, sticky=NSEW)
            # Code:
            Label(self.scroll_frame.view_port, text="Code:").grid(row=i*4+1, column=0, sticky="NSW")
            entry_var = StringVar(value=response_code["code"])
            Entry(self.scroll_frame.view_port, textvariable=entry_var).grid(row=i*4+1, column=1, sticky=NSEW)

            # Label:
            Label(self.scroll_frame.view_port, text="Name:").grid(row=i*4+2, column=0, sticky="NSW")
            label_var=StringVar(value=response_code["label"])
            Entry(self.scroll_frame.view_port, textvariable=label_var).grid(row=i*4+2, column=1, sticky=NSEW)

            # Enabled:
            Label(self.scroll_frame.view_port, text="Enabled:").grid(row=i*4+3, column=0, sticky="NWS")
            enabled_button = Checkbutton(self.scroll_frame.view_port, name="!response_enabled_btn_"+str(response_code["id"]).replace("-","_"))
            enabled_var = IntVar(master=enabled_button, value=response_code["isEnabled"])
            self.enabled_vars.append(enabled_var)
            enabled_button.configure(variable=self.enabled_vars[i], onvalue=True, offvalue=False)
            enabled_button.grid(row=i*4+3, column=1, sticky="NSE")

        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=True)