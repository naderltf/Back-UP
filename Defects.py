import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox, filedialog

import os
import glob


import requests
import base64
import json
import customtkinter
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image, ImageTk,ImageGrab,ImageDraw,ImageFont
import threading
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
# import some common detectron2 utilities
#from pages.Backend_defect import Backend_defect
from pages.chek_result import ImageViewer  
from pages.Backend_mesure import Backend_mesure
import tkinter.messagebox as messagebox
#--------------------------
from .helpers import resize_canvas  
customtkinter.set_default_color_theme("dark-blue")
import concurrent.futures

import numpy as np
import xml.dom.minidom
import xml.dom



def count_text_file_lines(text_file_path):
    try:
        with open(text_file_path, 'r') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        return 0
from PIL import Image, ImageTk




# colors for the bboxes
COLORS = ['red', 'orange', 'cyan', 'green', 'blue', 'purple', 'pink', 'black', 'gray']
# classes name
CLASSES = ['Tâche', 'Trace tags', 'Rédeposé', 'Tâche', 'Trace piérre-fil', 'Tâche', 'Plastique / Tags Mal Nettoyé', 'Trace tags', 'Rédeposé', 'Manque arrêt', 'Rédeposé', 'Trou', 'Trou', 'Trou', 'Manque arrêt', "Marque d'aiguille", "Marque d'aiguille", 'Point sauté', 'Plastique / Tags Mal Nettoyé', 'Trace tags', 'Point sauté', 'Plis', 'Manque arrêt', 'Point sauté', 'Manque surpiqure', 'Nuance', 'Trou', 'Epluchage', 'Nuance', 'Echappé', 'Echappé', 'Plis', 'Echappé', 'Tâche', 'Manque surpiqure', 'Point sauté', 'Manque arrêt', 'Epluchage', 'Trou', 'Trace tags', 'Rédeposé', 'Nuance', 'Trace tags', 'Rédeposé', 'Position bride NC', 'Arraché', 'Trace', "Visible à l'exterieur"]

# Some parameters for VOC label
_POSE = 'Unspecified'
_TRUNCATED = '0'
_DIFFICULT = '0'
_SEGMENTED = '0'

