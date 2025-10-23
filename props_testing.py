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
            "notes":[f"beep boop",f"Bla bla\n bla", f"Bla bla \n akj;sdf a;klsdjf ;akdjfa;leksjfa;kldjf;a kljsef;alksejf;aklsjef;aksjfj a;ske;fjkasd;fjk asej;fkasjf;lkasej;fkl asjef;k lasefj a;kslefj asklef ja;skejfa;klsfj a;selkj ;fjkasd;fjk asej;fkasjf;lkasej;fkl asjef;k lasefj a;kslefj asklef ja;skejfa;klsfj a;selkj f", "this is super important too"],
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
        },
        {
            "id_":str(guid()).upper(),
            "label":"Testing Prop 2",
            "isRequired":1,
            "isEnabled":0,
            "dataType":"Bs",
            "code":"C651549",
            "notes":["Bla bla bla", "This is a crutial note", "this is super important too"],
            "responseCode":[{
                "id":str(guid()).upper(),
                "name":"Blood letting",
                "label":"Blood letting2",
                "isEnabled":1,
                "code":"C65154",
            }],
        },{
            "id_":str(guid()).upper(),
            "label":"Testing Prop",
            "isRequired":0,
            "isEnabled":1,
            "dataType":"Blood sample",
            "code":"C64165",
            "notes":["Bla bla bla", ],
            "responseCode":[{
                "id":str(guid()).upper(),
                "name":"Blood letting",
                "label":"Blood letting2",
                "isEnabled":1,
                "code":"C65416541",
            }],
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

        # prop_frame = PropertiesFrame(self.root, properties=dummyProperties)

        master.wm_title(master.wm_title()+ ": " + str(len(dummyProperties)))
        properties_frame = Properties_Container(self.root,frame_title="Properties:", properties=dummyProperties)
        properties_frame.pack(side=TOP,fill=BOTH, expand=True)
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

class ScrollFrame(Frame):
    # max amount of visible children
    max_visible_chrildren:int
    def __init__(self, parent, expandable, max_size:int = 3, *args, **kwargs):
        super().__init__(parent) # Create a frame (self)
        self.max_visible_chrildren = max_size
        # Place canvas on self
        self.canvas = Canvas(self, borderwidth=0,)
        self.view_port = Frame(self.canvas, name="!viewport")
        self.v_scrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.canvas.config(bg="yellow")
        self.view_port.config(bg="green")
        self.config(bg="pink")

        self.v_scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas_window = self.canvas.create_window((4,4), 
                                                       window=self.view_port,
                                                       anchor=NW,
                                                       tags="self.view_port")


        self.view_port.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.view_port.bind("<Enter>", self._bind_enter)
        self.view_port.bind("<Leave>", self._bind_leave)

        if expandable:
            self.add_element_button = Button(self.view_port, text="button not configured",)
            self.add_element_button.pack(side="bottom", )
            self.add_element_button.bind("<Button>", self._on_button_click)

        # print(self.canvas.bbox('all')) // useless
        # print(self.view_port.bbox('all'))
        # print(self.bbox('all'))

        
       
        self._on_frame_configure(None)

    def _on_post_init(self):
        self.update_idletasks()
        self.recalculate_scrollregion(None)

    def _on_button_click(self, event, *args):
        self.recalculate_scrollregion(event)

    def recalculate_scrollregion(self, event):
        print(self.canvas.bbox('all'))
        
        if(event is not None):
            # print(event.widget)
            pass
        
        self.canvas.config(height=self.canvas.bbox('all')[3])
        # resize as long as the amount of children is less than max children (+1 for the button)
        children = [child for child in self.view_port.children.values() if not isinstance(child,Button)]
        
        if len(children) < self.max_visible_chrildren:
            # bbox('all') returns a tuple(x0, y0, x1, y1) enveloping all children
            bbox = self.canvas.bbox("all")
            new_height:int = bbox[3] - bbox[1]
            # calc new height

            self.canvas.config(height=new_height)
            
            # 

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

class Properties_Container(LabelFrame):
    def __init__(self, parent, frame_title:str="Properties:",properties=[], *args, **kwargs):
        super().__init__(parent, text=frame_title)
        self.scroll_frame = ScrollFrame(self, True)

        # self.required_properties_vars:list[BooleanVar] = []
        # self.enabled_properties_vars:list[BooleanVar] = []
        self.property_containers = []

        for prop in properties:
            main_frame = PropertyFrame(self.scroll_frame.view_port, property=prop, name=f"main_frame_{prop["id_"]}")
            main_frame.columnconfigure(1,weight=1)
            self.property_containers.append(main_frame)

        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.scroll_frame._on_post_init()
        
        

class PropertyFrame(Frame):
    def __init__(self, parent, property = {}, *args, **kwargs):
        super().__init__(parent, name=kwargs["name"])
        row_index = 0

        # Property Label
        label_var = StringVar(value=property["label"])
        Label(self,text="Property:").grid(row=row_index,column=0,sticky="NWS")
        # Note: (i:=i+1)-1 equates to i++ in c-like languages (++i would be (i:=i+1))
        Entry(self,textvariable=label_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")
        

        # Property Id
        id_var = StringVar(value=property["id_"])
        Label(self,text="Property Id:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self, state=DISABLED, textvariable=id_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")
        
        # Property Code
        id_var = StringVar(value=property["code"])
        Label(self,text="Code:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self, state=DISABLED, textvariable=id_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")
    
        # isRequired
        Label(self,text="Required").grid(row=row_index,column=0,sticky="NWS")
        required_btn = Checkbutton(self)
        self.required_var = BooleanVar(master=required_btn, value=property["isRequired"])
        # self.required_properties_vars.append(required_var)
        required_btn.configure(variable=self.required_var)
        required_btn.grid(row=(row_index:=row_index+1)-1,column=1,sticky="NSW")

        # isEnabled
        Label(self,text="Enabled").grid(row=row_index,column=0,sticky="NWS")
        enabled_button = Checkbutton(self, name="!property_enabled_cbtn_"+str(property["id_"]).replace("-","_"))
        self.enabled_var = BooleanVar(master=enabled_button, value=property["isEnabled"])
        # self.enabled_properties_vars.append(enabled_var)
        enabled_button.configure(variable=self.enabled_var)
        enabled_button.grid(row=(row_index:=row_index+1)-1, column=1, sticky="NSW")

        # Property data-type
        label_var = StringVar(value=property["dataType"])
        Label(self,text="Data-type:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self,textvariable=label_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")

        self.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Property Notes
        notes_frame = NotesFrame(self, notes=property["notes"])
        notes_frame.grid(row=(row_index:=row_index+1)-1, column=0, columnspan=2, sticky=NSEW)
        # prop_window.add(notes_frame)

        # Property Response Codes:
        response_code_frame = ResponseCodesContainerFrame(self, response_codes=property["responseCode"])
        response_code_frame.grid(row=(row_index:=row_index+1)-1, column=0, columnspan=2, sticky=NSEW)


class NotesFrame(LabelFrame):
    _line_height = 16 #pixels
    def __init__(self, parent, lines=4, notes:list[str]=[""], min_textboxes=1, max_textboxes=3, *args, **kwargs):
        self.lines=lines
        self.min_textboxes=min_textboxes
        self.max_textboxes=max_textboxes
        super().__init__(parent, text="Notes:")
        self.scroll_frame = ScrollFrame(self, True)
        
        self.note_boxes:list[Text]=[]
        self.note_vars:list[StringVar]=[]

        # create PanedWindow to make the boxes scalable
        self.notes_panel = PanedWindow(self.scroll_frame.view_port, orient=VERTICAL)
        self.notes_panel.pack(side=TOP, fill=BOTH, expand=True)
        
        self.notes_count = IntVar(master=self, value=len(notes))
        _default__textbox_height:int = lines * 17
        _default_canvas_height = 0
        
        _min_height:int = lines * 16 + 4
        _max_height:int = lines * 16 * 3 + 4


        # Create a Textbox for each Note
        for note_index, note in enumerate(notes):

            # Create a StringVar to store each note in. note sure if Requried...
            self.note_vars.append(StringVar(value=note))
            # Create the Textbox
            # Default height = 24 := 384 pixels, border=1px, pady = 1px ==> 388 px, 16px / line
            # Default for 4 lines := 4 * 16 + 2 + 2 = 52 px
            # text_box = Text(self.notes_panel, name=f"notebox_{note_index}")
            text_box = Text(self.notes_panel, name=f"notebox_{note_index}",height=lines)

            # Setting initial text:
            text_box.insert('end', self.note_vars[note_index].get())

            text_box.bind("<FocusOut>", self._on_focus_out)
            text_box.pack(side=TOP, fill=BOTH, expand=TRUE)
            self.notes_panel.add(text_box)
            # self.note_boxes.append(text_box)
        # Make sure canvas is at least 1 textbox and at most {min_textboxes} textboxes big:
        # self.recalculate_canvas_height(len(notes))
        # self.notes_count.trace_variable(mode=W,lambda min_textboxes=min_textboxes, max_textboxes=max_textboxes, current_textboxes=event.value:self.recalculate_canvas_height)
        # self.notes_count.trace_add("write", callback=self._on_notescount_changed)
        # self.notes_count.trace_add("read", callback=self.testing)
        # self.notes_count.bind("<ValueChange>", )
        self.notes_count.set(10)
        # Add empty frame to make bottom textbox rescalable
        self.notes_panel.add(Frame(self.notes_panel, name="empty_-1", height=0))
        
        # when placing in the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.scroll_frame._on_post_init()
    
    # def _on_notescount_changed(self, *args):
    #     self.recalculate_canvas_height(current_textboxes=self.notes_count.get())
        

    # def recalculate_canvas_height(self, current_textboxes:int=0):
    #     if current_textboxes >= self.max_textboxes:
    #         self.scroll_frame.canvas.config(height=self.max_textboxes * self.lines * NotesFrame._line_height)
    #     elif current_textboxes <= self.min_textboxes:
    #         self.scroll_frame.canvas.config(height=self.min_textboxes * self.lines * NotesFrame._line_height)
    #     else:
    #         self.scroll_frame.canvas.config(height=current_textboxes * self.lines * NotesFrame._line_height)

    def _on_focus_out(self, event):
        # widgit name will be in the shape of NAME#, where # is the index of the textbox
        text_index:int = int(event.widget._name.split('_')[-1])
        text_dump:tuple[str] = event.widget.dump('0.0', 'end', text=True)
        textbox_contents:str = ""
        for text_tuple in text_dump:
            # text_tuple == ('text', 'CONTENTS', 'index:line.character')
            textbox_contents = textbox_contents + text_tuple[1]
        # remove trailing \n
        if textbox_contents.endswith('\n'):
            textbox_contents = textbox_contents[:-1]
        self.note_vars[text_index].set(textbox_contents)
        # self.recalculate_height(event.widget, len(text_dump))
    
    # def recalculate_height(self, text_box:Text, lines, line_height=12):
    #     new_height = lines*line_height
    #     if text_box.winfo_height() < new_height:
    #         self.notes_panel.paneconfigure(text_box, height=new_height)
    #         self.notes_panel.configure(height=self.notes_panel.winfo_height() + new_height)
        

class ResponseCodesContainerFrame(LabelFrame):
    def __init__(self, parent, response_codes=[], *args, **kwargs):
        super().__init__(parent, text="Response Codes:")
        self.scroll_frame = self.config_scrollframe()
        self.response_codes = response_codes
        self.initialize_response_codes(response_codes, self.scroll_frame)


        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.scroll_frame._on_post_init()
        

    # def setup_add_button(self, response_codes):
    #     add_button = Button(self.scroll_frame.view_port, text="New response code")
    #     add_button.pack(side=BOTTOM, expand=True)
        
    def initialize_response_codes(self, response_codes={}, scrollframe:ScrollFrame=None):
        self.id_vars:list[StringVar] = []
        self.enabled_vars:list[BooleanVar] = []
        self.response_code_frames = []
        for i, response_code in enumerate(response_codes):
            new_frame = ResponseCodeFrame(scrollframe.view_port, response_code, i, relief="groove", borderwidth=1,)
            self.response_code_frames.append(new_frame)
            
        # TODO: Replace with Super's add btn
        # Add new rc button:
        add_button = Button(scrollframe.view_port, text="Add new response code")
        add_button.pack(side=BOTTOM, fill=X,expand=TRUE)
        add_button.config(command=lambda i=len(self.scroll_frame.view_port.children):self.on_add_button(i))

    def config_scrollframe(self):
        scroll_frame = ScrollFrame(self, True)
        scroll_frame.view_port.columnconfigure(index=1, weight=1, uniform=True)
        return scroll_frame
    
    def on_add_button(self, response_code_ui_id):
        new_frame = ResponseCodeFrame(self.scroll_frame.view_port, None, response_code_ui_id, relief="groove", borderwidth=1)
        self.response_code_frames.append(new_frame)
        self.response_codes.append(None)


class ResponseCodeFrame(Frame):
    rc_index:int # response code index

    # Attributes:
    label_var:StringVar
    id_var:StringVar
    # name_var:StringVar # hidden & inferred
    is_enabled_var:IntVar
    code_var:StringVar


    def __init__(self, parent, response_code=None, index:int=0, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)
        self.response_code=response_code
        self.rc_index = index
        # self.response_code_frame_id = __class__.NOT_SET
        self.create()
        self.pack(side=TOP, fill=BOTH, expand=True)
        self.columnconfigure(index=1, weight=1, uniform=TRUE)
        self.populate(response_code)

    def create(self):
        i:int=0
        self.initialize_vars()

        # Label:
        l_label = Label(self, text="Label:")
        l_label.grid(row=i, column=0, sticky="NSW")
        e_label = Entry(self, textvariable=self.label_var)
        e_label.grid(row=(i:=i+1)-1, column=1, sticky=NSEW)
        
        # Id:
        l_id = Label(self,text="Response code id:")
        l_id.grid(row=i, column=0, sticky="NSW")

        e_id = Entry(self, textvariable=self.id_var, state=DISABLED)
        e_id.grid(row=(i:=i+1)-1, column=1, sticky=NSEW)
        # Code:
        l_code = Label(self, text="Code:")
        l_code.grid(row=i, column=0, sticky="NSW")
        e_code = Entry(self, textvariable=self.code_var)
        e_code.grid(row=(i:=i+1)-1, column=1, sticky=NSEW)

        # Enabled:
        l_enabled = Label(self, text="Enabled:")
        l_enabled.grid(row=i, column=0, sticky="NWS")
        enabled_button = Checkbutton(self, variable=self.is_enabled_var)
        enabled_button.grid(row=(i:=i+1)-1, column=1, sticky="NSW")

    def initialize_vars(self):
        self.id_var = StringVar(value="", )
        self.label_var = StringVar(value="",)
        # self.name_var = StringVar(value="") # inferred
        self.is_enabled_var = IntVar(value=0, )
        self.code_var = StringVar(value="", )

    def populate(self, response_code=None):
        if response_code is not None:
            # Attributes:
            self.label_var.set(response_code["label"])
            self.id_var.set(response_code["code"])
            # name_var:StringVar # hidden & inferred
            self.is_enabled_var.set(response_code["isEnabled"])
            self.code_var.set(response_code["id"])
            # TODO Add Code support?
        else:
            self.id_var.set(guid())