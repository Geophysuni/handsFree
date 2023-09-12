# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 15:39:26 2023

@author: Sergey Zhuravlev
"""


import cv2 as cv
import matplotlib.pyplot as plt
from tkinter import *
from  tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pickle
from tkinter import filedialog as fd
from matplotlib.backend_bases import MouseButton
import imageio as iio
import numpy as np
import time
from PIL import Image, ImageTk
import pandas as pd
from matplotlib.backend_bases import key_press_handler
import time
import pyperclip
from tracker import track

class mainWin:
    def __init__(self):

        self.mainWin = Tk()
        
        self.mainWin.geometry('1920x1200')
        self.mainWin.title('Hands Free')
        
        self.text = Text(master = self.mainWin, width = 160, height = 20, font=("Helvetica", 32))
        
        self.canvasMini = Canvas(master = self.mainWin, width=1500, height=500)
        self.keyboard = cv.resize(iio.imread('KB_Russian.png'), (1500,500), interpolation = cv.INTER_AREA)
        
        self.photoMini = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(self.keyboard, cv.COLOR_BGR2RGB)))
        self.canvasMini.create_image(0, 0, image=self.photoMini, anchor=NW)
        
        self.text.place(x = 10, y = 10)
        self.canvasMini.place(x = 10, y = 360)
        
        self.smGlasses = []
        self.сrdList = [(int(750), int(300))]
        
        
        self.keys = []
        self.curCase = []
        
        self.delay = {}
        self.delay['key'] = ''
        self.delay['time'] = time.time()
        
        self.funDelay = {}
        self.funDelay['f'] = ''
        self.delay['time'] = time.time()
        
        self.cap = cv.VideoCapture(0)
        self.canvasTsh = Canvas(master = self.mainWin, width=250, height=170)
        
        self.crdList = [(750, 500)]
        self.trSlider = Scale(master = self.mainWin, from_=100, to=255, tickinterval=20, orient=HORIZONTAL, length=250)
        self.trSlider.set(23)
        self.trSlider.place(x=1300, y = 180)
        
        self.resetBut = Button(master = self.mainWin, text = 'Reset', width = 35, height = 5)
        
        # first line
        dx = 1500/14
        dy = 500/7
        for il, l in enumerate(['й','ц','у','к','е','н','г','ш','щ','з','х','ъ']):
            tmp = {}
            tmp['key'] = l
            tmp['x1'] = il*dx
            tmp['x2'] = (il+1)*dx
            tmp['y1'] = 0
            tmp['y2'] = dy
            self.keys.append(tmp)
        
        for il, l in enumerate(['ф','ы','в','а','п','р','о','л','д','ж','э', '?']):
            tmp = {}
            tmp['key'] = l
            tmp['x1'] = il*dx
            tmp['x2'] = (il+1)*dx
            tmp['y1'] = dy
            tmp['y2'] = 2*dy
            self.keys.append(tmp)
            
        for il, l in enumerate(['я','ч','с','м','и','т','ь','б','ю',',','.','!']):
            tmp = {}
            tmp['key'] = l
            tmp['x1'] = il*dx
            tmp['x2'] = (il+1)*dx
            tmp['y1'] = 2*dy
            tmp['y2'] = 3*dy
            self.keys.append(tmp)
        
        # space
        tmp = {}
        tmp['key'] = ' '
        tmp['x1'] = 0
        tmp['x2'] = 4*dx
        tmp['y1'] = 3*dy
        tmp['y2'] = 4*dy
        self.keys.append(tmp)
        
        # functionKey
        
        # curLeft
        tmp = {}
        tmp['key'] = 'left'
        tmp['x1'] = 12*dx
        tmp['x2'] = 13*dx
        tmp['y1'] = 0
        tmp['y2'] = dy
        self.keys.append(tmp)
        
        # curRight
        tmp = {}
        tmp['key'] = 'right'
        tmp['x1'] = 13*dx
        tmp['x2'] = 14*dx
        tmp['y1'] = 0
        tmp['y2'] = dy
        self.keys.append(tmp)
        
        # del symbol
        tmp = {}
        tmp['key'] = 'delSymb'
        tmp['x1'] = 12*dx
        tmp['x2'] = 14*dx
        tmp['y1'] = dy
        tmp['y2'] = 2*dy
        self.keys.append(tmp)
        
        # del word
        tmp = {}
        tmp['key'] = 'delWord'
        tmp['x1'] = 12*dx
        tmp['x2'] = 14*dx
        tmp['y1'] = 2*dy
        tmp['y2'] = 3*dy
        self.keys.append(tmp)
        
        # clear all
        tmp = {}
        tmp['key'] = 'clearAll'
        tmp['x1'] = 4*dx
        tmp['x2'] = 9*dx
        tmp['y1'] = 3*dy
        tmp['y2'] = 4*dy
        self.keys.append(tmp)
        
        # copy all
        tmp = {}
        tmp['key'] = 'copy'
        tmp['x1'] = 9*dx
        tmp['x2'] = 14*dx
        tmp['y1'] = 3*dy
        tmp['y2'] = 4*dy
        self.keys.append(tmp)
        
        
        # functions
        
        
                            
        # def captureVideo(event):
        #     self.vid = cv.VideoCapture(0)
        #     self.update()
                                          
        def reset(event):
            self.crdList = [(int(750), int(300))]
            # self.smGlasses = []
        # bind
        # self.canvasMini.bind('<ButtonRelease-1>',getCrd)
        # self.canvasMini.bind("<Motion>", getCrd)
        self.resetBut.bind('<ButtonRelease-1>', reset)
        # placing
        # self.faceArea.place(x = 1300, y = 30)
        self.canvasTsh.place(x = 1300, y = 10)
        self.resetBut.place(x = 1300, y = 250)
        
    def getCrd(self, xc, yc):
        # self.update()
        # xc = event.x
        # yc = event.y
        # print(str(xc)+'/'+str(yc))
        for key in self.keys:
            # time.sleep(1)
            # print(key['key'])
            if key['x1']<xc<key['x2']:
                if key['y1']<yc<key['y2']:
                    # если задержка больше секунды и буква не поменялась, печатаем букву и обновляем счетчик
                    if self.delay['key']==key['key'] and abs(self.delay['time']-time.time())>2:
                        if key['key'] not in ['left', 'right', 'delSymb', 'delWord', 'clearAll', 'copy']:
                            l,c = int(str(self.text.index(INSERT)).split('.')[0]), int(str(self.text.index(INSERT)).split('.')[1])
                            txt = self.text.get('1.0', END)
                            start = txt[:c]
                            fin = txt[c:].replace('\n','')
                            self.text.delete('1.0', END)
                            self.text.insert(END, start+key['key']+fin)
                            self.delay['key']=key['key']
                            self.delay['time']=time.time()
                        if key['key'] == 'left':
                            l,c = int(str(self.text.index(INSERT)).split('.')[0]), int(str(self.text.index(INSERT)).split('.')[1])
                            self.text.mark_set("insert", "%d.%d" % (l, c-1))
                            self.delay['key']=key['key']
                            self.delay['time']=time.time()
                        if key['key'] == 'right':
                            l,c = int(str(self.text.index(INSERT)).split('.')[0]), int(str(self.text.index(INSERT)).split('.')[1])
                            self.text.mark_set("insert", "%d.%d" % (l, c+1))
                            self.delay['key']=key['key']
                            self.delay['time']=time.time()
                        if key['key'] == 'delSymb':
                            l,c = int(str(self.text.index(INSERT)).split('.')[0]), int(str(self.text.index(INSERT)).split('.')[1])
                            txt = self.text.get('1.0', END)
                            start = txt[0:c-1]
                            fin = txt[c:].replace('\n', '')
                            self.text.delete('1.0', END)
                            self.text.insert('1.0', start)
                            self.text.insert(END, fin)
                            self.delay['key']=key['key']
                            self.delay['time']=time.time()
                        if key['key'] == 'delWord':
                            l,c = int(str(self.text.index(INSERT)).split('.')[0]), int(str(self.text.index(INSERT)).split('.')[1])
                            txt = self.text.get('1.0', END).replace('\n', '')
                            start = ''
                            for i in range(c-1,-1,-1):
                                if txt[i]==' ':
                                    start = txt[:i]
                                    print(start)
                                    break
                            
                            fin = ''
                            try:
                                for i in range(c+1,len(txt)):
                                    if txt[i]==' ':
                                        fin = txt[i:]
                                        print(fin)
                                        break
                            except:
                                bonk = 1
                            
                            self.text.delete('1.0', END)
                            self.text.insert('1.0', start)
                            self.text.insert(END, fin)
                    
                            
                            self.delay['key']=key['key']
                            self.delay['time']=time.time()
                            
                        if key['key'] == 'clearAll':
                            self.text.delete('1.0', END)
                            self.delay['key']=key['key']
                            self.delay['time']=time.time()
                        if key['key'] == 'copy':
                            print('copy')
                            pyperclip.copy(self.text.get('1.0', END))
                            self.delay['key']=key['key']
                            self.delay['time']=time.time()
                    # если видим новую букву обнуляем счетчик и задаем новую букву
                    if self.delay['key']!=key['key']:
                        self.delay['key']=key['key']
                        self.delay['time']=time.time()
    def update(self):
        # track(1)
        
        
        try:
            ret, frame = self.cap.read()
            frame, keyboard, self.crdList = track(frame, self.keyboard, self.crdList, int(self.trSlider.get()))
            
            if len(self.crdList)>2:
                self.getCrd(self.crdList[2][0] , self.crdList[2][1])
            # except:
            #     bonk = 1
            frame = cv.resize(frame, (250,170), interpolation = cv.INTER_AREA)
            # plt.imshow(frame)
            
            if ret:
                try:
                    self.photoTsh = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB)))
                    self.canvasTsh.create_image(0, 0, image=self.photoTsh, anchor=NW)
                    
                    # self.keyboard = cv.resize(iio.imread('KB_Russian.png'), (1500,500), interpolation = cv.INTER_AREA)
                    
                    self.photoMini = ImageTk.PhotoImage(image=Image.fromarray(cv.cvtColor(keyboard, cv.COLOR_BGR2RGB)))
                    self.canvasMini.create_image(0, 0, image=self.photoMini, anchor=NW)
                except:
                    bonk = 1
            self.mainWin.after(1, self.update)
        except:
            bonk = 1
        # self.mainWin.after(1, self.update)              
                
    def run(self):
        self.mainWin.after(1, self.update)
        self.mainWin.mainloop()

mwin = mainWin()
mwin.run()   