class LabelTool(tk.Toplevel):
    def __init__(self,image_path):
        
        self.image_path_def = image_path
        super().__init__()
        self.title("Image ")
        self.geometry("800x400")
        self.w, self.h =  self.maxsize()
        # self.parent.geometry('%dx%d' %(w, h))
        self.state('zoomed')
        self.frame = tk.Frame(self)
        self.frame.pack(fill=BOTH, expand=1)

        # initialize mouse state
        self.STATE = {'click': 0, 'x': 0, 'y': 0}

        # initialize global state
        self.flag = 0
        self.imageList = []     # The list for images path.
        self.outDir = './Labels'    # The path of labelled annotations.
        self.cur = 0    # The index of images path.
        self.total = 0     # The total images.
        self.del_num = 0    # The number of deleted images.
        self.image_name = ''    # The name of precessing image.
        self.label_filename = ''    # The name of .xml.
        self.label_filename1 = ''   # The name of .txt, it's used to check annotations.
        self.tkimg = None   # Image displayed on canvas.
        self.img = None
        self.width = 0     # The size of origin image.
        self.height = 0    # The size of origin image.
        self.depth = 0     # The size of origin image.
        self.color_map = COLORS[0]   # The color of bounding boxes.
        self.class_name = None     # The class name of right-click.
        self.classes_name = []     # All classes of a image.
        self.bboxIdLine = []
        self.bboxIdList = []     # Save drawing handle.
        self.classIdList = []    # Save text handle.
        self.bboxId = None     # Drawing handle.
        self.bboxList = []     # Save all bounding boxes.
        self.hl = None      # Horizontal line.
        self.vl = None      # Vertical line.
        self.coordinate = []
        self.x1 = 0
        self.y1 = 0
        self.xx1 = 0
        self.x2 = 0
        self.yy1 = 0
        self.y2 = 0

        # dir entry & load
        radio_var = IntVar()
        self.label = Label(self.frame, text = 'Label Type:')
        #self.label.place(x = 10, y = 10, width = 70, height = 16)
        self.rad = Radiobutton(self.frame, text = 'rectangle', variable = radio_var, value = 1, command = self.Rectangle)
        #self.rad.place(x = 90, y = 10, width = 80, height = 16)
        self.rad1 = Radiobutton(self.frame, text = 'polygon', variable = radio_var, value = 2, command = self.Polygon)
        #self.rad1.place(x = 180, y = 10, width = 80, height = 16)

        self.label1 = Label(self.frame, text = "Image Path:")
        #self.label1.place(x = 10, y = 40, width = 71, height = 16)
        self.label2 = Entry(self.frame)
        #self.label2.place(x = 90, y = 40, width = 255, height = 20)
        self.label3 = Label(self.frame, text = "Image Size:")
        #self.label3.place(x = 10, y = 70, width = 71, height = 16)
        self.label4 = Label(self.frame, bg='green')
        #self.label4.place(x = 90, y = 70, width = 171, height = 16)
        self.label5 = Label(self.frame, text = "Bounding Box:")
        #self.label5.place(x = 3, y = 100, width = 101, height = 16)
        self.label6 = Label(self.frame, text =  "Doing:     /    ")
        #self.label6.place(x = 120, y = 100 , width = 150, height = 16)
        self.label7 = Label(self.frame, bg = 'white', fg = 'red', anchor = W, text = "x: ")
        #elf.label7.place(x = 270, y = 120, width = 75, height = 20)
        self.label8 = Label(self.frame, bg = 'white', fg = 'red', anchor = W, text = "y: ")
        #self.label8.place(x = 270, y = 145, width = 75, height = 20)


        # main panel for labeling
        self.canvas_w = self.w - 370    # The size of canvas.
        self.canvas_h = self.h - 80
        self.mainPanel = Canvas(self.frame, bg = 'white')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Button-3>", self.popupList)
        self.mainPanel.bind("<Button-2>", self.delete_line)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.mainPanel.place(x = 360, y = 10, width = self.canvas_w, height = self.canvas_h)

        # showing bbox info & delete bbox
        self.listbox = Listbox(self.frame)
        #self.listbox.place(x = 10, y = 120, width = 250, height = 120)
        
        # showing log
        self.label9 = Label(self.frame, text = "Print Log:")
        #self.label9.place(x = 1, y = 280, width = 71, height = 20)
        self.messageList = Listbox(self.frame)
        #self.messageList.place(x = 10, y = 300, width = 336, height = 300)
        #image_path = r'C:/Users/user/Desktop/version_1/ch_1.png'  # Chemin vers l'image spécifique
        self.load_specific_image(image_path)

        # Right-click menu, display class name.
        self.contextMenu = Menu(self.frame)
        self.Classes = StringVar()
        for classes in CLASSES:
            self.contextMenu.add_radiobutton(label = classes, variable = self.Classes, command = self.clickMenu)
        self.protocol("WM_DELETE_WINDOW", self.save_and_exit)
        
        
    def save_and_exit(self):
        self.saveImage()
        self.destroy()
        messagebox.showinfo('Information', 'Image saved successfully!')
    def Rectangle(self):
        self.flag = 0
        self.button.config(state='active')

    def Polygon(self):
        self.flag = 1
        self.button.config(state='active')
    def Load_image(self):
        folder_path =  r'./cropped_zones'  # Chemin vers le dossier d'images
        self.imageList = glob.glob(os.path.join(folder_path, '*.png'))
        if len(self.imageList) == 0:
            messagebox.showinfo('Information', 'No .PNG images found in the specified directory!')
            return

    # Le reste du code reste inchangé


        self.button1.config(state='active')
        self.button2.config(state='active')
        self.button3.config(state='active')
        self.button4.config(state='active')
        self.button5.config(state='active')
        self.cur = 1
        self.total = len(self.imageList)
        self.messageList.insert(END, "The number of images is %d " % self.total)

        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        if not os.path.exists('./label'):
            os.mkdir('./label')

        self.loadImage()

    def load_specific_image(self, image_path):
        self.img = Image.open(image_path)
        size_img = np.shape(self.img)
        self.width = size_img[1]
        self.height = size_img[0]
        self.depth = size_img[2]
        self.img = self.img.resize((self.width*3,self.height*3), Image.ANTIALIAS)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.create_image(0, 0, image=self.tkimg, anchor=NW)
        self.label6.config(text = "Doing: %d/%d" %(self.cur, self.total))
        self.label4.config(text = '(%d, %d, %d)' % (self.width, self.height, self.depth))

        # load labels
        self.clearBBox()
        self.image_name = os.path.split(image_path)[-1].split('.')[0]
        label_name = self.image_name + '.xml'
        self.label_filename = os.path.join(self.outDir, label_name)
        label_name1 = self.image_name + '.txt'
        self.label_filename1 = os.path.join('./label', label_name1)
        if os.path.exists(self.label_filename1):
            with open(self.label_filename1) as f:
                for (ind, line) in enumerate(f):
                    if ind == 0:
                        continue
                    if self.flag == 0:
                        tmp = [t.strip() for t in line.split()]
                        self.bboxList.append(tuple([tmp[0], tmp[1], tmp[2], tmp[3]]))
                        self.classes_name.append(tmp[4])
                        x = float(tmp[0]) * self.canvas_w / self.width
                        y = float(tmp[1]) * self.canvas_h / self.height
                        xx = float(tmp[2]) * self.canvas_w / self.width
                        yy = float(tmp[3]) * self.canvas_h / self.height
                        color = COLORS[(len(self.bboxList) - 1) % len(COLORS)]
                        tmpId = self.mainPanel.create_rectangle(int(x), int(y), int(xx), int(yy), width = 2, outline = color)
                        classId = self.mainPanel.create_text(int(x) + 5, int(y) + 8, text = tmp[4], anchor = W, fill = color)
                        self.bboxIdList.append(tmpId)
                        self.classIdList.append(classId)
                        self.listbox.insert(END, '(%s, %s) -> (%s, %s) -> %s' % (tmp[0], tmp[1], tmp[2], tmp[3], tmp[4]))
                        self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = color)
                    if self.flag == 1:
                        tmp = [t.strip() for t in line.split()]
                        boxes = []
                        self.coordinate = []
                        self.bboxIdLine = []
                        for i in range(0, len(tmp)-1, 2):
                            self.coordinate.append((tmp[i], tmp[i+1]))
                            x = float(tmp[i]) * self.canvas_w / self.width
                            y = float(tmp[i+1]) * self.canvas_h / self.height
                            boxes.append((int(x), int(y)))
                        self.bboxList.append(self.coordinate)
                        self.classes_name.append(tmp[8])
                        color = COLORS[(len(self.bboxList) - 1) % len(COLORS)]
                        classId = self.mainPanel.create_text(boxes[0][0]+5, boxes[0][1]+8, text = tmp[8], anchor = W, fill = color)
                        for i in range(len(boxes)-1):
                            tmpId = self.mainPanel.create_line(boxes[i], boxes[i+1], width = 2, fill = color)
                            self.bboxIdLine.append(tmpId)
                        tmpId = self.mainPanel.create_line(boxes[3], boxes[0], width=2, fill=color)
                        self.bboxIdLine.append(tmpId)
                        self.bboxIdList.append(self.bboxIdLine)
                        self.classIdList.append(classId)
                        self.listbox.insert(END, '(%d,%d)->(%d,%d)->(%d,%d)->(%d,%d)->%s' % (boxes[0][0], boxes[0][1], boxes[1][0], boxes[1][1], boxes[2][0],
                                                                                             boxes[2][1], boxes[3][0], boxes[3][1],self.class_name))
                        self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = color)

    def saveImage(self):
        if self.classes_name:
            img_name = self.image_name + '.jpg'
            shape = [self.width, self.height, self.depth]
            doc = createXML(img_name, shape, self.classes_name, self.bboxList, self.flag)
            writeXMLFile(doc, self.label_filename)

            with open(self.label_filename1, 'w') as f:
                f.write('%d\n' % len(self.bboxList))
                if self.flag == 0:
                    for ind in range(len(self.classes_name)):
                        f.write(' '.join(map(str, self.bboxList[ind])) + ' ' + self.classes_name[ind] + '\n')

                if self.flag == 1:
                    for ind in range(len(self.classes_name)):
                        for box in self.bboxList[ind]:
                            f.write(str(box[0]) + ' ' + str(box[1]) + ' ')
                        f.write(self.classes_name[ind] + '\n')

            self.messageList.insert(END, "Image No. %d saved" % self.cur)
            if len(self.messageList.get(0,END)) > 16:
                self.messageList.delete(1)

    def mouseClick(self, event):
        if self.flag == 0:
            if self.STATE['click'] == 0:
                self.STATE['x'], self.STATE['y'] = event.x, event.y
            else:
                self.x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
                self.y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
                self.xx1 = int(float(self.x1) * self.width / self.canvas_w)
                self.x2 = int(float(x2) * self.width / self.canvas_w)
                self.yy1 = int(float(self.y1) * self.height / self.canvas_h)
                self.y2 = int(float(y2) * self.height / self.canvas_h)
                self.bboxList.append((self.xx1, self.yy1, self.x2, self.y2))
                self.bboxIdList.append(self.bboxId)
                self.bboxId = None
            self.STATE['click'] = 1 - self.STATE['click']

        if self.flag == 1:
            if self.STATE['click'] == 0:
                self.STATE['x'], self.STATE['y'] = event.x, event.y
                x1, x2 = event.x, event.y
                self.x1, self.y1 = event.x, event.y
            else:
                x1, x2 = event.x, event.y
            x1 = int(float(x1) * self.width / self.canvas_w)
            x2 = int(float(x2) * self.height / self.canvas_h)
            self.STATE['x'], self.STATE['y'] = event.x, event.y
            self.coordinate.append((x1, x2))
            if self.bboxId:
                self.bboxIdLine.append(self.bboxId)
            self.STATE['click'] += 1
            if self.STATE['click'] == 4:
                self.STATE['click'] = 0
                self.bboxList.append(self.coordinate)
                self.bboxId = self.mainPanel.create_line(self.STATE["x"], self.STATE['y'], self.x1, self.y1, width=2,
                                                         fill=self.color_map)
                self.bboxIdLine.append(self.bboxId)
                self.bboxIdList.append(self.bboxIdLine)
                self.coordinate = []
                self.bboxIdLine = []

            self.bboxId = None


    def mouseMove(self, event):  
        self.color_map = COLORS[len(self.bboxIdList) % len(COLORS)]
        self.label7.config(text = 'x: %.2f' % event.x)
        self.label8.config(text = 'y: %.2f' % event.y)
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            if self.flag == 0:
                self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], event.x, event.y, width = 2, outline = self.color_map)
            if self.flag == 1:
                self.bboxId = self.mainPanel.create_line(self.STATE["x"], self.STATE['y'], event.x, event.y, width = 2, fill = self.color_map)

    def popupList(self, event):
        self.contextMenu.post(event.x_root, event.y_root)

    def clickMenu(self):
        self.class_name = self.Classes.get()
        self.color_map = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)]
        if self.flag == 0:
            self.listbox.insert(END, '(%d, %d) -> (%d, %d) -> %s' % (self.xx1, self.yy1, self.x2, self.y2, self.class_name))
        if self.flag == 1:
            num = len(self.bboxIdList)
            coor = self.bboxList[num - 1]
            self.listbox.insert(END, '(%d,%d)->(%d,%d)->(%d,%d)->(%d,%d)->%s' % (coor[0][0], coor[0][1], coor[1][0], coor[1][1],
                                coor[2][0], coor[2][1], coor[3][0], coor[3][1], self.class_name))
        self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = self.color_map)
        classIdx = self.mainPanel.create_text(self.x1+5, self.y1+8, text = self.class_name, anchor = W, fill = self.color_map)
        self.classes_name.append(self.class_name)
        self.classIdList.append(classIdx)

    def delete_line(self, event):
        if self.bboxId:
            try:
                if self.flag == 0:
                    self.mainPanel.delete(self.bboxId)
                    self.bboxId = None
                    self.STATE['click'] = 0
            except:
                pass
        else:
            try:
                if self.flag == 0:
                    if len(self.bboxIdList) != len(self.classes_name):
                        boxId = self.bboxIdList.pop()
                        self.mainPanel.delete(boxId)
                        self.bboxList.pop()
                if self.flag == 1:
                    if len(self.bboxIdList) != len(self.classes_name):
                        boxId = self.bboxIdList.pop()
                        self.bboxList.pop()
                        for Id in boxId:
                            self.mainPanel.delete(Id)
            except:
                pass

    def delBBox(self):
        try:
            sel = self.listbox.curselection()
            if len(sel) != 1 :
                return
            idx = int(sel[0])
            if self.flag == 0:
                self.mainPanel.delete(self.bboxIdList[idx])
            if self.flag == 1:
                for Id in self.bboxIdList[idx]:
                    self.mainPanel.delete(Id)
            self.mainPanel.delete(self.classIdList[idx])
            self.bboxIdList.pop(idx)
            self.classIdList.pop(idx)
            self.bboxList.pop(idx)
            self.classes_name.pop(idx)
            self.listbox.delete(idx)
        except:
            pass

    def clearBBox(self):
        try:
            for idx in range(len(self.bboxIdList)):
                if self.flag == 0:
                    self.mainPanel.delete(self.bboxIdList[idx])
                if self.flag == 1:
                    for Id in self.bboxIdList[idx]:
                        self.mainPanel.delete(Id)
                self.mainPanel.delete(self.classIdList[idx])
            self.listbox.delete(0, len(self.classes_name))
            self.bboxIdList = []
            self.classIdList = []
            self.bboxList = []
            self.classes_name = []
            self.coordinate = []
            self.bboxIdLine = []
        except:
            pass

    def Delete_image(self, event):
        image_path = self.imageList[self.cur-1]
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        else:
            self.messageList.insert(END, "Image NO. %d deleted" % self.cur)
            if len(self.messageList.get(0,END)) > 1:
                self.messageList.delete(1)
            messagebox.showinfo('Information','\tCompleted!\n\nAll images have been labelled!')
        os.remove(image_path)
        self.del_num += 1
        self.messageList.insert(END, "Image NO. %d deleted \t%d images have been deleted." %(self.cur-1, self.del_num))
        if len(self.messageList.get(0, END)) > 16:
            self.messageList.delete(1)

    def prevImage(self, event = None):
        try:
            self.saveImage()
            if self.cur > 1:
                self.cur -= 1
                self.loadImage()
            else:
                messagebox.showinfo('Information', "\t\n\nIt's already the first image.")
        except:
            pass

    def nextImage(self, event = None):
        try:
            self.saveImage()
            
        except:
            pass
     


