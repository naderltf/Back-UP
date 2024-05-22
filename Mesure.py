import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox, filedialog

import os
import glob
from IDS_cam import Camera



import requests
import base64
import json
import customtkinter
import cv2
from scipy.spatial import distance
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageTk,ImageGrab,ImageDraw,ImageFont
import threading
import platform
import subprocess
import time
#from IDS_cam import Camera
#from ids_peak import ids_peak
import  datetime
import  numpy as np  
from  imutils  import  contours 
import  imutils
import shutil
# import some common detectron2 utilities
#from pages.Backend_defect import Backend_defect
from pages.Backend_mesure import Backend_mesure
import tkinter.messagebox as messagebox
#--------------------------
#from .helpers import resize_canvas  
customtkinter.set_default_color_theme("dark-blue")
import concurrent.futures

import numpy as np
import xml.dom.minidom
import xml.dom





class Mesure(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.data={'poi': '____', 'client': '____ ', 'saison':'____','model':' ____-', 'lavage': '_____', 'tissu': '_____ ', 'elasticite':'______' , 'idPiece':'_____' , 'etape': '____'}

        self.Camera=Camera.get_instance()
        
        t1=time.time()
        t2=time.time()
        self.done = False
        self.oval_moves = False
        self.ovals = []
        self.selected_circle = None
        self.oval_x0 = 40
        self.oval_y0 = 40
        self.oval_radius = 4
        self.oval_x1 = 50
        self.oval_y1 = 50
        print("run",t2-t1)
        self.zones_dict={}
        customtkinter.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.frame=None
        image_path=os.path.join(os.path.dirname(__file__),"test_images","sartex.png")

        # Set up the camera
        self.pred_count = 0
        self.cap = None
        self.photo = None
        self.image_path=None

        self.main_frame = Frame(self)
        
        self.main_frame.pack(fill=BOTH, expand=1)

        self.main_canvas = tk.Canvas(self.main_frame, bg="#007DCF", highlightthickness=0)
        self.main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        

        # Add A Scrollbar To The main_canvas
        self.my_scrollbar = tk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.main_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Create ANOTHER Frame INSIDE the self.main_canvas
        self.second_frame = customtkinter.CTkFrame(self.main_canvas,fg_color="#87cefa")
        self.second_frame.pack(fill=BOTH, expand=1)
        left_image = Image.open(r"./pages/test_images/logo-sartex.png")
        w, h = left_image.size
        self.left_image = customtkinter.CTkImage(left_image, size=(w, h))
        self.left_image_label = customtkinter.CTkLabel(self.second_frame, image=self.left_image, text="")
        self.left_image_label.grid(row=0,column=0,padx=(10, 0), pady=(0, 20), sticky="nw")
        
        left_image = Image.open(r"./pages/test_images/sartex1.png")
        w, h = left_image.size
        self.left_image = customtkinter.CTkImage(left_image, size=(w, h))
        self.left_image_label = customtkinter.CTkLabel(self.second_frame, image=self.left_image, text="")
        self.left_image_label.grid(row=0,column=0,padx=(200, 0), pady=(0, 20), sticky="nw")
   

        
        
        

        # Add that New frame To a Window In The self.main_canvas
        #self.main_canvas.create_window((0,0), window=self.second_frame, anchor="center")
        # Créer une nouvelle frame sous le canvas
        self.frame1 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="#007BDF")
        self.frame1.grid(row=0,column=3,padx=(150, 150), pady=(60, 20), sticky="n")
        row = 0
        col = 0
        for key, value in self.data.items():
            # Create labels
            label = customtkinter.CTkLabel(self.frame1, text=key, font=customtkinter.CTkFont(size=12),
                                           text_color="white")
            label.grid(row=row, column=col, padx=5, pady=5)
        
            # Create entry widgets
            entry = customtkinter.CTkEntry(self.frame1, placeholder_text="This doesnt do anything yet",
                                           text_color="#FFFFFF")
            entry.grid(row=row, column=col + 1, padx=2, pady=2)
        
            # Set entry widget value
            entry.insert(0, value)
        
            col += 2  # Move to the next column (skip one column)
        
            # If we reach the 8th column, move to the next row
            if col >= 12:
                col = 0
                row += 1
        
        
        





        # create sidebar frame on the left with widgets
        self.measure_frame1 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="#004CFF")
        self.measure_frame1.grid(row=2,column=0, sticky="we",columnspan=6,padx=(20, 0), pady=(20, 20))
        self.measure_frame1.grid_rowconfigure(11, weight=2)
        
        
        self.measure_frame = customtkinter.CTkFrame(self.measure_frame1, width=450, height=100, corner_radius=0)
        self.measure_frame.grid(row=0, column=0, rowspan=6,columnspan=1, padx=(5, 0), pady=(20, 0), sticky="nsw")
        
        
        
        # create the camera canvas
        self.canvas = customtkinter.CTkCanvas(self.measure_frame1,background='#0032FF',highlightthickness=0,height=500,width=950)
        self.canvas.grid(row=0, column=2,columnspan=6, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        self.sidebar_frame = customtkinter.CTkFrame(self.measure_frame1, width=140,  height=200,corner_radius=0)
        self.sidebar_frame.grid(row=0, column=8, rowspan=6, padx=(20, 0), pady=(20, 0),sticky="nse")
        self.sidebar_frame.grid_rowconfigure(11, weight=1)
        
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="QUALITE CONTROLE MESURE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

       

        customer_array=[]

      

        self.customer_label = customtkinter.CTkLabel(self.sidebar_frame, text="customer info", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.customer_label.grid(row=5, column=0, padx=20, pady=(50, 0))


        for i in range(len(customer_array)):
            self.customer_label = customtkinter.CTkLabel(self.sidebar_frame, text=customer_array[i],anchor="e")
            self.customer_label.grid(row=i+6, column=0, padx=0, pady=(10, 0))



        self.go_back = customtkinter.CTkButton(self.sidebar_frame,text="go back", command=self.go_)
        self.go_back.grid(row=11, column=0, padx=20, pady=20)
        self.g_pdf = customtkinter.CTkButton(self.sidebar_frame,text="generer PDF", command=self.generer)
        self.g_pdf.grid(row=7, column=0, padx=20, pady=10)
        self.g_pdf = customtkinter.CTkButton(self.sidebar_frame,text="Corection _image", command=self.generer)
        self.g_pdf.grid(row=8, column=0, padx=20, pady=10)
        # Create and configure a Scale widget
        # Create and configure a Scale widget
        slider = tk.StringVar()
        slider.set('1.00')
        
        self.scale_widget = tk.Scale(self.sidebar_frame, from_=2.0, to=13.00,resolution=0.01,length=300, command=lambda s:slider.set('%0.2f' % float(s)),orient=tk.HORIZONTAL)
        #self.scale_widget.set(self.Camera.get_gain())
        self.scale_widget.grid(row=9, column=0, padx=20, pady=(10, 0))
        
        
        self.scale_widget_exp = tk.Scale(self.sidebar_frame, from_=0, to=100,resolution=1,length=300, command=lambda s:slider.set('%0.2f' % float(s)),orient=tk.HORIZONTAL)
        #self.scale_widget_exp.set(self.Camera.get_exposure_time())
        self.scale_widget_exp.grid(row=10, column=0, padx=20, pady=(10, 0))
    

       


        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)


        
        # create sidebar frame on the left with widgets
        self.measure_frame2 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="#007BDF",height=600)
        self.measure_frame2.grid(row=3,column=0, sticky="we",columnspan=2,padx=(20, 0), pady=(20, 20))
        self.qr_code = customtkinter.CTkEntry(self.measure_frame2, placeholder_text="This doesnt do anything yet")
        self.qr_code.grid(row=1, column=1, rowspan=6, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(self.measure_frame2,text="enter QR code", fg_color="#007BDF", border_width=2,command=self.up_client)
        self.main_button_1.grid(row=1, column=5, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.scrollable_frame_switches1 = []
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
        self.switch.grid(row=2, column=0, padx=20, pady=10)
        # Set the images for on and off states
        self.switch.config(image= self.off_image, compound=tk.LEFT)
        self.switch.image =  self.off_image  # Keep a reference to avoid garbage collection
        
        
      
        self.product_dict = {"Ceintures":0.0,"motant_devant":0.0,"entre jambe":0.0 ,"longu_measure":0.0,"cuise_m_1":0.0,"leg_opening":0.0}



        


         # add the scrolling to the all elements cause tkinter 
        self.main_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.second_frame.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        self.second_frame.bind("<MouseWheel>", self.on_mousewheel)
       
        self.canvas.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        self.canvas.bind("<MouseWheel>", self.on_mousewheel) 
        
        #self.canvas2.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        #self.canvas2.bind("<MouseWheel>", self.on_mousewheel)
        self.sidebar_frame.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion = self.main_canvas.bbox("all")))
        self.sidebar_frame.bind("<MouseWheel>", self.on_mousewheel)
        
        
        
        self.selection_rectangle = None
        self.selection_start = None
        self.selection_active = False  # Indicateur de sélection active

 
        self.cropped_images_dir = r"./cropped_zones"
        self.last_image_count = 0  # To keep track of the number of images initially
    
           # Start a separate thread to monitor for new images
        
      

        
        
        
        
        

        self.switch_value=False
        
        
        self.demarer=False
        self.img=None
        
        self.show()
        self.img=None
        self.result_zone=[]
        self.code_piece=None
        self.progressbar = customtkinter.CTkProgressBar(self.second_frame,determinate_speed=5,indeterminate_speed=2,mode="indeterminate",height=50,width=750,corner_radius=30,border_width=10,fg_color="black",progress_color="#F8FC7F",border_color="black")

    
        
       


