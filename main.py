import tkinter as tk
from pages.Index import Index
from pages.Mesure import Mesure
#from pages.Nuance import Nuance
from pages.Nuance import Nuance
#from pages.Nuance import Nuance
import os
from IDS_cam import Camera
from ids_peak import ids_peak as peak
import threading
from PIL import Image, ImageTk,ImageGrab,ImageDraw,ImageFont

class Main(tk.Tk):
    def __init__(self):

        tk.Toplevel.__init__(self)
        # Set up the window and the frames
        self.title("SMART'X") 
        self.attributes('-fullscreen', True)  # Open in full-screen mode
        self.geometry("1500x950")
        self.user_camera = False 
        self.create_folders()
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.Camera=Camera()
        self.Camera.demmarage()
        self.t = threading.Thread(target=self.Camera.demmarage)
        self.t.start()
        # Create the pages
        self.frames = {}
        #for F in (Index, Mesure,Nuance):
        
        for F in (Index, Mesure,Nuance):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
           
        # Show the first page
        """
        F = Mesure
        page_name = F.__name__
        frame = F(parent=container, controller=self)
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        """
        self.show_frame("Index")


    def create_folders(self):
       # Create the necessary folders if they don't exist
       folders_to_create = ["cropped_zones", "rectangles_folder", "result","Labels","label"]
       for folder_name in folders_to_create:
           if not os.path.exists(folder_name):
               os.makedirs(folder_name)
           else:
            print(f"Le dossier '{folder_name}' existe déjà.")
            
            

           

    def show_frame(self, page_name):
        #Shows the specified frame
        if page_name != "Index":
            self.user_camera = True
            self.frames[page_name]
            self.frames[page_name].tkraise()
        else:
            self.user_camera = False
            #self.frames["Nuance"].hide()
            #self.frames["Defects"].hide()
            #self.frames["Mesure"].hide()
            #self.frames["Back_pocket"].hide()
            self.frames[page_name].tkraise()
            
    def exit_fullscreen(self):
        # Function to exit full-screen mode
        self.attributes('-fullscreen', False)


            
            
if __name__ == "__main__":
    app = Main()
    app.mainloop()