def createElementNode(doc, tag, attr):
    element_node = doc.createElement(tag)
    text_node = doc.createTextNode(attr)
    element_node.appendChild(text_node)
    return element_node

def createChildNode(doc, tag, attr, parent_node):
    child_node = createElementNode(doc, tag, attr)
    parent_node.appendChild(child_node)

def createObjectNode(doc, classes_name, bbox, flag):
    object_node = doc.createElement('object')
    for i in range(len(classes_name)):
        class_name = classes_name[i]
        boxes = bbox[i]
        createChildNode(doc, 'name', class_name, object_node)
        createChildNode(doc, 'pose', _POSE, object_node)
        createChildNode(doc, 'truncated', _TRUNCATED, object_node)
        createChildNode(doc, 'difficult', _DIFFICULT, object_node)

        bndbox_node = doc.createElement('bndbox')
        if flag == 0:
            createChildNode(doc, 'xmin', str(boxes[0]), bndbox_node)
            createChildNode(doc, 'ymin', str(boxes[1]), bndbox_node)
            createChildNode(doc, 'xmax', str(boxes[2]), bndbox_node)
            createChildNode(doc, 'ymax', str(boxes[3]), bndbox_node)
        if flag == 1:
            createChildNode(doc, 'xlu', str(boxes[0][0]), bndbox_node)
            createChildNode(doc, 'ylu', str(boxes[0][1]), bndbox_node)
            createChildNode(doc, 'xru', str(boxes[1][0]), bndbox_node)
            createChildNode(doc, 'yru', str(boxes[1][1]), bndbox_node)
            createChildNode(doc, 'xrd', str(boxes[2][0]), bndbox_node)
            createChildNode(doc, 'yrd', str(boxes[2][1]), bndbox_node)
            createChildNode(doc, 'xld', str(boxes[3][0]), bndbox_node)
            createChildNode(doc, 'yld', str(boxes[3][1]), bndbox_node)

        object_node.appendChild(bndbox_node)
    return object_node

