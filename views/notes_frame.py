from tkinter import LabelFrame, PanedWindow, StringVar, Text
from tkinter.constants import *

from views.scroll_frame import ScrollFrame


class NotesFrame(LabelFrame):
    _line_height = 16 #pixels
    def __init__(self, parent, lines=4, notes:list[str]=[""], min_textboxes=1, max_textboxes=3, *args, **kwargs):
        self.lines=lines
        self.min_textboxes=min_textboxes
        self.max_textboxes=max_textboxes
        super().__init__(parent, text="Notes:")
        self.scroll_frame = ScrollFrame(self, True)
        
        self.note_vars:list[StringVar]=[]

        # create PanedWindow to make the boxes scalable
        self.notes_panel = PanedWindow(self.scroll_frame.view_port, orient=VERTICAL)
        self.notes_panel.pack(side=TOP, fill=BOTH, expand=True)


        # Create a Textbox for each Note
        if notes is not None:
            for note_index, note in enumerate(notes):
                self._add_text_box(note,4)

        # when placing in the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.scroll_frame._on_post_init()
        self._bind_add_button()

    def _bind_add_button(self):
        button = self.scroll_frame.add_element_button
        button["text"] = "Add new Note"
        button["command"] = self._on_button_click

    def _on_button_click(self, event=None, *args):
        self._add_text_box("", 4)

    def add_notes(self, notes):
        for note in notes:
            self._add_text_box(note.text,4)

    def _add_text_box(self, text="", textbox_height:int=4):
        self.note_vars.append(StringVar(value=text))
        new_box = Text(self.scroll_frame.view_port, name=f"notebox_{len(self.note_vars)-1}", height=textbox_height)
        if text != "":
            new_box.insert('end', text)
        new_box.bind("<FocusOut>", self._on_focus_out)
        new_box.pack(side=TOP, fill=BOTH, expand=True)
        self.notes_panel.add(new_box)
        self.update_idletasks()
        self.scroll_frame.check_resize()

    def _on_focus(self, event):
        ...

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

    def get_notes(self):
        if len(self.note_vars) == 0:
            return []
        notes:list[str]=[]
        for string_var in self.note_vars:
            if string_var.get() != "":
                notes.append(string_var.get())
        return notes
