import sys, thread, time
sys.path.insert(0,"D:\Leap\lib")
#from PIL import Image,ImageTk
import Tkinter
from time import sleep
import numpy as np
global count
import cv2
import time
import os


                
class lep:

    def run(self,a=None,label=None,c = None):
        if a == None:
            a = range(0,10)
        if type(a)!= list:
            a = [a]
        if label == None: 
            label = range(1,11)
        if type(label)!= list:
            label = [label]
        
        
        for i in a:
            try:
                os.mkdir(".\\database\\"+str(i))
            except :
                pass
        for j in a:
            if self.gui != None:
                self.gui.Message.config(text = "DATABASE FOR "+str(j))
                self.gui.masnew.update()
            for i in label:
                self.main(j,i,c)
            if self.gui != None:
                self.gui.Message.config(text = "DATABASE UPDATED FOR "+str(j))
                self.gui.masnew.update()

                
    def __init__(self,gui=None):
        self.gui = gui
        self.cap = cv2.VideoCapture(0)

    
    def main(self,a,i,c = None):
        # Create a sample listener and controller
        try:
            os.remove("captured.jpg")
        except:
            pass
        while True:
            
            ret,img = self.cap.read()
            img2 = img.copy()
            cv2.rectangle(img2,(180,96),(550,336),(0,255,0),0)
            cv2.imshow("frame",img2)
            cv2.moveWindow("frame",0,0)
            if cv2.waitKey(1)&0xff == ord('q'):
                break
##        cv2.imwrite("test.jpg",img)
##        img = cv2.imread("test.jpg")
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY) #covertion of colour imaag to grey   
        cv2.imshow("gray",gray)  
        crop=gray[96:336,180:550]
##        blackimg = np.zeros([500,600],np.uint8)
##        blackimg[96:336,180:550]= crop.copy()
        blackimg = crop.copy()
##        gaus = cv2.equalizeHist(blackimg)
##        gaus = cv2.GaussianBlur(blackimg,(15,15),0)
        gaus = cv2.createCLAHE(clipLimit = 15.0,tileGridSize = (10,10))
        gaus = gaus.apply(blackimg)
        gaus = cv2.GaussianBlur(gaus,(5,5),0)
        gaus = cv2.medianBlur(gaus,5)
##
##        kernal = np.ones((5,5),np.uint8)
##        close = cv2.morphologyEx(gaus,cv2.MORPH_CLOSE,kernal)
##        dff =cv2.absdiff(blackimg,close)
        k,dff = cv2.threshold(gaus,100,255,cv2.THRESH_BINARY_INV)
        
        
##        kernal = np.ones((5,5),np.uint8)
##        dff2 = cv2.dilate(dff,kernal,1)
##        dff2 = cv2.resize(dff2,(50,50))
##        dff2 = cv2.resize(dff2,(200,200))
##        dff2 = cv2.resize(dff2,(50,50))
##        dff2 = cv2.resize(dff2,(200,200))
##        dff2 = cv2.resize(dff2,(50,50))
##        dff2 = cv2.resize(dff2,(200,200))
##        dff2 = cv2.resize(dff2,(50,50))
##        dff2 = cv2.resize(dff2,(200,200))
##        k,dff2 = cv2.threshold(dff2,30,255,cv2.THRESH_BINARY)
##        kernal = np.ones((1,15),np.uint8)
##        kernal = np.ones((12,5),np.uint8)
####        dff2 = cv2.dilate(dff2,kernal,1)
##        dff = cv2.medianBlur(dff,1)

        
        ##        dff2 = cv2.dilate(dff2,kernal,4)
##        while cv2.waitKey(1)&0xff != ord('q'):
##            cv2.imshow("frame1",dff)
####            cv2.imshow("frame",gaus)
####            cv2.imshow("frame2",crop)
##        cv2.destroyAllWindows()
####
##        medImg = cv2.cv.CreateImage(cv2.cv.GetSize(blackImg),8,1)
##        cv2.cv.Smooth(blackImg,medImg,cv2.cv.CV_GAUSSIAN,5,5,0,0) #appling gussian 
##        cv2.cv.SaveImage('aftersmoothing.jpg',medImg)
##        sE=cv2.cv.CreateStructuringElementEx(3,3,1,1,cv2.cv.CV_SHAPE_ELLIPSE)
##        bkgImg=cv2.cv.CreateImage(cv2.cv.GetSize(blackImg),8,1)
##        temp=cv2.cv.CreateImage(cv2.cv.GetSize(blackImg),8,1)
##        cv2.cv.MorphologyEx(medImg,bkgImg,temp,sE,cv2.cv.CV_MOP_CLOSE,8)  #enchancingg vein pattern
##        cv2.cv.SaveImage('aftermorphology.jpg',bkgImg)
##        normed=cv2.cv.CreateImage(cv2.cv.GetSize(medImg),8,1)
##        cv2.cv.AbsDiff(bkgImg,medImg,normed)     
##        cv2.cv.SaveImage('afternormalising.jpg',normed)
##        ##
##        thresh = cv2.cv.CreateImage(cv2.cv.GetSize(blackImg),8, 1); 
##        cv2.cv.Threshold(normed,thresh,1,255,cv2.cv.CV_THRESH_BINARY);   #binary imggg
##        cv2.cv.SaveImage('afterthresholding.jpg',thresh);
##        ##
##        medthresh = cv2.cv.CreateImage(cv2.cv.GetSize(blackImg),8,1); 
##        cv2.cv.Smooth(thresh, medthresh, cv2.cv.CV_MEDIAN, 11, 11,0,0); 
##        cv2.cv.NamedWindow("Captured Vein Pattern",cv2.cv.CV_WINDOW_AUTOSIZE);
##        cv2.cv.SaveImage("/home/pi/Desktop/veinpatten/database/"+str(a)+"/"+str(i)+".jpg",medthresh);

        
        
        ##cv2.cv.SaveImage(testimage)
        if False:
            if self.gui.enlargevar.get()==1:
                cv2.cv.ShowImage("1Captured Vein Pattern3",dff); 
                k=cv2.cv.WaitKey(2000);
                cv2.destroyAllWindows()
        else:
            cv2.imshow("myimage",dff)            
            cv2.waitKey(0)
            cv2.destroyAllWindows()

##        cv2.cv.SaveImage("/home/pi/Desktop/veinpatten/database/"+str(a)+"/"+str(i)+".jpg",medthresh);
        cv2.imwrite(".\\database\\"+str(a)+"/"+str(i)+".jpg",dff,)
        cv2.destroyAllWindows()
        if False:
            self.temp = Image.open(".\\database\\"+str(a)+"/"+str(i)+".jpg")
            self.temp = self.temp.resize((150,150),Image.ANTIALIAS)
            self.t = ImageTk.PhotoImage(self.temp)
            self.gui.image = Tkinter.Frame(self.gui.masnew,width=150,height=150)
            self.gui.image.pack_propagate(0)
            self.gui.image.place(x=500,y=130)
            self.gui.im = Tkinter.Label(self.gui.image,image = self.t,width=100,height=150)
            self.gui.im.pack(side = "top")
            self.gui.masnew.update()
            
##            else:
##                cv2.waitKey(3)
##                cv2.destroyAllWindows()
        
                


if __name__ == "__main__":
    a = lep()
    #a.run("a","a")
    a.main("zain",1)