def writeXMLFile(doc, filename):
    tmpfile = open('tmp.xml', 'w')
    doc.writexml(tmpfile, addindent = ' '*4, newl = '\n', encoding = 'utf-8')
    tmpfile.close()

    fin = open('tmp.xml')
    fout = open(filename, 'w')
    lines = fin.readlines()

    for line in lines[1:]:
        if line.split():
            fout.writelines(line)
    fin.close()
    fout.close()
    os.remove('tmp.xml')

def createXML(image_name, shape, classes_name, bbox, flag):
    my_dom = xml.dom.getDOMImplementation()
    doc = my_dom.createDocument(None, 'annotation', None)

    root_node = doc.documentElement
    createChildNode(doc, 'folder', 'HUST2018', root_node)
    createChildNode(doc, 'filename', image_name, root_node)

    source_node = doc.createElement('source')
    createChildNode(doc, 'database', 'Detection', source_node)
    createChildNode(doc, 'annotation', 'HUST2018', source_node)
    createChildNode(doc, 'image', 'flickr', source_node)
    createChildNode(doc, 'flickrid', 'NULL', source_node)
    root_node.appendChild(source_node)

    owner_node = doc.createElement('owner')
    createChildNode(doc, 'flickr_url', '0', owner_node)
    createChildNode(doc, 'name', '?', owner_node)
    root_node.appendChild(owner_node)

    size_node = doc.createElement('size')
    createChildNode(doc, 'width', str(shape[0]), size_node)
    createChildNode(doc, 'height', str(shape[1]), size_node)
    createChildNode(doc, 'depth', str(shape[2]), size_node)
    root_node.appendChild(size_node)

    createChildNode(doc, 'segmented', _SEGMENTED, root_node)

    object_node = createObjectNode(doc, classes_name, bbox, flag)
    root_node.appendChild(object_node)
    return doc

