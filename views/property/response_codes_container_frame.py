from tkinter import BooleanVar, LabelFrame, StringVar
from tkinter.constants import *

from views.property.response_code_frame import ResponseCodeFrame
from views.scroll_frame import ScrollFrame

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
        if response_codes is not None:
            for i, response_code in enumerate(response_codes):
                new_frame = ResponseCodeFrame(scrollframe.view_port, response_code, i, relief="groove", borderwidth=1,)
                self.response_code_frames.append(new_frame)

        # TODO: Replace with Super's add btn
        # Add new rc button:
        self._bind_add_button()

        # add_button = Button(scrollframe.view_port, text="Add new response code")

    def config_scrollframe(self):
        scroll_frame = ScrollFrame(self, True)
        scroll_frame.view_port.columnconfigure(index=1, weight=1, uniform=True)
        return scroll_frame

    def _bind_add_button(self):
        button = self.scroll_frame.add_element_button
        button["text"] = "Add new response code"
        button["command"] =lambda i=len(self.scroll_frame.view_port.children):self._on_add_button(i)

    def _on_add_button(self, response_code_ui_id):
        new_frame = ResponseCodeFrame(self.scroll_frame.view_port, None, response_code_ui_id, relief="groove", borderwidth=1)
        self.response_code_frames.append(new_frame)
        if self.response_codes is None:
            self.response_codes = [None]
        else:
            self.response_codes.append(None)
        self.update_idletasks()
        self.scroll_frame.check_resize()