#function--------------------------------------------------------------

    def zoom(self,event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.canvas.scale("all", event.x, event.y, factor, factor)
        
    def on_canvas_click(self,event):
           """        
           global selected_circle
           selected_circle = 2
           print(event.x,event.y,6*"sss")
           """
           distances=[]
           global selected_circle
           if not self.oval_moves :
               for oval_coord in self.ovals_coords:
                   dist = distance.euclidean((event.x,event.y), oval_coord)
                   distances.append(dist)
               self.selected_circle = np.argmin(distances)
               print(self.selected_circle,4*"sssssss")
           
    def move_a(self,event):
           global selected_circle
           if self.selected_circle is not None:
               self.oval_moves = True
               print("MOVING...",self.selected_circle)
               self.canvas.coords(self.ovals[self.selected_circle], event.x-10, event.y-10, event.x+10, event.y+10)
               
    def stop_a(self,event):
           global selected_circle
           if self.selected_circle is not None and self.oval_moves :
               
               print("Coords \n",event.x,event.y)
               """
               self.ovals[self.selected_circle][0] = event.x
               self.ovals[self.selected_circle][1] =  event.y
               """
               if self.selected_circle == 0:
                   print("before moving \n",self.measure_keypoints_,'### \n')
                         
                   print("Left Belt Being in Control")
                   self.measure_keypoints_['left_side_belt']['x'] = event.x * 1.4
                   self.measure_keypoints_['left_side_belt']['y'] = event.y * 1.55
                   self.product_dict['Ceintures'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["left_side_belt"]['x'],self.measure_keypoints_["left_side_belt"]['y'])
                                                                     ,(self.measure_keypoints_["right_side_belt"]['x'],self.measure_keypoints_["right_side_belt"]['y']))/10.12,2)
                   self.product_dict['longu_measure'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["left_side_belt"]['x'],self.measure_keypoints_["left_side_belt"]['y'])
                                                                     ,(self.measure_keypoints_["longu"]['x'],self.measure_keypoints_["longu"]['y']))/10.12,2)
                   print("self.product_dict modified edited\n",self.product_dict)
                   self.display_results_in_table(self.product_dict)
                   self.selected_circle = None
                   
               if self.selected_circle == 1:
                   print("Middle Belt Being in Control")
                   self.measure_keypoints_['belt_middle']['x'] = event.x * 1.4
                   self.measure_keypoints_['belt_middle']['y'] = event.y * 1.55
                   self.product_dict['montant_devant'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["belt_middle"]['x'],self.measure_keypoints_["belt_middle"]['y'])
                                                                     ,(self.measure_keypoints_["montant_devant"]['x'],self.measure_keypoints_["montant_devant"]['y']))/10.12,2)
                   
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 2:
                   print("Right Belt Being in Control")
                   self.measure_keypoints_['right_side_belt']['x'] = event.x * 1.4
                   self.measure_keypoints_['right_side_belt']['y'] = event.y * 1.521 
                   self.product_dict['Ceintures'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["left_side_belt"]['x'],self.measure_keypoints_["left_side_belt"]['y'])
                                                                     ,(self.measure_keypoints_["right_side_belt"]['x'],self.measure_keypoints_["right_side_belt"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 3:
                    print("Braguette Being in Control")
                    self.measure_keypoints_['montant_devant']['x'] = event.x * 1.4
                    self.measure_keypoints_['montant_devant']['y'] = event.y * 1.55
                    self.product_dict['entre_jambe'] = round(distance.euclidean(
                                                                      (self.measure_keypoints_["montant_devant"]['x'],self.measure_keypoints_["montant_devant"]['y'])
                                                                      ,(self.measure_keypoints_["entre_jambe"]['x'],self.measure_keypoints_["entre_jambe"]['y']))/10.12,2)
                    self.product_dict['montant_devant'] = round(distance.euclidean(
                                                                      (self.measure_keypoints_["belt_middle"]['x'],self.measure_keypoints_["belt_middle"]['y'])
                                                                      ,(self.measure_keypoints_["montant_devant"]['x'],self.measure_keypoints_["montant_devant"]['y']))/10.12,2)
                    print("self.product_dict modified edited\n",self.product_dict)
                    self.display_results_in_table(self.product_dict)
                    
               if self.selected_circle == 4:
                   print("Entre Jambe Being in Control")
                   self.measure_keypoints_['entre_jambe']['x'] = event.x * 1.424916
                   self.measure_keypoints_['entre_jambe']['y'] = event.y * 1.55
                   self.product_dict['entre_jambe'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["montant_devant"]['x'],self.measure_keypoints_["montant_devant"]['y'])
                                                                     ,(self.measure_keypoints_["entre_jambe"]['x'],self.measure_keypoints_["entre_jambe"]['y']))/10.12,2)
                   self.product_dict['tour_de_bas'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["longu"]['x'],self.measure_keypoints_["longu"]['y'])
                                                                     ,(self.measure_keypoints_["entre_jambe"]['x'],self.measure_keypoints_["entre_jambe"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 5:
                   print("longu Being in Control")
                   self.measure_keypoints_['longu']['x'] = event.x * 1.424916
                   self.measure_keypoints_['longu']['y'] = event.y * 1.55   
                   self.product_dict['tour_de_bas'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["longu"]['x'],self.measure_keypoints_["longu"]['y'])
                                                                     ,(self.measure_keypoints_["entre_jambe"]['x'],self.measure_keypoints_["entre_jambe"]['y']))/10.12,2)
                   self.product_dict['longu_measure'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["left_side_belt"]['x'],self.measure_keypoints_["left_side_belt"]['y'])
                                                                     ,(self.measure_keypoints_["longu"]['x'],self.measure_keypoints_["longu"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 6:
                   print("cuise_1 Being in Control")
                   self.measure_keypoints_['cuise_1']['x'] = event.x * 1.424916
                   self.measure_keypoints_['cuise_1']['y'] = event.y * 1.55   
                   self.product_dict['cuise_1'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["cuise_1"]['x'],self.measure_keypoints_["cuise_1"]['y'])
                                                                     ,(self.measure_keypoints_["montant_devant"]['x'],self.measure_keypoints_["montant_devant"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 7:
                   print("cuise_2_lower Being in Control")
                   self.measure_keypoints_['cuise_2_lower']['x'] = event.x * 1.424916
                   self.measure_keypoints_['cuise_2_lower']['y'] = event.y * 1.55   
                   self.product_dict['cuise_2'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["cuise_2_lower"]['x'],self.measure_keypoints_["cuise_2_lower"]['y'])
                                                                     ,(self.measure_keypoints_["cuise_2_upper"]['x'],self.measure_keypoints_["cuise_2_upper"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 8:
                   print("cuise_2_upper Being in Control")
                   self.measure_keypoints_['cuise_2_upper']['x'] = event.x * 1.424916
                   self.measure_keypoints_['cuise_2_upper']['y'] = event.y * 1.55   
                   self.product_dict['cuise_2'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["cuise_2_lower"]['x'],self.measure_keypoints_["cuise_2_lower"]['y'])
                                                                     ,(self.measure_keypoints_["cuise_2_upper"]['x'],self.measure_keypoints_["cuise_2_upper"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 9:
                   print("genou_lower Being in Control")
                   self.measure_keypoints_['genou_lower']['x'] = event.x * 1.424916
                   self.measure_keypoints_['genou_lower']['y'] = event.y * 1.55   
                   self.product_dict['tour_jen'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["genou_lower"]['x'],self.measure_keypoints_["genou_lower"]['y'])
                                                                     ,(self.measure_keypoints_["genou_upper"]['x'],self.measure_keypoints_["genou_upper"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               
               if self.selected_circle == 10:
                   print("genou_upper Being in Control")
                   self.measure_keypoints_['genou_upper']['x'] = event.x * 1.424916
                   self.measure_keypoints_['genou_upper']['y'] = event.y * 1.55   
                   self.product_dict['tour_jen'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["genou_lower"]['x'],self.measure_keypoints_["genou_lower"]['y'])
                                                                     ,(self.measure_keypoints_["genou_upper"]['x'],self.measure_keypoints_["genou_upper"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 11:
                   print("v_left Being in Control")
                   self.measure_keypoints_['v_left']['x'] = event.x * 1.424916
                   self.measure_keypoints_['v_left']['y'] = event.y * 1.55 
                   self.product_dict['tour_v'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["v_left"]['x'],self.measure_keypoints_["v_left"]['y'])
                                                                     ,(self.measure_keypoints_["v_right"]['x'],self.measure_keypoints_["v_right"]['y']))/10.12,2)
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 12:
                   print("v_center Being in Control")
                   self.measure_keypoints_['v_center']['x'] = event.x * 1.424916
                   self.measure_keypoints_['v_center']['y'] = event.y * 1.55 
                   self.display_results_in_table(self.product_dict)
               if self.selected_circle == 13:
                   print("v_right Being in Control")
                   self.measure_keypoints_['v_right']['x'] = event.x * 1.424916
                   self.measure_keypoints_['v_right']['y'] = event.y * 1.521 
                   self.product_dict['tour_v'] = round(distance.euclidean(
                                                                     (self.measure_keypoints_["v_left"]['x'],self.measure_keypoints_["v_left"]['y'])
                                                                     ,(self.measure_keypoints_["v_right"]['x'],self.measure_keypoints_["v_right"]['y']))/10.12,2)
                
                   self.display_results_in_table(self.product_dict)
               self.selected_circle = None
           self.oval_moves = False    
                   
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
    def widget_client(self,data):
        row = 0
        col = 0
        for key, value in self.data.items():
            # Create labels
            label = customtkinter.CTkLabel(self.frame1, text=key, font=customtkinter.CTkFont(size=12),text_color="#4D2700")
            label.grid(row=row, column=col, padx=5, pady=5)
        
            # Create entry widgets
            entry = customtkinter.CTkEntry(self.frame1, placeholder_text="This doesnt do anything yet",text_color="#FFFFFF")
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
    def start(self):
        self.progressbar.grid(row=2, column=2,columnspan=2, pady=(0, 0),padx=(0,250 ))
        self.progressbar.set(0)
        progres=1/30
        stepval=0 
        for i in range(30):
            for j in range(1000000):
                pass
            stepval=stepval+progres
            self.progressbar.set(stepval)
            self.progressbar.update_idletasks()
    def toggle_switch(self, switch_var):
        self.switch_value = switch_var.get()
    # Perform actions based on the switch's value
        if self.switch_value == True:
            # Switch is ON
            print("Switch is ON")
            self.switch.config(image=self.on_image)
            t1=time.time()
            
            self.switch.config(image=self.on_image)
            self.d = threading.Thread(target=self.run_detection)
            self.d.start()
            
            
            t2=time.time()
            print("run_all",t2-t1)

            #self.process_image()
            
            
            #self.show()
            # Add your actions here when the switch is ON
        else:
            self.switch.config(image=self.off_image)
            print("Switch is OF")
            
            
        
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




        # Start the camera when this page is shown
    def scale_value_changed(self,scale_widget):
        scale_widget=scale_widget
        # This function will be called when the scale value changes
        scale_value = scale_widget.get()
        #scale_value = 20000 + (float(scale_value) / 100) * (978000 - 20000)
        #print("Scale value:", scale_value)
        return scale_value
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
    def display_results_in_table(self, results):
        # Destroy existing Treeview widget if it exists
        if hasattr(self, 'result_treeview'):
            self.result_treeview.destroy()
    
        # Create a Treeview to display the results in a table
        self.result_treeview = ttk.Treeview(self.measure_frame,height=12)
        self.result_treeview['columns'] = ('Parmeteur', 'valeur')
        self.result_treeview.heading('Parmeteur', text='Parmeteur')
        self.result_treeview.heading('valeur', text='valeur')
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', '16'))  # Change font size to 20


        # Insert data into the Treeview
        for key, value in results.items():
            self.result_treeview.insert('', 'end', values=(key, value))
    
        # Pack and display the Treeview
        self.result_treeview.grid(row=0, column=0, sticky='nsew')
    
        # Optional: Adjust Treeview column widths
        self.result_treeview.column('#0', width=0)  # Hide the default empty column
        self.result_treeview.column('Parmeteur',width=250)
        self.result_treeview.column('valeur', width=250)
        
        


    
        
    def run_detection(self):
        self.progressbar.grid(row=2, column=2,columnspan=2, pady=(0, 0),padx=(0,250 ))

        self.progressbar.start()

        self.code_piece=self.qr_code.get()
        self.mesur=Backend_mesure()
        self.predictor_m= Backend_mesure().initialize_predictor()
        self.mesur = Backend_mesure(predictor=self.predictor_m)
       
        t1=time.time()
        image = self.frame
        print(f"Image {image.shape}entering Model to be detected")
        self.code_piece=self.qr_code.get()
        self.product_dict, self.measure_keypoints_ = self.mesur.detection_m(self.code_piece,image)
        self.measure_keypoints_copy = self.measure_keypoints_
        print("self.product_dict \n",self.product_dict)
        print("Measurement Process Done")
        
        self.display_results_in_table(self.product_dict)
        #self.detector.process_image(image)
        #self.frame=self.detector.process_image(image)
        t2=time.time()
        print(f"{t2-t1} second took to do mesure&def")
        self.progressbar.stop()
        self.progressbar.grid_forget()
        

        print(f"Keypoints coordinates of measure parameters are \n {self.measure_keypoints_}")
        #the image that would be shown in main screen after running detection
        self.frame=cv2.imread("res.png")
        #self.canvas.create_oval(80,80,100,100,fill = "red")
        self.done = True

        
    def generer(self):
        print("prooooduuuct dict \n proood",self.product_dict)
        self.mesur.send_data_and_display_pdf(self.product_dict)

       


        



        

            
            



 



    def on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        




    # Start the camera when this page is shown
    def scale_value_changed_exp(self,scale_widget):
        scale_widget=scale_widget
        # This function will be called when the scale value changes
        scale_value = scale_widget.get()
        scale_value = 20000 + (float(scale_value) / 100) * (978000 - 20000)
        #print("Scale value:", scale_value)
        return scale_value
    def show(self):

        self.update()
       

        # Show the self.canvas
        self.canvas.grid()   
        #self.canvas.grid(row=0, column=1, columnspan=2, padx=(5, 0), pady=(20, 0), sticky="nsew")

        #self.canvas.pack(side=LEFT, fill=BOTH, expand=1)


    
        
        
    
    def update(self):
        self.scale_value=self.scale_value_changed(self.scale_widget)
        self.scale_value_exp=self.scale_value_changed_exp(self.scale_widget_exp)
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas)
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas2)
        #print("s",self.scale_value)
        
        #configuration of camera parameters
        
        self.Camera.set_gain(self.scale_value)
        self.Camera.get_exposure_time()
        self.Camera.set_exposure_time(self.scale_value_exp)
        
       
        # Read a frame from the camera
        
        try :
            #if  self.Camera.live() is  not None and self.switch_value==False :
            if self.Camera.live() is  not None and self.switch_value==False :
                #self.frame = self.Camera.live() #self frame is image that we would process
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
            
            
            if self.done == True :
              """
              self.a = self.canvas.create_oval(
                  self.oval_x0 - self.oval_radius  \
                , self.oval_y0 - self.oval_radius,  \
                  self.oval_x0 + self.oval_radius,  \
                  self.oval_y0 + self.oval_radius,fill = "red")
              self.canvas.bind("<Button-1>", self.on_canvas_click)
              self.canvas.bind("<Motion>", self.move_a)
              self.canvas.bind("<Button-3>", self.stop_a)
              """
              
              #left belt point
              self.left_side_belt = self.canvas.create_oval(
                  self.measure_keypoints_['left_side_belt']['x'] /1.4 - self.oval_radius  \
                , self.measure_keypoints_['left_side_belt']['y'] / 1.55 - self.oval_radius,  \
                  self.measure_keypoints_['left_side_belt']['x'] / 1.4+ self.oval_radius,  \
                  self.measure_keypoints_['left_side_belt']['y']/1.55 + self.oval_radius,fill = "red")
              self.canvas.bind("<Button-1>", self.on_canvas_click)
              self.canvas.bind("<Motion>", self.move_a)
              self.canvas.bind("<Button-3>", self.stop_a)
              
              
              
              #middle belt point
              self.belt_middle = self.canvas.create_oval(
                  self.measure_keypoints_['belt_middle']['x'] /1.4 - self.oval_radius  \
                , self.measure_keypoints_['belt_middle']['y'] / 1.55 - self.oval_radius,  \
                  self.measure_keypoints_['belt_middle']['x'] / 1.4 + self.oval_radius,  \
                  self.measure_keypoints_['belt_middle']['y'] / 1.55 + self.oval_radius,fill = "red")
              self.canvas.bind("<Button-1>", self.on_canvas_click)
              self.canvas.bind("<Motion>", self.move_a)
              self.canvas.bind("<Button-3>", self.stop_a)
              
              self.canvas.create_line(self.measure_keypoints_['left_side_belt']['x'] /1.4,
                                      self.measure_keypoints_['left_side_belt']['y']/1.55 
                                      , self.measure_keypoints_['belt_middle']['x']/1.424916,
                                      self.measure_keypoints_['belt_middle']['y']/1.55, fill="#476042", width=3)
              #right belt point
              self.right_side_belt = self.canvas.create_oval(
                 self.measure_keypoints_['right_side_belt']['x'] / 1.4 - self.oval_radius  \
               , self.measure_keypoints_['right_side_belt']['y'] / 1.521 - self.oval_radius,  \
                 self.measure_keypoints_['right_side_belt']['x'] / 1.4 + self.oval_radius,  \
                 self.measure_keypoints_['right_side_belt']['y'] / 1.521 + self.oval_radius,fill = "red")
              self.canvas.bind("<Button-1>", self.on_canvas_click)
              self.canvas.bind("<Motion>", self.move_a)
              self.canvas.bind("<Button-3>", self.stop_a)
              self.canvas.create_line(self.measure_keypoints_['right_side_belt']['x'] /1.4,
                                      self.measure_keypoints_['right_side_belt']['y']/1.521 
                                      , self.measure_keypoints_['belt_middle']['x']/1.424916,
                                      self.measure_keypoints_['belt_middle']['y']/1.55, fill="#476042", width=3)
              #braguette
              self.montant_devant = self.canvas.create_oval(
                  self.measure_keypoints_['montant_devant']['x'] / 1.4 - self.oval_radius  \
                , self.measure_keypoints_['montant_devant']['y'] / 1.54 - self.oval_radius,  \
                  self.measure_keypoints_['montant_devant']['x'] / 1.4 + self.oval_radius,  \
                  self.measure_keypoints_['montant_devant']['y']/1.54 + self.oval_radius,fill = "red")
              self.canvas.bind("<Button-1>", self.on_canvas_click)
              self.canvas.bind("<Motion>", self.move_a)
              self.canvas.bind("<Button-3>", self.stop_a)
              self.canvas.create_line(self.measure_keypoints_['montant_devant']['x'] /1.4,
                                      self.measure_keypoints_['montant_devant']['y']/1.54 
                                      , self.measure_keypoints_['belt_middle']['x']/1.424916,
                                      self.measure_keypoints_['belt_middle']['y']/1.55, fill="#476042", width=3)
              #entre jambe
              self.entre_jambe = self.canvas.create_oval(
                  self.measure_keypoints_['entre_jambe']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['entre_jambe']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['entre_jambe']['x'] /1.424916+ self.oval_radius,  \
                  self.measure_keypoints_['entre_jambe']['y'] /1.55+ self.oval_radius,fill = "red")
              self.canvas.bind("<Button-1>", self.on_canvas_click)
              self.canvas.bind("<Motion>", self.move_a)
              self.canvas.bind("<Button-3>", self.stop_a)
              self.canvas.create_line(self.measure_keypoints_['montant_devant']['x'] /1.4,
                                      self.measure_keypoints_['montant_devant']['y']/1.54 
                                      , self.measure_keypoints_['entre_jambe']['x']/1.424916,
                                      self.measure_keypoints_['entre_jambe']['y']/1.55, fill="#476042", width=3)
              #longuer
              self.longu = self.canvas.create_oval(
                  self.measure_keypoints_['longu']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['longu']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['longu']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['longu']['y'] /1.55+ self.oval_radius,fill = "red")
              self.canvas.create_line(self.measure_keypoints_['longu']['x'] /1.424916,
                                      self.measure_keypoints_['longu']['y']/1.55 
                                      , self.measure_keypoints_['entre_jambe']['x']/1.424916,
                                      self.measure_keypoints_['entre_jambe']['y']/1.55, fill="#476042", width=3)    
              self.canvas.create_line(self.measure_keypoints_['longu']['x'] /1.424916,
                                      self.measure_keypoints_['longu']['y']/1.55 
                                      , self.measure_keypoints_['left_side_belt']['x'] /1.4,
                                      self.measure_keypoints_['left_side_belt']['y'] /1.55, fill="#476042", width=3)    
              #cuise1
              self.cuise_1 = self.canvas.create_oval(
                  self.measure_keypoints_['cuise_1']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['cuise_1']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['cuise_1']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['cuise_1']['y'] /1.55+ self.oval_radius,fill = "red")
              self.canvas.create_line(self.measure_keypoints_['montant_devant']['x'] /1.4,
                                      self.measure_keypoints_['montant_devant']['y']/1.54 
                                      , self.measure_keypoints_['cuise_1']['x']/1.424916,
                                      self.measure_keypoints_['cuise_1']['y']/1.55, fill="#476042", width=3)   
              #cuise2
              self.cuise_2_lower = self.canvas.create_oval(
                  self.measure_keypoints_['cuise_2_lower']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['cuise_2_lower']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['cuise_2_lower']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['cuise_2_lower']['y'] /1.55+ self.oval_radius,fill = "red")
              self.cuise_2_upper = self.canvas.create_oval(
                  self.measure_keypoints_['cuise_2_upper']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['cuise_2_upper']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['cuise_2_upper']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['cuise_2_upper']['y'] /1.55+ self.oval_radius,fill = "red")
              self.canvas.create_line(self.measure_keypoints_['cuise_2_lower']['x']/1.424916,
                                      self.measure_keypoints_['cuise_2_lower']['y']/1.55 
                                      , self.measure_keypoints_['cuise_2_upper']['x']/1.424916,
                                      self.measure_keypoints_['cuise_2_upper']['y']/1.55, fill="#476042", width=3)    
              #genou
              self.genou_lower = self.canvas.create_oval(
                  self.measure_keypoints_['genou_lower']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['genou_lower']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['genou_lower']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['genou_lower']['y'] /1.55+ self.oval_radius,fill = "red")
              self.genou_upper = self.canvas.create_oval(
                  self.measure_keypoints_['genou_upper']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['genou_upper']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['genou_upper']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['genou_upper']['y'] /1.55+ self.oval_radius,fill = "red")
              self.canvas.create_line(self.measure_keypoints_['genou_lower']['x']/1.424916,
                                      self.measure_keypoints_['genou_lower']['y']/1.55 
                                      , self.measure_keypoints_['genou_upper']['x']/1.424916,
                                      self.measure_keypoints_['genou_upper']['y']/1.55, fill="#476042", width=3)
              #VVVVVVVVVVVVVVVVVVVV
              self.v_left = self.canvas.create_oval(
                  self.measure_keypoints_['v_left']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['v_left']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['v_left']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['v_left']['y'] /1.55+ self.oval_radius,fill = "red")
              self.v_center = self.canvas.create_oval(
                  self.measure_keypoints_['v_center']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['v_center']['y']/1.55 - self.oval_radius,  \
                  self.measure_keypoints_['v_center']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['v_center']['y'] /1.55+ self.oval_radius,fill = "red")
              self.canvas.create_line(self.measure_keypoints_['v_left']['x']/1.424916,
                                      self.measure_keypoints_['v_left']['y']/1.55 
                                      , self.measure_keypoints_['v_center']['x']/1.424916,
                                      self.measure_keypoints_['v_center']['y']/1.55, fill="#476042", width=3)    
              self.v_right = self.canvas.create_oval(
                  self.measure_keypoints_['v_right']['x']/1.424916 - self.oval_radius  \
                , self.measure_keypoints_['v_right']['y']/1.521 - self.oval_radius,  \
                  self.measure_keypoints_['v_right']['x']/1.424916 + self.oval_radius,  \
                  self.measure_keypoints_['v_right']['y'] /1.521+ self.oval_radius,fill = "red")
              self.canvas.create_line(self.measure_keypoints_['v_right']['x']/1.424916,
                                      self.measure_keypoints_['v_right']['y']/1.55 
                                      , self.measure_keypoints_['v_center']['x']/1.424916,
                                      self.measure_keypoints_['v_center']['y']/1.55, fill="#476042", width=3)       
                  
              self.canvas.bind("<Button-1>", self.on_canvas_click)
              self.canvas.bind("<Motion>", self.move_a)
              self.canvas.bind("<Double-Button-1>", self.stop_a)
              self.canvas.bind("<MouseWheel>", self.zoom)
              
              self.ovals = [self.left_side_belt, self.belt_middle, self.right_side_belt,
                            self.montant_devant, self.entre_jambe, self.longu,
                            self.cuise_1,self.cuise_2_lower,self.cuise_2_upper,
                            self.genou_lower, self.genou_upper,
                            self.v_left, self.v_center, self.v_right]
              
              self.ovals_coords = [ [self.measure_keypoints_['left_side_belt']['x'] /1.4,
                              self.measure_keypoints_['left_side_belt']['y'] /1.55],
                             [self.measure_keypoints_['belt_middle']['x'] /1.4,
                              self.measure_keypoints_['belt_middle']['y'] /1.55],
                             [self.measure_keypoints_['right_side_belt']['x'] / 1.4,
                              self.measure_keypoints_['right_side_belt']['y'] / 1.521],
                             
                             [self.measure_keypoints_['montant_devant']['x'] / 1.4,
                              self.measure_keypoints_['montant_devant']['y'] / 1.55],
                             
                             [self.measure_keypoints_['entre_jambe']['x']/1.4,
                              self.measure_keypoints_['entre_jambe']['y']/1.55],
                             
                             [self.measure_keypoints_['longu']['x']/1.4,
                              self.measure_keypoints_['longu']['y']/1.55],
                             
                             [self.measure_keypoints_['cuise_1']['x']/1.4,
                              self.measure_keypoints_['cuise_1']['y']/1.55],
                             
                             [self.measure_keypoints_['cuise_2_lower']['x']/1.4,
                              self.measure_keypoints_['cuise_2_lower']['y']/1.55],
                             [self.measure_keypoints_['cuise_2_upper']['x']/1.4,
                              self.measure_keypoints_['cuise_2_upper']['y']/1.55],
                             
                             [self.measure_keypoints_['genou_lower']['x']/1.4,
                              self.measure_keypoints_['genou_lower']['y']/1.55],
                             [self.measure_keypoints_['genou_upper']['x']/1.4,
                              self.measure_keypoints_['genou_upper']['y']/1.55],
                             
                             [self.measure_keypoints_['v_left']['x']/1.4,
                              self.measure_keypoints_['v_left']['y']/1.55],
                             [self.measure_keypoints_['v_center']['x']/1.4,
                              self.measure_keypoints_['v_center']['y']/1.55],
                             [self.measure_keypoints_['v_right']['x']/1.4,
                              self.measure_keypoints_['v_right']['y']/1.55]
                             
                             ]
              
              
  
            # Schedule the next update in 10 milliseconds
            self.after(600, self.update)
            if self.Camera.live() is  not None and self.switch_value==False:
                if len(self.ovals):
                    for oval in self.ovals:
                        self.canvas.delete(oval)
                    self.ovals = []    
                self.done = False    
        except Exception as e:
            print( "Exception_def1", str(e))


    



 




    # Stop the camera and show the index page
    def go_(self):
        self.controller.show_frame("Index")

           




   


    

    # Adjust the sleep interval based on your requirements
    #
            
    


        
        