def Help():
    space = "     "
    p = "\n\n" + space + "This is a simple tool for labelling object in image.\n"
    p1 = space + "The Label-Tool can label rectangle (two coordinates) and polygon (four coordinates), you can select mode.\n\n"
    p2 = space + "Usage:\n"
    p3 = space + space + "1. Select mode (rectangle or polygon). This is a radio, you can only choose one, and can't change mode during labelling.\n"
    p4 = space + space + "2. Select path that has '.jpg' file. If not '.jpg' format, you can run 'image.py' to generate and number images.\n"
    p5 = space + space + "3. Label:\n"
    p6 = "\tIf you choose 'rectangle', click the left mouse button, select the first point, then move the mouse, click the left button " \
         "again, select the second point, and then you can see the rectangle. And then click the right mouse button to select class name. " \
         "Finally, a bounding box is labelled.\n"
    p7 = "\nNOTE: If you draw rectangle wrong and class name has not been selected, you can click middle mouse button to delete rectangle. " \
         "If class name has been selected, you can click the bounding box that you want to delete in 'Bounding Box', then click 'Delete' " \
         "button. If you want to delete all bounding boxes, you can click 'ClearAll' button.\n\n"
    p8 = "\tIf you choose 'polygon', click the left mouse button four times to select four points, then you can see the polygon. And " \
         "then click the right mouse button to select class name.\n" \
         "\nNOTE: When you label polygon, you must click left-up, right-up, right-down, left-down of the polygon in order.\n\n"
    p9 = space + space + "4. If you label a image, click 'Next >>' button to next image, or you can press shortcut 's' or 'd' to next image. " \
                         "If you want to check previous image, you can click '<< Prev' button, or press shortcut 'w' or 'a'.\n"
    p10 = space + space + "5. If you think the image is not good, you can click 'Delete Image' button to delete image.\n"
    p11 = space + space + "6. Image's label is saved to '.xml' format, this is VOC format, you can easily use. Image's " \
                          "label is also saved to '.txt' format, this is used to check annotation.\n"
    p12 = "\nNOTE: Image shows on the canvas, the image is forced to zoom to the canvas size, so the image may be distorted, but " \
          "this is no problem, the coordinates of the annotation are restored to the original image size.\n"
    p13 = "\nNOTE: If you label your own data set, you need to modify 'CLASSES'.\n"
    p14 = "\nNOTE: If you find a bug in using, you can submit it in the issue."
    log = p + p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9 + p10 + p11 + p12 + p13 + p14
    messagebox.showinfo('Help', log)


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
        self.load_form_info()
        
        
    def load_image_and_setup_interface(self):
        try:
            self.image = Image.open(self.image_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.nom_image = os.path.basename(self.image_path)

            self.label = tk.Label(self.left_frame, image=self.photo)
            self.label.pack()

            self.text_entry_label = tk.Label(self.right_frame, text="Enter Text:")
            #self.text_entry_label.grid(row=0, column=0, columnspan=2, pady=10)

            self.text_entry = tk.Entry(self.right_frame)
            self.text_entry.insert(0, self.nom_image)
            #self.text_entry.grid(row=1, column=0, columnspan=2, pady=10)

            self.image_name_label = tk.Label(self.right_frame, text=f"Image Name: {os.path.basename(self.image_path)}")
            self.image_name_label.grid(row=2, column=0, columnspan=2, pady=10)

            self.line_count = tk.IntVar()
            self.count_text_file_lines()

        except Exception as e:
            print("Error loading image:", e)

    
    def load_form_info(self):
        # Load form information from the text file if available
        text_file_path = self.text_file_path or self.get_text_file_path()
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as file:
                form_info = file.read()
    
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, form_info)
    
            # Extract values for comboboxes and update them
            lines = form_info.split('\n')
            for i, line in enumerate(lines[1:]):
                values = line.split(':')
                if len(values) == 2:
                    self.combobox = self.combobox_list[i]  # Use the combobox from the list
                    if isinstance(self.combobox, ttk.Combobox):
                        self.combobox.set(values[1])

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





    def count_text_file_lines(self):
        text_file_path = self.text_file_path or self.get_text_file_path()
        line_count = count_text_file_lines(text_file_path)
        self.line_count.set(line_count)
        self.update_comboboxes(line_count)
        self.line_count_label = tk.Label(self.right_frame, text=f"Nombre de lignes: {line_count}")
        self.line_count_label.grid(row=line_count + 4, column=0, columnspan=2, pady=10)

    def get_text_file_path(self):
        image_directory, image_filename = os.path.split(self.image_path)
        text_filename = os.path.splitext(image_filename)[0] + ".png.txt"
        text_file = r"./rectangles_folder"  # Remplacez 'chemin_vers_votre_dossier' par le chemin réel
        text_file_path = os.path.join(text_file, text_filename)  # Replace this with the text files directory
        return text_file_path

    def update_comboboxes(self, line_count):
        for widget in self.right_frame.winfo_children():
            widget.grid_forget()

        self.text_entry_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.text_entry.grid(row=1, column=0, columnspan=2, pady=10)

        self.combo_values = ["Option 1", "Option 2", "Option 3", "Option 4"]

        for i in range(line_count):
            self.combobox_label = tk.Label(self.right_frame, text=f"Defect {i + 1}:")
            self.combobox_label.grid(row=i + 2, column=0, pady=10)

            combobox = ttk.Combobox(self.right_frame, values=self.combo_values)
            combobox.grid(row=i + 2, column=1, pady=10)
            self.combobox_list.append(combobox)  # Store the combobox reference in the list

        self.save_button = tk.Button(self.right_frame, text="Enregistrer", command=self.save_image)
        self.save_button.grid(row=line_count + 2, column=0, columnspan=2, pady=10)

        self.count_lines_button = tk.Button(self.right_frame, text="Compter les lignes", command=self.count_text_file_lines)
        self.count_lines_button.grid(row=line_count + 3, column=0, columnspan=2, pady=10)
    
    def extract_values(self):
        new_values = []

        # Extract the new text from the text_entry widget
        new_text = self.text_entry.get()

        # Loop through the comboboxes and get their values
        for i in range(self.line_count.get()):
            defect_number = i + 1
            combobox = self.combobox_list[i]
            value = combobox.get()
            new_values.append(f"Defect {defect_number}:{value}")

        # Combine the new text and the combobox values
        combined_values = '\n'.join(new_values)
        result = f"{new_text}\n{combined_values}"

        return result

  
    
    
    def save_image(self):
        updated_values = self.extract_values()
        # Save the updated values into a new text file
        output_folder = r"./result"  # Change this to your desired output folder
        new_text_filename = os.path.splitext(os.path.basename(self.image_path))[0] + "_updated.txt"
        new_text_file_path = os.path.join(output_folder, new_text_filename)

        with open(new_text_file_path, 'w') as file:
            file.write(updated_values)

        print(f"Updated values saved to: {new_text_file_path}")
        
        new_image_filename = os.path.basename(self.image_path)
        new_image_path = os.path.join(output_folder, new_image_filename)
        shutil.copyfile(self.image_path, new_image_path)
        print(f"Image copied to: {new_image_path}")


