# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 08:34:35 2023

@author: user
"""


import  numpy  as  np  
import time
import  colorsys
import  cv2
import  os  

import threading

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor

from detectron2.config import get_cfg



def detection_task(args):
    detector, zone_name, zone_image = args
    return detector.detection(zone_name, zone_image)




class Backend_defect: 
    def __init__(self, predictor=None):
        self.lock = threading.Lock()
        #self.rows=6
        #self.columns =4
        self.rows=4
        self.columns =6
        self.cropped_img = None
        self.zones_dict = {}
        self.predictor = predictor if predictor is not None else self.initialize_predictor()
        
        self.count=0
        self.res=[]
     
        
     
        
     
    def initialize_predictor(self):
        # Initialize the model only once for each process
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
        cfg.MODEL.DEVICE = 'cuda'
        #cfg.DATALOADER.NUM_WORKERS = 4
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 2  # hand
        cfg.MODEL.RETINANET.NUM_CLASSES = 2
        
        cfg.MODEL.WEIGHTS = 'model_final.pth'  # Replace with the correct path to detection.pth
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.1 # set a custom testing threshold
        
        # Return the predictor for this process
        return DefaultPredictor(cfg)
    
    
    
    def gamma_correction(self,image):
        gamma=1
        adjusted = np.power(image / 255.0, 1.0 / gamma)
        adjusted = np.uint8(adjusted * 255)
        
        
        return adjusted
    
    

    def detection(self, name, im):
        
        modified_name = name  # Use a new variable to store the modified name
        output_images_dir = r"./cropped_zones"
        output_text_dir = r"./rectangles_folder"
        image_12=r"./res.png"
        image_originale = self.cropped_img

    
        im1 = self.gamma_correction(im)
        hauteur, largeur = im.shape[:2]
      
        t1 = time.time()
        im1 = np.array(im1)

        im1 = np.clip(im1, 0, 255).astype(np.uint8)
        outputs = self.predictor(im1)
        t2 = time.time()
        print("predictor", t2 - t1)
        instances = outputs["instances"].pred_boxes.tensor.cpu().numpy()
    
        # Vérifier s'il y a des objets détectés
        if len(instances) > 0:
            im_with_detections = im.copy()
            detected_objects_info = []
    
            for i, box in enumerate(instances):
                #print(name,box)
                x0, y0, x1, y1 = box
                x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
                
                cv2.rectangle(im_with_detections, (x0, y0), (x1 + 10, y1 + 10), (255, 0, 0), 1)
                #cv2.rectangle(image_originale, (int(x0), int(y0)), (int(x1) + 10, int(y1) + 10), (255, 0, 0), 1)  # (0, 255, 0) est la couleur du rectangle (vert)
                # Dessiner également sur l'image d'origine
                cv2.putText(im_with_detections, f"def {i + 1}", (int(x0), int(y0) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 3)

                  
                x3,y3,x4,y4=self.zones_dict[modified_name]['coordinates'] 
                cv2.rectangle(image_originale, (x3+x0, y3+y0), (x3+x1, y3+y1), (0, 255, 0), 6)  
               


    
                # Save coordinates in detected_objects_info list
                object_info = {"def": f"def_{i + 1}", "x0": int(x0), "y0": int(y0), "x1": int(x1) + 10, "y1": int(y1) + 10}
                detected_objects_info.append(object_info)
    
            # Save coordinates to a text file
            output_path = "res.png"  # Specify the desired output path
            cv2.imwrite(output_path, image_originale)
            output_text_path = os.path.join(output_text_dir, f"{modified_name}.txt")
            with open(output_text_path, "w") as file:
                for obj_info in detected_objects_info:
                    file.write(f"{obj_info['x0']},{obj_info['y0']},{obj_info['x1']},{obj_info['y1']}\n")
    
            # Save annotated image
            output_image_path = os.path.join(output_images_dir, modified_name)
            cv2.imwrite(output_image_path, im_with_detections)
            return True
        else:
            return False




                
            # Save the image with the modified name and proper file extension
    def detection_wrapper(self,args): 
        
        return self.detection(*args)    
        
    def process_image(self,frame):
        
        frame=frame
        self.capture_frame_and_save(frame)
        for i in os.listdir(r"./cropped_zones"):
            os.remove(os.path.join(r"./cropped_zones", i))
        #num_processes = multiprocessing.cpu_count()
        #task_func = partial(detection_task, detector=self)
        #tasks = [(zone_name) for zone_name, zone_info in self.zones_dict.items()]

    

        t1=time.time()
        for zone_name, zone_info in self.zones_dict.items():
            self.res.append(self.detection(zone_name, zone_info['image']))
    
        '''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [(zone_name, zone_info['image']) for zone_name, zone_info in self.zones_dict.items()]
            t1=time.time()
            self.res=list(executor.map(lambda args: self.detection(*args), tasks))
            t2=time.time()
            print("run",t2-t1)
        '''
        
        #im=self.verif()   
        """
        # Use multiprocessing instead of threading
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [(zone_name, zone_info['image']) for zone_name, zone_info in self.zones_dict.items()]
            results = list(executor.map(detection_task, [(self, *task) for task in tasks]))

        """
        t2=time.time()
        print("detection",t2-t1)
        #cv2.imwrite("res.png",im)
            
                # Si le résultat de la détection est True, dessiner un rectangle sur l'image originale

                    
    
    


        
        
        
        

        
        
        
        
        
    def dect_zone(self):
        #self.image_path = "webcam_frame.png"
        self.img = self.cropped_img
        height, width = self.img.shape[:2]
        rows=self.rows
        columns =self.columns
        tile_width = width // columns
        tile_height = height // rows
    
        zones = {}
        for i in range(rows):
            for j in range(columns):
                x1 = j * tile_width
                y1 = i * tile_height
                x2 = x1 + tile_width
                y2 = y1 + tile_height
    
                zone_img = self.img[y1:y2, x1:x2].copy()
    
                index = (j + (columns * i)) + 1
                name = str(index) + ".png"
                zone_info = {'coordinates': (x1, y1, x2, y2), 'image': zone_img}
                self.zones_dict[name] = zone_info

                #print("zone zone",self.zones_dict.keys() )

    def capture_frame_and_save(self,frame):
        # Capture a single frame

        
        # Save the frame as an image
        image_path = "webcam_frame.png"

        image = frame
       
        self.cropped_img = image
        
        #cropped_img = cv2.cvtColor(self.cropped_img, cv2.COLOR_RGB2GRAY)
        cv2.imwrite("webcam_frame.png", self.cropped_img)
        self.thread_zone = threading.Thread(target=self.dect_zone)
        self.thread_zone.start()
        self.thread_zone.join()
        #cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        
        
        
       
 


""" 

   def verif(self):
      
       # Read a frame from the camera

        
       
       #frame = self.resize_image(img, self.canvas.winfo_width(), self.canvas.winfo_height())
       frame=self.cropped_img
       # Split the frame into 6 zones
       height, width = frame.shape[:2]
       rows=self.rows
       columns =self.columns
       tile_width = width // columns
       tile_height = height // rows
       #♣cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

 
       # Draw rectangles around the zones
       for i in range(rows):
           for j in range(columns):
               x1 = j * tile_width
               y1 = i * tile_height
               x2 = x1 + tile_width
               y2 = y1 + tile_height
               index =(j+(columns*i))+1
               if self.res[index-1]==True:
                   cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                   cv2.putText(frame, "defect", (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
               

               else:
                  cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                  cv2.putText(frame, "z_"+str(index), (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 2)
       self.res=[]
       return  frame             
if __name__ == "__main__":


   

    # Create the DefectDetector object
    
    detector = Backend_defect()
    predictor = Backend_defect().initialize_predictor()  # Initialize the predictor only once
    detector = Backend_defect(predictor=predictor)
    #detector = Backend_defect()
    
    #detector.capture_frame_and_save()
    t1=time.time()
    detector.process_image()
    t2=time.time()
    print("run",t2-t1)
"""
   

