import customtkinter as ctk
from CTK_Desert import Chest
from CTK_Desert.Page_base_model import Page_BM
from CTK_Desert.Theme import *
from CTK_Desert.utils import hvr_clr_g

# don't ever pack the frame, it will be packed in the Tab_Page_Frame.py
class CUNAME__C(Page_BM):
    def __init__(self):
        super().__init__(scrollable="SCRL_VAL__")
        self.menu_page_frame = Chest.Manager
        self.frame = self.Scrollable_frame # Parent of all children in this page
        self.frame.configure(fg_color = (hvr_clr_g(LIGHT_MODE["background"], "l"), hvr_clr_g(DARK_MODE["background"], "d")))
        self.mode = ctk.get_appearance_mode()

    def on_start(self):
        pass

    def on_pick(self):
        pass

    def on_update(self):
        pass
    
    def on_leave(self, event):
        return True

    def tool_menu(self):
        self.tool_p_f = self.menu_page_frame.apps_frame
        self.tools_f = ctk.CTkFrame(self.tool_p_f, fg_color="transparent")

        return self.tools_f

