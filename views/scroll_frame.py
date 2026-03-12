from tkinter import Button, Canvas, Frame, PanedWindow, Scrollbar
from tkinter.constants import *


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


        self.v_scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas_window_id = self.canvas.create_window((4,4), 
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

        self._on_frame_configure(None)

    def _on_post_init(self):
        self.update_idletasks()
        self.recalculate_scrollregion(None)

    def _on_button_click(self, event, *args):
        pass

    def check_resize(self):
        # TODO: doesn't work correctly
        # TODO: fix before production
        children = [child for child in self.view_port.children.values() if not isinstance(child, (Button, PanedWindow))]
        if len(children) < self.max_visible_chrildren:
            self.recalculate_scrollregion(None)

    def recalculate_scrollregion(self, event):
        bbox = self.canvas.bbox("all")
        new_height:int = bbox[3] - bbox[1]
        self.canvas.config(height=new_height)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        # whenever the size of the canvas changes
        # update the window size
        self.canvas.itemconfig(self.canvas_window_id,width=canvas_width)

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
