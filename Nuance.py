# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:30:02 2023

@author: IA_la
"""

import tkinter as tk
from tkinter import ttk
import colorsys
import nuance_b
from CTkMessagebox import CTkMessagebox

from tkinter import *
import customtkinter
import cv2
import PIL.Image, PIL.ImageTk 
from PIL import Image
import  numpy  as  np
import  pandas  as  pd  
from imutils import contours
import imutils
import  os  
import glob

from PIL import Image, ImageTk,ImageGrab,ImageDraw,ImageFont
import os
import threading
import torch
import platform
import subprocess
import time
from IDS_cam import Camera
from ids_peak import ids_peak
import  datetime
import  numpy as np  
from  imutils  import  contours 
import  imutils
import shutil
from tkinter import messagebox
from matplotlib import pyplot as plt
from  pages.metier_nuance import  Metier_nuance
import tkinter.messagebox as messagebox
#--------------------------
from .helpers import resize_canvas  
from tkinter import messagebox

#customtkinter.set_default_color_theme("dark-blue")
import glob



class ImageViewer(tk.Toplevel):
    def __init__(self, image_path, text_file_path=None):
        super().__init__()
        self.title("Image Viewer")
        self.geometry("800x400")

        # Store the image and text file paths for later use
        self.image_path = image_path
        self.text_file_path = text_file_path
        self.new_text = ""
        
        self.combobox_list = []  # List to store references to comboboxes

        # Create the left and right frames
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Variables for image zoom and panning
        self.zoom_factor = 1.0
        self.x_position = 0
        self.y_position = 0

        self.load_image_and_setup_interface()

        # Event bindings for mouse actions
        self.label.bind("<MouseWheel>", self.zoom)
        self.label.bind("<ButtonPress-1>", self.start_pan)
        self.label.bind("<B1-Motion>", self.pan)
        
        
    def load_image_and_setup_interface(self):
        try:

            self.image = Image.open(self.image_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.nom_image = os.path.basename(self.image_path)

            self.label = tk.Label(self.left_frame, image=self.photo)
            self.label.pack()



            self.image_name_label = tk.Label(self.right_frame, text=f"Image Name: {os.path.basename(self.image_path)}")
            self.image_name_label.grid(row=6, column=0, columnspan=2, pady=10)

            

        except Exception as e:
            print("Error loading image:", e)

    


    def zoom(self, event):
        # Handle image zooming with mouse wheel
        if event.delta > 0:
            self.zoom_factor *= 1.1
        else:
            self.zoom_factor /= 1.1

        self.update_image()

    def update_image(self):
        # Update the image with the current zoom factor and position
        zoomed_image = self.image.resize((int(self.image.width * self.zoom_factor),
                                          int(self.image.height * self.zoom_factor)))
        self.photo = ImageTk.PhotoImage(zoomed_image)
        self.label.configure(image=self.photo)

    def start_pan(self, event):
        # Record the starting position for panning
        self.x_position = event.x
        self.y_position = event.y

    def pan(self, event):
        # Handle panning of the image with mouse drag
        delta_x = event.x - self.x_position
        delta_y = event.y - self.y_position

        self.x_position = event.x
        self.y_position = event.y

        self.label.place(x=self.label.winfo_x() + delta_x, y=self.label.winfo_y() + delta_y)







    def get_text_file_path(self):
        image_directory, image_filename = os.path.split(self.image_path)
        text_filename = os.path.splitext(image_filename)[0] + ".png.txt"
        text_file = r"./cropped_zones"  # Remplacez 'chemin_vers_votre_dossier' par le chemin réel
        text_file_path = os.path.join(text_file, text_filename)  # Replace this with the text files directory
        return text_file_path


  
    
    


class Limit_ref(tk.Toplevel):
    customtkinter.set_appearance_mode('dark')
    def __init__(self):
        super().__init__()
        self.title("Image Viewer")
        self.geometry("1500x950")
        
     
        self.Camera=Camera.get_instance()
        self.metier=Metier_nuance()
        
        image_path=os.path.join(os.path.dirname(__file__),"test_images","sartex.png")
        self.result_dict = {}


        self.df_ref=None
        self.df_ref_1=None
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.main_canvas = tk.Canvas(self.main_frame, bg="#212121", highlightthickness=0)
        self.main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        

        # Add A Scrollbar To The main_canvas
        self.my_scrollbar = tk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.main_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Create ANOTHER Frame INSIDE the self.main_canvas
        self.second_frame = customtkinter.CTkFrame(self.main_canvas,fg_color=("#B2D8FF","#6687E5"))
        self.second_frame.pack(fill=BOTH, expand=1)
        left_image = Image.open(r"./pages/test_images/logo-sartex.png")
        w, h = left_image.size
        self.left_image = customtkinter.CTkImage(left_image, size=(w//2, h//2))
        self.left_image_label = customtkinter.CTkLabel(self.second_frame, image=self.left_image, text="")
        self.left_image_label.grid(row=0,column=0,padx=(10, 0), pady=(0, 0), sticky="nw")
        
        left_image = Image.open(r"./pages/test_images/sartex1.png")
        w, h = left_image.size
        self.left_image = customtkinter.CTkImage(left_image, size=(w//2, h//2))
        self.left_image_label = customtkinter.CTkLabel(self.second_frame, image=self.left_image, text="")
        self.left_image_label.grid(row=0,column=0,padx=(200, 0), pady=(0, 10), sticky="nw")
        

        

        

        
        
        self.measure_frame1 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="transparent")
        self.measure_frame1.grid(row=1,column=6, sticky="we",columnspan=6,padx=(20, 0), pady=(0, 0))
        
        #self.measure_frame1.grid_rowconfigure(2, weight=1)
        
        
        
        
    
        # create the camera canvas
        self.canvas = customtkinter.CTkCanvas(self.measure_frame1,background='#212121',highlightthickness=0,height=500,width=850)
        self.canvas.grid(row=0, column=2,columnspan=6, padx=(20, 0), pady=(20, 0), sticky="we")
        
        self.sidebar_frame = customtkinter.CTkFrame(self.measure_frame1, width=140,  height=200,corner_radius=0,fg_color="#E0EFFF")
        self.sidebar_frame.grid(row=0, column=8, rowspan=6, padx=(20, 0), pady=(20, 0),sticky="nse")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text=" CONTROLE Nuance", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
       

       




        self.go_back = customtkinter.CTkButton(self.sidebar_frame,text="go back",command=self.fermer_app)
        self.go_back.grid(row=11, column=0, padx=20, pady=10)
        self.g_pdf = customtkinter.CTkButton(self.sidebar_frame,text="scanne limite",command=self.capt)
        self.g_pdf.grid(row=7, column=0, padx=20, pady=5)
        self.label_clic = customtkinter.CTkLabel(self.sidebar_frame, text="",text_color="black",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_clic.grid(row=8, column=0, padx=20, pady=5)
        self.g_pdf = customtkinter.CTkButton(self.sidebar_frame,text="Corection _image")
        self.g_pdf.grid(row=9, column=0, padx=20, pady=5)
        # Create and configure a Scale widget
        slider = tk.StringVar()
        slider.set('1.00')
       
        self.scale_widget = tk.Scale(self.sidebar_frame, from_=1.0, to=13.00,resolution=0.01,length=300, command=lambda s:slider.set('%0.2f' % float(s)),orient=tk.HORIZONTAL)
        self.scale_widget.set(self.Camera.get_gain())
        self.scale_widget.grid(row=9, column=0, padx=20, pady=(10, 0))
        
        
        self.scale_widget_exp = tk.Scale(self.sidebar_frame, from_=62.666666666666664, to=977178.9166666666,resolution=10,length=300, command=lambda s:slider.set('%0.2f' % float(s)),orient=tk.HORIZONTAL)
        self.scale_widget_exp.set(self.Camera.get_exposure_time())
        self.scale_widget_exp.grid(row=10, column=0, padx=20, pady=(10, 0))
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        



        


         # add the scrolling to the all elements cause tkinter 
        

        self.main_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.second_frame.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        self.canvas.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        self.sidebar_frame.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        
        


    

        self.switch_value=False        
        self.demarer=False
        self.img=None
        self.frame=None
        
        self.show()
        self.img=None
        self.result_zone=[]
        self.code_piece=None        
        self.clic_counter =0
        self.data_client=None
        
        
        


         


            # Switch is OFF
            
            # Add your actions here when the switch is OFF

    def fit_and_center_image(self, canvas, img, width, height):
        img_width, img_height = img.size
        scale = min(width / img_width, height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        img = img.resize((new_width, new_height), Image.LANCZOS)

        x_offset = (width - new_width) // 2
        y_offset = (height - new_height) // 2

        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(x_offset, y_offset, anchor="nw", image=img_tk)
        canvas.image = img_tk
        return img_tk


    def resize_image(self, img, max_width, max_height):
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height

        if img_width > img_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

        # Ensure the new dimensions do not exceed the maximum dimensions
        new_width = min(new_width, max_width)
        new_height = min(new_height, max_height)

        return img.resize((new_width, new_height), Image.LANCZOS)




            
            
    def capt(self):
        self.lire_fichier_json()
        
        print("capt---",self.data_client)
        t1=threading.Thread(target=self.metier.capt(self.frame))
        t1.start()
        t1.join()
        
        self.clic_counter += 1
        self.label_clic.configure(text=f"Limite numéro {self.clic_counter} bien effectué")
        
        
    def show(self):
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas)
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas2)
        self.t = threading.Thread(target=self.update)
        self.t.start()

        # Show the self.canvas
        self.canvas.grid()   
        #self.canvas.grid(row=0, column=1, columnspan=2, padx=(5, 0), pady=(20, 0), sticky="nsew")

        #self.canvas.pack(side=LEFT, fill=BOTH, expand=1)


    def update(self):
       
        # Read a frame from the camera
        
        try :
            if  self.Camera.live() is  not None and self.switch_value==False :
         
                self.frame = self.Camera.live()
                #self.frame = cv2.rotate( self.frame, cv2.ROTATE_180)
                #frame = self.resize_image(img, self.canvas.winfo_width(), self.canvas.winfo_height())
                frame=cv2.resize(self.frame, (self.canvas.winfo_width(),self.canvas.winfo_height()))

                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            else:
                frame=cv2.resize(self.frame, (self.canvas.winfo_width(),self.canvas.winfo_height()))
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                

            # Convert the OpenCV image to a PIL image
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2image))
  
            # Display the camera footage on the self.canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
  
            # Schedule the next update in 10 milliseconds
            self.after(500, self.update)
        except Exception as e:
            print( "Exception_def1", str(e))


    # Stop the camera and show the index page
    def fermer_app(self):
       # self.attributes('-fullscreen', False)
       self.withdraw()
       
    def lire_fichier_json(self):
        nom_fichier_json=("donnees.json")
        # Ouvrir le fichier JSON et charger les données
        with open(nom_fichier_json, 'r') as fichier_json:
            self.data_client = json.load(fichier_json)

        

    
 


        


import  json 
import requests




class Nuance(customtkinter.CTkFrame):
    #customtkinter.set_appearance_mode('dark')
    
    def __init__(self, parent=None, controller=None):
     
        self.Camera=Camera.get_instance()
        self.metier=Metier_nuance()


        t1=time.time()
        #self.detector.process_image()
        t2=time.time()
        print("run",t2-t1)
        
        self.zones_dict={}
        
        
        
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.frame=None



        image_path=os.path.join(os.path.dirname(__file__),"test_images","sartex.png")

        # Set up the camera
        self.pred_count = 0
        self.pred_count_2=0
        self.cap = None
        self.photo = None
        self.data={'poi': '____', 'client': '____ ', 'saison':'____','model':' ____-', 'lavage': '_____', 'tissu': '_____ ', 'elasticite':'______' , 'idPiece':'_____' , 'etape': '____'}

        self.image_path=None

        
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=1)

        self.main_canvas = tk.Canvas(self.main_frame, bg="#212121", highlightthickness=0)
        self.main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        
        

        # Add A Scrollbar To The main_canvas
        self.my_scrollbar = tk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.main_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Create ANOTHER Frame INSIDE the self.main_canvas
        self.second_frame = customtkinter.CTkFrame(self.main_canvas,fg_color=("#B2D8FF","#6687E5"))
        self.second_frame.pack(fill=BOTH, expand=1)
        left_image = Image.open(r"./pages/test_images/logo-sartex.png")
        w, h = left_image.size
        self.left_image = customtkinter.CTkImage(left_image, size=(w//2, h//2))
        self.left_image_label = customtkinter.CTkLabel(self.second_frame, image=self.left_image, text="")
        self.left_image_label.grid(row=0,column=0,padx=(10, 0), pady=(0, 0), sticky="nw")
        
        left_image = Image.open(r"./pages/test_images/sartex1.png")
        w, h = left_image.size
        self.left_image = customtkinter.CTkImage(left_image, size=(w//2, h//2))
        self.left_image_label = customtkinter.CTkLabel(self.second_frame, image=self.left_image, text="")
        self.left_image_label.grid(row=0,column=0,padx=(200, 0), pady=(0, 5), sticky="nw")
        
        image = Image.open(r'./icons/cancel.png')
        image = image.resize((25, 25), Image.LANCZOS)
        
        image = ImageTk.PhotoImage(image)
        image_button = tk.Button(self.second_frame, image=image,command=lambda: controller.exit_fullscreen())
        image_button.image = image  # to prevent garbage collection of the image
        image_button.grid(row=0,column=5,padx=(0, 0), pady=(0, 0), sticky="en")
        
        
        self.frame_client = customtkinter.CTkFrame(self.second_frame, corner_radius=3,fg_color="transparent",width=600)
        self.frame_client.grid(row=0,column=2,padx=(40, 40), pady=(5, 5), sticky="n")
        
        
     
        
        
        row = 0
        col = 0
        for key, value in self.data.items():
            # Create labels
            label = customtkinter.CTkLabel(self.frame_client, text=key, font=customtkinter.CTkFont(size=12),
                                           text_color="#4D2700")
            label.grid(row=row, column=col, padx=5, pady=5)
        
            # Create entry widgets
            entry = customtkinter.CTkEntry(self.frame_client, placeholder_text="This doesnt do anything yet",
                                           text_color="#FFFFFF")
            entry.grid(row=row, column=col + 1, padx=2, pady=2)
        
            # Set entry widget value
            entry.insert(0, value)
        
            col += 2  # Move to the next column (skip one column)
        
            # If we reach the 8th column, move to the next row
            if col >= 12:
                col = 0
                row += 1

        

        

        self.scrollable_frame_switches1 = []
        self.scrollable_frame_switches2=[]

        self.measure_ref = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="#E0EFFF",height=200)
        self.measure_ref.grid(row=1,column=0, sticky="we",columnspan=6,padx=(20, 0), pady=(0, 0))
        self.measure_ref.grid_rowconfigure(8, weight=1)
        
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.measure_ref,width=1050,height=150,orientation="horizontal", label_text="Les limites",fg_color="#E0EFFF")
        self.scrollable_frame.grid(row=0,column=2,columnspan=12, padx=(200, 0), pady=(0, 0), sticky="nsw")
        self.qr_code = customtkinter.CTkEntry(self.measure_ref, placeholder_text="This doesnt do anything yet")
        self.qr_code.grid(row=0, column=22, padx=(30, 2), pady=(0,15), sticky="e")
        self.main_button_1 = customtkinter.CTkButton(self.measure_ref,text="enter QR code", fg_color="#0076FF", border_width=2,command=self.up_client)
        self.main_button_1.grid(row=0, column=25, padx=(30, 2), pady=(0, 15), sticky="e")
        
        self.measure_frame1 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="transparent")
        self.measure_frame1.grid(row=2,column=0, sticky="we",columnspan=6,padx=(20, 0), pady=(0, 0))
        
        #self.measure_frame1.grid_rowconfigure(2, weight=1)
        self.measure_frame = customtkinter.CTkFrame(self.measure_frame1, width=450, height=300, corner_radius=0,fg_color="#E0EFFF")
        self.measure_frame.grid(row=0, column=0, rowspan=6,columnspan=1, padx=(5, 0), pady=(5, 0), sticky="nsw")
        # create scrollable frame on the top right
        self.resultat_frame1 = customtkinter.CTkFrame(self.measure_frame,height=500,width=450,fg_color="#E0EFFF")
        self.resultat_frame1.grid(row=0, column=0,columnspan=2,rowspan=2, padx=(5, 0), pady=(5, 0), sticky="nsew")
        self.label_c = customtkinter.CTkLabel(self.resultat_frame1, text="Resultat",text_color="black",width=150,font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_c.grid(row=5, column=2, padx=5,  pady=(20, 0), sticky="nsw")
        
        
        
        # create the camera canvas
        self.canvas = customtkinter.CTkCanvas(self.measure_frame1,background='#212121',highlightthickness=0,height=500,width=50)
        self.canvas.grid(row=0, column=2, padx=(0, 0), pady=(5, 0), sticky="w")
        
        
        self.sidebar_frame = customtkinter.CTkFrame(self.measure_frame1, width=140,  height=200,corner_radius=0,fg_color="#E0EFFF")
        self.sidebar_frame.grid(row=0, column=8, rowspan=6, padx=(0, 0), pady=(5, 0),sticky="nse")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,text_color="black" ,text=" CONTROLE Nuance", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(5, 5))
        
        self.go_scan = customtkinter.CTkButton(self.sidebar_frame,text="Création  limite", command=self.scan_limit)
        self.go_scan.grid(row=2, column=0, padx=20, pady=5)
        
        self.on_image = Image.open(r"./pages/on.png")
        self.on_image =  self.on_image.resize((150, 50), Image.LANCZOS)  # Adjust the size as needed
        self.on_image = ImageTk.PhotoImage( self.on_image)
        
        self.off_image = Image.open(r"./pages/off.png")
        self.off_image =  self.off_image.resize((150,50), Image.LANCZOS)  # Adjust the size as needed
        self.off_image = ImageTk.PhotoImage( self.off_image)
        self.switch_var = tk.IntVar()
        self.switch_var.set(0)  # Initialize the switch to OFF

        # Create the on-off switch (Checkbutton)
        self.switch = ttk.Checkbutton(self.sidebar_frame, variable=self.switch_var,
                                      onvalue=1, offvalue=0, command=lambda: self.toggle_switch(self.switch_var))
        self.switch.grid(row=3, column=0, padx=20, pady=5)
        
        left_image = Image.open(r"./pages/test_images/sartex1.png")
        w, h = left_image.size
        self.left_image = customtkinter.CTkImage(left_image, size=(w*1, h*1))
        self.left_image_label = customtkinter.CTkLabel(self.sidebar_frame, image=self.left_image, text="")
        self.left_image_label.grid(row=4,column=0,padx=(20, 0), pady=(0, 5), sticky="we")
        # Set the images for on and off states

       
     
        slider = tk.StringVar()
        slider.set('1.00')
       
        self.scale_widget = tk.Scale(self.sidebar_frame, from_=1.0, to=13.00,resolution=0.01,length=300, command=lambda s:slider.set('%0.2f' % float(s)),orient=tk.HORIZONTAL)
        self.scale_widget.set(self.Camera.get_gain())
        
        self.scale_widget.grid(row=5, column=0, padx=20, pady=(5, 0))
        
        
        self.scale_widget_exp = tk.Scale(self.sidebar_frame, from_=62.666666666666664, to=977178.9166666666,resolution=10,length=300, command=lambda s:slider.set('%0.2f' % float(s)),orient=tk.HORIZONTAL)
        self.scale_widget_exp.set(self.Camera.get_exposure_time())
        self.scale_widget_exp.grid(row=6, column=0, padx=20, pady=(5, 0))
 
        self.go_back = customtkinter.CTkButton(self.sidebar_frame,text="generer PDF", command=self.metier.gene_pdf)
        self.go_back.grid(row=7, column=0, padx=20, pady=5)
        self.go_back = customtkinter.CTkButton(self.sidebar_frame,text="go back", command=self.go_)
        self.go_back.grid(row=8, column=0, padx=20, pady=5)

        
        
        self.switch.config(image= self.off_image, compound=tk.LEFT)
        self.switch.image =  self.off_image  # Keep a reference to avoid garbage collection
        # Create and configure a Scale widget
     
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
       
        self.product_dict = {"centure":0.0,"motant_devant":0.0,"entre jambe":0.0 ,"longu_measure":0.0,"cuise_m_1":0.0,"leg_opening":0.0}



        


         # add the scrolling to the all elements cause tkinter 
        self.main_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.second_frame.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        self.second_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        self.canvas.bind("<MouseWheel>", self.on_mousewheel) 
        self.sidebar_frame.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        self.sidebar_frame.bind("<MouseWheel>", self.on_mousewheel)
        
        
        
        self.selection_rectangle = None
        self.selection_start = None
        self.selection_active = False  # Indicateur de sélection active


        self.last_image_count = 0 
        self.cropped_images_dir = r"./cropped_zones"
        

    
# Start a separate thread to monitor for new images
        
      

        
        
        
        
        
        
        
        self.switch_value=False        
        self.demarer=False
        self.img=None
        
        self.show()
        self.img=None
        self.result_zone=[]
        self.code_piece=None
        self.scan=False
        
        #self.box()
        
       
        
       

#function--------------------------------------------------------------
    def get_client(self,client): 
    
        data_to_send = {
                "idpiece": client
    
            }
        
        # URL du service web
        data_json = json.dumps(data_to_send)
        print(data_json)
         
         # URL du service web
        url = "http://192.168.0.70/WebServices/rooting/RepriseIntraService/getDetailPiece"
         
         # Spécifier les en-têtes de la requête
        headers = {'Content-Type': 'application/json'}
        
       
    
        try: 
            response = requests.post("http://192.168.0.70/WebServices/rooting/RepriseIntraService/getDetailPiece", data=data_to_send)
            response.raise_for_status()  # Vérifier si la requête a réussi
            #print(response.json())  # Renvoyer la réponse JSON du service web
            # Vérifier la réponse du service web
            if response.status_code == 201:
                print("Données envoyées avec succès au service web.")
                print("req_envoyé:", data_to_send)
                print(response)
                print("js", response.json())
    
                # Extract only the specific keys you need
                desired_keys = ['poi', 'client', 'saison', 'model', 'lavage', 'tissu', 'elasticite', 'idPiece', 'etape']
                filtered_data = {key: response.json()[key] for key in desired_keys}
                filtered_data['code_piece'] = client
                
                return filtered_data
    
            else:
                print(f"Erreur lors de l'envoi des données au service web. Code de statut : {response.status_code}")
                print(data_to_send)
                return None
    
        except requests.exceptions.RequestException as e:
            print("Erreur lors de l'envoi de la requête :", str(e))
            return None
    
    #data = get_client(code)
    def widget_client(self,data):
        row = 0
        col = 0
        for key, value in self.data.items():
            # Create labels
            label = customtkinter.CTkLabel(self.frame_client, text=key, font=customtkinter.CTkFont(size=12),
                                           text_color="#4D2700")
            label.grid(row=row, column=col, padx=5, pady=5)
        
            # Create entry widgets
            entry = customtkinter.CTkEntry(self.frame_client, placeholder_text="This doesnt do anything yet",
                                           text_color="#FFFFFF")
            entry.grid(row=row, column=col + 1, padx=2, pady=2)
        
            # Set entry widget value
            entry.insert(0, value)
        
            col += 2  # Move to the next column (skip one column)
        
            # If we reach the 8th column, move to the next row
            if col >= 12:
                col = 0
                row += 1
        
    
    def up_client(self):
        value=self.qr_code.get()
        self.data=self.get_client(value)
        self.widget_client(self.data)
        nom_fichier_json = 'donnees.json'

# Enregistrez le dictionnaire dans un fichier JSON
        with open(nom_fichier_json, 'w') as fichier_json:
            json.dump(self.data, fichier_json)
        
    
    def is_folder_empty(self, folder_path): 
        return not any(os.scandir(folder_path))
    
    
    def start(self):
        self.progressbar = customtkinter.CTkProgressBar(self.second_frame,determinate_speed=5,indeterminate_speed=2,mode="determinate",height=50,width=950,corner_radius=30,border_width=10,fg_color="black",progress_color="#F8FC7F",border_color="black")
        self.progressbar.grid(row=2, column=1,columnspan=2, pady=(5, 0),padx=(5, 0))
        self.progressbar.set(0)
        progres=1/25
        stepval=0 
        for i in range(25):
            for j in range(1000000):
                pass
            stepval=stepval+progres
            self.progressbar.set(stepval)
            self.progressbar.update_idletasks()
        
    def box(self):
        cropped_images_dir="./cropped_zones"
        self.draw_bounding_boxes(self.scrollable_frame,cropped_images_dir,  self.scrollable_frame_switches1)
        self.after(500,self.box)
    def ask_question(self):
        # get yes/no answers
        msg = CTkMessagebox(title="INFO?", message="Il est important d'apprendre les limites avant de commencer ?",
                            icon="warning", option_1="Exit", option_2="Non", option_3="Oui")
        response = msg.get()
        
        if response=="Oui":
            self.t1 = threading.Thread(target=self.box)
            self.t1.start()
            self.charger_interface()


    def toggle_switch(self, switch_var):
        self.switch_value = switch_var.get()
        
        ref=self.is_folder_empty(r"./cropped_zones")
        
        if self.switch_value == True :
            if  ref==True:
                self.switch_var.set(0)
                self.ask_question()
                self.scan=True
            else:
                print("Switch is ON")
                self.switch.config(image=self.on_image)
                self.p = threading.Thread(target=self.start)
                self.d = threading.Thread(target=self.run_detection)
                
                self.d.start()
                self.p.run()
                self.scan=False
                

                # Switch is ON
                cropped_images_dir="./hors_limite"
              
                
                
                t1=time.time()
                t2=time.time()
                print("run_all",t2-t1)     
                self.progressbar.grid_forget()
                self.metier.gene_pdf()
                
                #self.t1 = threading.Thread(target=self.draw_bounding_boxes(self.scrollable_frame1,cropped_images_dir,self.scrollable_frame_switches1))
                #self.t1.start()
                # Add your actions here when the switch is ON
                
        else:
            self.switch.config(image=self.off_image)
            print("Switch is OF")
            self.label_c.configure(text=" ",text_color="red")
            
            
            #for widget in self.scrollable_frame1.winfo_children(): 
                #widget.destroy()
            


    def fit_and_center_image(self, canvas, img, width, height):
        img_width, img_height = img.size
        scale = min(width / img_width, height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        img = img.resize((new_width, new_height), Image.LANCZOS)

        x_offset = (width - new_width) // 2
        y_offset = (height - new_height) // 2

        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(x_offset, y_offset, anchor="nw", image=img_tk)
        canvas.image = img_tk
        return img_tk





    def resize_image(self, img, max_width, max_height):
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height

        if img_width > img_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)

        # Ensure the new dimensions do not exceed the maximum dimensions
        new_width = min(new_width, max_width)
        new_height = min(new_height, max_height)

        return img.resize((new_width, new_height), Image.LANCZOS)

    
   
    def run_detection(self):
      
        t1=time.time()
        image = self.frame
        verif=self.metier.capt_proc(image)   
        if  verif==True :
            self.label_c.configure(text="Pièce_conforme ",text_color="green")
        else :
            self.label_c.configure(text="pièce_non_conforme ",text_color="red") 
        t2=time.time()
        print("mesure&def____",t2-t1)






    def draw_bounding_boxes(self,scrollable_frame,cropped_images_dir,scrollable_frame_switches):
        cropped_images_dir=cropped_images_dir
        scrollable_frame=scrollable_frame
        scrollable_frame_switches=scrollable_frame_switches
        
        for widget in scrollable_frame.winfo_children(): 
            widget.destroy()
       
        # Create a directory for cropped images if it doesn't exist
        if not os.path.exists(cropped_images_dir):
            os.makedirs(cropped_images_dir)
            
        
            
        for path in os.listdir(cropped_images_dir): 
            cropped_image = Image.open(os.path.join(cropped_images_dir, path))
            img = cropped_image.copy()
            original_width, original_height = img.size
            img = self.resize_image(img, self.canvas.winfo_width(), self.canvas.winfo_height())
            new_width, new_height = img.size
            width_scale = new_width / original_width
            height_scale = new_height / original_height
            if cropped_images_dir=="./hors_limite":
                cropped_img_canvas = Canvas(scrollable_frame, background='#292929',highlightthickness=0, width=300, height=300)
                cropped_img_canvas.grid(row=self.pred_count, column=0, padx=2, pady=(0, 5))
            else:
                cropped_img_canvas = Canvas(scrollable_frame, background='#292929',highlightthickness=0, width=300, height=300)
                cropped_img_canvas.grid(row=0, column=self.pred_count, padx=2, pady=(0, 5))
                
        
        
            self.fit_and_center_image(cropped_img_canvas, img, 230, 266)
            scrollable_frame_switches.append(img)
            cropped_img_canvas.bind("<Button-1>", lambda event, path=os.path.abspath(os.path.join(cropped_images_dir, path)): self.open_image(path))
            self.pred_count += 1







    def on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        




    # Start the camera when this page is shown
    def show(self):
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas)
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas2)
        self.update()

        # Show the self.canvas
        self.canvas.grid()   
        #self.canvas.grid(row=0, column=1, columnspan=2, padx=(5, 0), pady=(20, 0), sticky="nsew")

        #self.canvas.pack(side=LEFT, fill=BOTH, expand=1)



    def update(self):
        self.scale_value=self.scale_value_changed(self.scale_widget)
        self.scale_value_exp=self.scale_value_changed(self.scale_widget_exp)
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas)
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas2)

       
        # Read a frame from the camera
        
        try :
            if  self.Camera.live() is  not None and self.switch_value==False :
         
                self.frame = self.Camera.live()
                #self.frame = cv2.rotate( self.frame, cv2.ROTATE_180)
                #frame = self.resize_image(img, self.canvas.winfo_width(), self.canvas.winfo_height())
                frame=cv2.resize(self.frame, (self.canvas.winfo_width(),self.canvas.winfo_height()))

                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            else:
                frame=cv2.resize(self.frame, (self.canvas.winfo_width(),self.canvas.winfo_height()))
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                
                
        # Resize the canvas and the frame to fit the window
            resize_canvas(self.sidebar_frame,self.measure_frame, self, self.canvas)
    
  
          
            # Convert the OpenCV image to a PIL image
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2image))
  
            # Display the camera footage on the self.canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
  
            # Schedule the next update in 10 milliseconds
            self.after(450, self.update)
        except Exception as e:
            print( "Exception_def1", str(e))



    # Stop the camera and show the index page
    def go_(self):
        self.controller.show_frame("Index")
  
    def scan_limit(self):

        
        self.t1 = threading.Thread(target=self.box)
        self.t1.start()
        self.charger_interface()
    
    def charger_interface(self):
        container = tk.Frame(self)
        viewer = Limit_ref()
        viewer.mainloop()

        # Start the camera when this page is shown
    def scale_value_changed(self,scale_widget):
        scale_widget=scale_widget
        # This function will be called when the scale value changes
        scale_value = scale_widget.get()
        #print("Scale value:", scale_value)
        return scale_value
    
    
    
    def open_image(self, path):
        # Check if the file exists before opening the image viewer
        if os.path.exists(path):
            # Create an instance of the image viewer and pass the image path to it
            viewer = ImageViewer(path)
            viewer.mainloop()
        else:
            print(f"Error: File not found at path {path}") 
            

        


