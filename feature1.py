import cv2
import cv2.cv as cv
import numpy as np
import os
import time
import scipy.io as mat
from program import *

class feature1:
    def __init__(self,gui = None):
        self.gui = gui
        pass
    
    def dctim(self,imge):
        B=4 #blocksize
        fn3= imge
        img1 = cv2.imread(fn3, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        h,w=np.array(img1.shape[:2])/B * B
        img1=img1[:h,:w]
        blocksV=h/B
        blocksH=w/B
        vis0 = np.zeros((h,w), np.float32)
        Trans = np.zeros((h,w), np.float32)
    
        
        vis0[:h, :w] = img1
        for row in range(blocksV):
            for col in range(blocksH):
                currentblock = cv2.dct(vis0[row*B:(row+1)*B,col*B:(col+1)*B])
                Trans[row*B:(row+1)*B,col*B:(col+1)*B]=currentblock
        return Trans
    
    def extract(self):
        dctvariable1=np.zeros((1,500),np.float32)
        train=np.zeros((1,1),np.float32)
        name = []
        fl = -1
        t1 = -1
        for fold in os.listdir(".\\database\\"):
            try:
                if fold == "test" or fold == "word":
                    continue
                name.append(fold)
                t1 = t1 + 1
                for fil in os.listdir(".\\database\\"+fold+"/crop/"):
                    try:
                        a = self.dctim(".\\database\\"+str(fold)+"/crop/"+str(fil))
                        img=np.asarray(a)
                        fl = fl + 1
                        if fl>0:
                            dctvariable1 = np.append(dctvariable1,np.zeros((1,500),np.float32),axis=0)
                            train = np.append(train,np.zeros((1,1),np.float32),axis=0)
                        image_no = fl
                        k=0
                        for i in range(10):        
                            for j in range(10):
                                    train[image_no,0] = t1
                                    a=img[i*6:((i+1)*6-1),(j)*6:((j+1)*6)-1]
                                    dctvariable1[image_no,k]=a[0,1]
                                    k=k+1
                                    dctvariable1[image_no,k]=a[1,0]
                                    k=k+1
                                    dctvariable1[image_no,k]=a[2,0]
                                    k=k+1
                                    dctvariable1[image_no,k]=a[1,1]
                                    k=k+1
                                    dctvariable1[image_no,k]=a[0,2]
                                    k=k+1
                    except Exception as ex:
                        continue
            except Exception as ex:
                continue
        mat.savemat("feature.mat",{'dct':dctvariable1,'train':train,'name':name})
        if self.gui != None:
            self.gui.Message.config(text = "Feature Extracted")
            self.gui.mas.update()

    def testfun(self,c=None):
        f = mat.loadmat("feature.mat")
        dctvariable1 = f["dct"]
        train = f["train"]
        name = f["name"]
        svm_params = dict( kernel_type = cv2.SVM_LINEAR,svm_type=cv2.SVM_C_SVC,C=2.67, gamma=5.383 )
        svm=cv2.SVM()
        print train
        svm.train(dctvariable1,train,params=svm_params)
        test=np.zeros((1,500),np.float32)
        image='.\\database\\test\\crop\\1.jpg'
        img=self.dctim(image)
        img=np.asarray(img)
        image_no = 0
        k=0
        for i in range(10):        
            for j in range(10):
                    a=img[i*6:((i+1)*6-1),(j)*6:((j+1)*6)-1]
                    test[image_no,k]=a[0,1]
                    k=k+1
                    test[image_no,k]=a[1,0]
                    k=k+1
                    test[image_no,k]=a[2,0]
                    k=k+1
                    test[image_no,k]=a[1,1]
                    k=k+1
                    test[image_no,k]=a[0,2]
                    k=k+1
        
        result=svm.predict(test)
##        print result
##        print name
        result = name[int(result)]
        
        flg  = 0
        result = result.replace(" ","")
        value_m = []
        for fil in os.listdir(".\\database\\"+result+"\\crop\\"):
##            print fil
            imagepath1=".\\database\\"+result+"\\crop\\"+fil
            imagepath='.\\database\\test\\crop\\1.jpg'#enter the address of the image obtained
            if compare1(imagepath,imagepath1):
                flg = 1
                break
            
##            src2 = cv2.imread(imagepath,0)
##            src1 = cv2.imread(imagepath1,0)   # load first image in grayscale
##                #src2 = cv2.imread('2.jpg',0)     # load second image in grayscale
##
##            src1 = np.float32(src1)             # convert first into float32
##            src2 = np.float32(src2)             # convert second into float32  
##            ret = cv2.phaseCorrelate(src1,src2) # now calculate the phase correlation
##                #value=math.fabs(ret[0])
##            value=ret[1]
##            value_m.append(value)
##        h_count = 0
##        n_count = 0
##        print value_m
##        for item in value_m:
##            if item>-0.12 and item <= 0:
##                h_count=h_count+1
##            if item<0.12 and item >= 0:
##                n_count=n_count+1
        if flg == 1:
             if self.gui != None:
                self.gui.Message.config(text = result)
                self.gui.mas.update()
                return result
             else:
                print result
        else:
            if self.gui != None:
                self.gui.Message.config(text = "not found")
                self.gui.mas.update()
                return "not found"
            else:
                print "not found"
            
            
if __name__ == "__main__":
    ap = feature1()
    ap.extract()
    ap.testfun()
