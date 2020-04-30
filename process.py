import cv2
import os
import numpy
#from PIL import Image,ImageTk
import Tkinter
import time
class process:
    def __init__(self,gui=None):
        self.gui = gui
        
    def crop(self,p=None,q=None):
        print 1
        if(p==None):
            p = os.listdir(".\\database\\")
        elif(type(p)!=list):
            p = [p]
        if q:
            if(type(q)!=list):
                q = [str(q)+".jpg"]
            else:
                q = [str(b)+".jpg" for b in q]
                
        self.missing = []
        for i in p:
            if q == None:
                q1 = os.listdir(".\\database\\"+str(i)+"\\")
            else:
                q1 = q
            for j in q1:
                f = 0
                lt = 0
                rt = 0
                if j == "crop":
                    continue
                txt = "cropping "+ str(j) 
                self.gui.Message.config(text = txt)
                self.gui.masnew.update()
                self.img = cv2.imread(".\\database\\"+str(i)+"\\"+str(j),cv2.CV_LOAD_IMAGE_GRAYSCALE)
                try:
                    if (self.img==None):
                        if self.gui:
                            self.gui.Message.config(text = ".\\database\\"+str(i)+"\\"+str(j)+" Not Found")
                            self.gui.masnew.update()
                            time.sleep(2)
                            continue
                except:
                    pass
                try:
                    self.img = cv2.resize(self.img,(400,400))
                except Exception as sr:
                    self.gui.Message.config(text = sr)
                    continue
                cv2.imshow("img",self.img)
                cv2.waitKey(5000)
##                if (self.img != None):
                if (True):
                    row,col = self.img.shape
                    lt = col-1
                    for r in range(0,row-2):
                        for c in range(0,col-1):
                            if((self.img[r][c]>60) and (self.img[r+1][c]>60) ):
                                f = 1
                                b = r
                                if(c<lt):
                                    lt = c
                                if(c>rt):
                                    rt = c
                            if(f==0):
                                t = r
                    
                    try:
                        self.img = self.img[t:b,lt:rt]
                    except UnboundLocalError:
                        pass
                    try:
                        self.img = cv2.resize(self.img,(60,80))
                    except Exception as sr:
                        self.gui.Message.config(text = sr)
                        self.gui.masnew.update()
                        continue
                    try:
                        os.mkdir(".\\Database\\"+str(i)+"\\crop")
                    except:
                        pass
                    cv2.imwrite(".\\database\\"+str(i)+"\\crop\\"+str(j),self.img)
                    if False:
                        self.temp = Image.open(".\\database\\"+str(i)+"\\crop\\"+str(j))
                        self.t = ImageTk.PhotoImage(self.temp)
                        self.gui.image = Tkinter.Frame(self.gui.mas,width=150,height=150)
                        self.gui.image.pack_propagate(0)
                        self.gui.image.place(x=500,y=130)
                        self.gui.im = Tkinter.Label(self.gui.image,image = self.t,width=100,height=150)
                        self.gui.im.pack(side = "top")
                        self.gui.Message.config(text = str(i)+" - " + str(j[0:j.index(".jpg")]) + " Cropped")
                        self.gui.masnew.update()
                    else:
##                        cv2.destroyAllWindows()
##                        cv2.imshow("das",self.img)
##                        cv2.waitKey(3)
                        pass
                    
                    
                else:
                    self.missing.append([str(i),str(j)])
        
if __name__ == "__main__":
    a = process()
    a.crop()
    cv2.destroyAllWindows()
                            
                    
        