class Defects(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        self.Camera=Camera.get_instance()
        

        
        #self.detector = Backend_defect()
        #self.predictor = Backend_defect().initialize_predictor()  # Initialize the predictor only once
        #self.detector = Backend_defect(predictor=self.predictor)
        
        

        #detector = Backend_defect()
        
        #detector.capture_frame_and_save()
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
        self.cap = None
        self.photo = None

        self.image_path=None
        self.data={'poi': '____', 'client': '____ ', 'saison':'____','model':' ____-', 'lavage': '_____', 'tissu': '_____ ', 'elasticite':'______' , 'idPiece':'_____' , 'etape': '____'}


        
        self.main_frame = Frame(self)
        
        self.main_frame.pack(fill=BOTH, expand=1)

        self.main_canvas = tk.Canvas(self.main_frame, bg="#212121", highlightthickness=0)
        self.main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        

        # Add A Scrollbar To The main_canvas
        self.my_scrollbar = tk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.main_canvas.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Create ANOTHER Frame INSIDE the self.main_canvas
        self.second_frame = customtkinter.CTkFrame(self.main_canvas)
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
        self.frame1 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="red")
        self.frame1.grid(row=0,column=3,padx=(150, 150), pady=(60, 20), sticky="n")
        row = 0
        col = 0
        for key, value in self.data.items():
            # Create labels
            label = customtkinter.CTkLabel(self.frame1, text=key, font=customtkinter.CTkFont(size=12),
                                           text_color="#4D2700")
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
        self.measure_frame1 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="black")
        self.measure_frame1.grid(row=2,column=0, sticky="we",columnspan=6,padx=(20, 0), pady=(20, 20))
        self.measure_frame1.grid_rowconfigure(11, weight=2)
        
        
        self.measure_frame = customtkinter.CTkFrame(self.measure_frame1, width=450, height=100, corner_radius=0)
        self.measure_frame.grid(row=0, column=0, rowspan=6,columnspan=1, padx=(5, 0), pady=(20, 0), sticky="nsw")
        
        
        
        # create the camera canvas
        self.canvas = customtkinter.CTkCanvas(self.measure_frame1,background='#212121',highlightthickness=0,height=500,width=950)
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
        slider = tk.StringVar()
        slider.set('1.00')
       
        self.scale_widget = tk.Scale(self.sidebar_frame, from_=1.0, to=13.00,resolution=0.01,length=300, command=lambda s:slider.set('%0.2f' % float(s)),orient=tk.HORIZONTAL)
        self.scale_widget.set(self.Camera.get_gain())
        self.scale_widget.grid(row=9, column=0, padx=20, pady=(10, 0))
        
        
        self.scale_widget_exp = tk.Scale(self.sidebar_frame, from_=62.666666666666664, to=977178.9166666666,resolution=10,length=300, command=lambda s:slider.set('%0.2f' % float(s)),orient=tk.HORIZONTAL)
        self.scale_widget_exp.set(self.Camera.get_exposure_time())
        self.scale_widget_exp.grid(row=10, column=0, padx=20, pady=(10, 0))
    

       


        # create the output canvas
        #self.canvas2 = customtkinter.CTkCanvas(self.second_frame, background='#474747', highlightthickness=0)
        #self.canvas2.grid(row=1, column=1, padx=(10, 0), pady=(20, 0), sticky="nsew")

        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        # Get the dimensions of the canvas and the image
        #canvas_width = self.canvas2.winfo_width()
        #canvas_height = self.canvas2.winfo_height()
        #image_width = photo.width()
        #image_height = photo.height()

        # Calculate the coordinates for the top-left corner of the image to center it
        #x = (canvas_width - image_width) // 2
        #y = (canvas_height - image_height) // 2

        #self.canvas2.create_image(-x, -y, image=photo, anchor="nw")
        #self.canvas2.image = photo

        #qr code input at the bottom
        
        # create sidebar frame on the left with widgets
        self.measure_frame2 = customtkinter.CTkFrame(self.second_frame, corner_radius=0,fg_color="red",height=600)
        self.measure_frame2.grid(row=3,column=0, sticky="we",columnspan=2,padx=(20, 0), pady=(20, 20))
        self.qr_code = customtkinter.CTkEntry(self.measure_frame2, placeholder_text="This doesnt do anything yet")
        self.qr_code.grid(row=1, column=1, rowspan=6, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(self.measure_frame2,text="enter QR code", fg_color="transparent", border_width=2,command=self.up_client)
        self.main_button_1.grid(row=1, column=5, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
       
       
        
        
        
     
     

       # Ajouter un label pour afficher "Le mesure est :"
  
        
       
        self.scrollable_frame_switches1 = []
        self.on_image = Image.open(r"./pages/on.png")
        self.on_image =  self.on_image.resize((150, 50), Image.ANTIALIAS)  # Adjust the size as needed
        self.on_image = ImageTk.PhotoImage( self.on_image)
        
        self.off_image = Image.open(r"./pages/off.png")
        self.off_image =  self.off_image.resize((150,50), Image.ANTIALIAS)  # Adjust the size as needed
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
        
        
      
        self.product_dict = {"centure":0.0,"motant_devant":0.0,"entre jambe":0.0 ,"longu_measure":0.0,"cuise_m_1":0.0,"leg_opening":0.0}



        


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

        self.canvas.bind("<Button-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.end_selection)
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
        self.progressbar = customtkinter.CTkProgressBar(self.second_frame,determinate_speed=5,indeterminate_speed=2,mode="determinate",height=50,width=750,corner_radius=30,border_width=10,fg_color="black",progress_color="#F8FC7F",border_color="black")
        self.progressbar.grid(row=2, column=2,columnspan=2, pady=(0, 0),padx=(0,250 ))
        self.progressbar.set(0)
        progres=1/25
        stepval=0 
        for i in range(25):
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
            self.p = threading.Thread(target=self.start)
            self.d = threading.Thread(target=self.run_detection)
            
            self.d.start()
            self.p.run()
            t2=time.time()
            print("run_all",t2-t1)

            #self.process_image()
            self.progressbar.grid_forget()
            
            self.frame=cv2.imread("res.png")
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
        img = img.resize((new_width, new_height), Image.ANTIALIAS)

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

        return img.resize((new_width, new_height), Image.ANTIALIAS)
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
        self.mesur=Backend_mesure()
        self.predictor_m= Backend_mesure().initialize_predictor()
        self.mesur = Backend_mesure(predictor=self.predictor_m)
       
        t1=time.time()
        image = self.frame
        print(image)
        self.code_piece=self.qr_code.get()
        self.product_dict=self.mesur.detection_m(self.code_piece,image)
        print("self.product_dict",self.product_dict)
        self.display_results_in_table(self.product_dict)
        #self.detector.process_image(image)
        #self.frame=self.detector.process_image(image)
        t2=time.time()
        print("mesure&def____",t2-t1)

        
    def generer(self):
        self.mesur.send_data_and_display_pdf()

       


        



        

            
            



 
    def delete_image(self, image_path):
        cropped_images_dir = r"./cropped_zones"
        try:
            if os.path.exists(image_path):
                
                os.remove(image_path)
                self.draw_bounding_boxes()  # Refresh display after deleting image
            else:
                print("File not found:", image_path)
        except Exception as e:
            print("Error deleting image:", str(e))



    def on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        




    # Start the camera when this page is shown
    def scale_value_changed(self,scale_widget):
        scale_widget=scale_widget
        # This function will be called when the scale value changes
        scale_value = scale_widget.get()
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
        self.scale_value_exp=self.scale_value_changed(self.scale_widget_exp)
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas)
        #resize_canvas(self.sidebar_frame, self.scrollable_frame1, self, self.canvas2)
        #print("s",self.scale_value)
        self.Camera.set_gain(self.scale_value)
        self.Camera.get_exposure_time()
        self.Camera.set_exposure_time(self.scale_value_exp)
       
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
    
  
          
            # Convert the OpenCV image to a PIL image
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2image))
  
            # Display the camera footage on the self.canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
  
            # Schedule the next update in 10 milliseconds
            self.after(600, self.update)
        except Exception as e:
            print( "Exception_def1", str(e))

    



 




    # Stop the camera and show the index page
    def go_(self):
        self.controller.show_frame("Index")
        
    def open_image(self, path):
        # Check if the file exists before opening the image viewer
        if os.path.exists(path):
            # Create an instance of the image viewer and pass the image path to it
            viewer = ImageViewer(path)
            viewer.mainloop()
        else:
            print(f"Error: File not found at path {path}")
           
    def open_res_th(self): 
        defect_window = ImageViewer_lable(self)

        
    def labl(self,path):
        viewer1 = LabelTool(path)

        viewer1.mainloop()
   
    
    def start_selection(self, event):
        self.selection_start = (event.x, event.y)
        if self.selection_rectangle:
            self.canvas.delete(self.selection_rectangle)
        self.selection_rectangle = None  # Clear the previous rectangle

    def update_selection(self, event):
        x, y = self.selection_start
        if self.selection_rectangle:
            self.canvas.delete(self.selection_rectangle)
        self.selection_rectangle = self.canvas.create_rectangle(x, y, event.x, event.y, outline="red")

    def end_selection(self, event):
        x1, y1 = self.selection_start
        x2, y2 = event.x, event.y
        if self.selection_rectangle:
            self.canvas.delete(self.selection_rectangle)

        selected_image = self.crop_image(y1, y2, x1, x2)
        current_datetime = datetime.datetime.now()
        date_string = current_datetime.strftime("%Y-%m-%d_%H-%M-%S-%f")
        # Génération d'un nom de fichier unique
        image_name =f"image_{date_string}.png"
        
        
        # Chemin complet pour enregistrer l'image
        self.image_path_def = os.path.join(r"./cropped_zones", image_name)
        
        cv2.imwrite(self.image_path_def, selected_image)
        self.labl(path=self.image_path_def)
        #self.monitor_images()
        self.draw_bounding_boxes()
    
   


    def crop_image(self, y1, y2, x1, x2):
        x1=x1
        x2=x2
        y1=y1
        y2=y2
        frame=cv2.resize(self.frame, (self.canvas.winfo_width(),self.canvas.winfo_height()))
        pil_image = frame
        cropped_image = pil_image[y1:y2, x1:x2]
        
        return cropped_image
    
    

    # Adjust the sleep interval based on your requirements
    #
            
    


        
        
        
        
    def img_service(self):
        dossier_photos = r"././cropped_zones"
        url = "http://192.168.0.70/WebServices/rooting/Rework/addPieceIA"
        i=0
        for filename in os.listdir(dossier_photos):
            if filename.endswith(".png"):  # Assurez-vous que les fichiers sont des images PNG
                chemin_image = os.path.join(dossier_photos, filename)
    
                # Lisez l'image sous forme de bytes et encodez-la en base64
                with open(chemin_image, "rb") as image_file:
                    image_bytes = image_file.read()
                    b64_string = base64.b64encode(image_bytes).decode('utf-8')
    
                # Construisez la payload pour la requête POST
                payload = {
                    "CPiece": 14,
                    "listDef": [
                        {
                            "image": b64_string,
                            "idDef": "13"
                        }
                    ]
                }
    
                # Effectuez la requête POST
                headers = {}
    
                response = requests.post(url, headers=headers, json=payload)
                i=i+1
    
                # Traitez la réponse
                if response.status_code == 201:
                    print(f"Image {filename} envoyée avec succès.")
                    # Affichez la réponse JSON
                    print("Réponse JSON du service web :")
                    print(payload)

                else:
                    print(f"Échec de l'envoi de l'image {filename}. Code d'état : {response.status_code}") 
                    print("_____________________________________________",payload)
        print("End")
        print(i)


