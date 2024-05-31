import tkinter as tk
import customtkinter as ctk

from .Core import userChest as Chest
from .Theme import *


class Page_BM(ctk.CTkFrame): #the final frame to use is the "self.Scrollable_frame"
    def __init__(self, scrollable=True):
        self.parent = Chest.PageParent
        super().__init__(self.parent, fg_color="transparent")

        self.scrollable = scrollable
        self.key = 0            # doesn't allow the execution of the "called_when_opened" function untill the page is opened from the "tab frame page" >> self.key = 1
        self.openable = True
        self.started = False    # to check if the page is opened for the first time or not
        self.pickable = False
        self.last_Known_size = (0, 0)

        self.starting_call_list = []
        self.picking_call_list = []
        self.updating_call_list = []
        self.leaving_call_list = []

        if self.scrollable:
            self.Scrollable_canvas = tk.Canvas(self, background=LIGHT_MODE["background"] if ctk.get_appearance_mode() == "Light" else DARK_MODE["background"], scrollregion = (0, 0, self.winfo_width(), 10000), bd=0, highlightthickness=0, relief = 'ridge')
            self.Scrollable_canvas.pack(fill="both", expand=True)
            self.Scrollable_frame = ctk.CTkFrame(self.Scrollable_canvas, fg_color="transparent", bg_color=(LIGHT_MODE["background"], DARK_MODE["background"]))
        else:
            self.Scrollable_frame = ctk.CTkFrame(self, fg_color="transparent", bg_color=(LIGHT_MODE["background"], DARK_MODE["background"]))
            self.Scrollable_frame.pack(fill="both", expand=True)


    def called_when_opened(self, k=0): #it updates the height of the page and the scrollable region
        self.key = k if k else self.key
        if self.key: #* this is to prevent the function from running when the page isn't opened yet from the "tab frame page"
            if self.scrollable:
                # draw_scrollable_frame
                self.update()
                self.Scrollable_canvas.create_window(                                                       #we create it with a large height to see where is the last widget
                    (0,0), 
                    window=self.Scrollable_frame, 
                    anchor="nw", 
                    width = self.winfo_width(), 
                    height = 10000, 
                    tags= "frame")
                
                self.update()
                self.widget_children = self.Scrollable_frame.winfo_children()
                if self.widget_children != []:
                    self.max_height = self.Scrollable_frame.winfo_children()[-1].winfo_y() + self.Scrollable_frame.winfo_children()[-1].winfo_height()     # then we get the y position of the last widget
                else:
                    self.max_height = 1

                self.Scrollable_canvas.configure(scrollregion=(0, 0, self.winfo_width(), self.max_height))  # then we set the scrollable region to the last widget y position
                # there is no need to edit the frame height, just leave it with its default height, and limit the scroll using the canvas only
                
                if self.max_height > self.winfo_height():                                                   # if the max height is bigger than the frame height, we add the scrollbar
                    self.Scrollable_canvas.bind_all("<MouseWheel>", lambda event: self.Scrollable_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
                else:
                    self.Scrollable_canvas.unbind_all("<MouseWheel>")

            if self.started and self.pickable == False:
                self.pickable = True
            if self.started == False:
                self.started = True
                self.Starting() # this function is called only once when the page is opened for the first time
            
    #! it doesn't update the height of the page or the scrollable region
    def update_size_BM(self): #it updates the width of the page and checks if the scroll action is needed
        if self.scrollable:
            self.update()
            self.Scrollable_canvas.itemconfigure("frame", width=self.winfo_width())
            
            if self.max_height > self.winfo_height():                                                   # if the max height is bigger than the frame height, we add the scrollbar
                self.Scrollable_canvas.bind_all("<MouseWheel>", lambda event: self.Scrollable_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
            else:
                self.Scrollable_canvas.unbind_all("<MouseWheel>")
            
        self.update()
        self.Updating()    # this function is called every time the page is resized
    

    def Starting(self): # this function is called only once when the page is opened for the first time
        self.menu_frame = self.tool_menu()
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        for func in self.starting_call_list:
            func()
        self.on_start()
        self.last_Known_size = (self.parent.winfo_width(), self.parent.winfo_height())

    def Picking(self): 
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        if self.scrollable: 
            if self.last_Known_size != (self.parent.winfo_width(), self.parent.winfo_height()):
                # print("Size changed")
                self.update_size_BM()
                self.called_when_opened()

        for func in self.picking_call_list:
            func()

        self.on_pick()

    def Updating(self):
        for func in self.updating_call_list:
            func()
        
        self.last_Known_size = (self.parent.winfo_width(), self.parent.winfo_height())

        self.on_update()

    def Leaving(self, event):
        for func in self.leaving_call_list:
            func()

        self.last_Known_size = (self.parent.winfo_width(), self.parent.winfo_height())

        state = self.on_leave(event)
        return state 
           

    def get_scrframe_color(self):
        color = self.Scrollable_frame._fg_color
        if color == "transparent":
            return Chest.Manager._fg_color
        else:
            return color
        
