
from __future__ import division, print_function, absolute_import

import numpy as np
from tkinter import *
from PIL import Image, ImageDraw 
import tensorflow as tf

root = Tk() #interface
 #image is taken as input
f = Frame(root, height=200, width=400, background="white") # a frame is created for GUI
f.pack() # pack is used to display on the screen

label = Label(root)
label.pack()

class ImageGenerator:
    
    def __init__(self,parent,posx,posy,*kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 155
        self.sizey = 275
        self.b1 = "up"
        self.xold = None
        self.yold = None 
        self.drawing_area=Canvas(self.parent,width=self.sizex,height=self.sizey, background='white')
        self.drawing_area.place(x=self.posx,y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        # self.drawing_area.bind("<ButtonPress-2>", self.clear)
        self.button1=Button(self.parent,text="Clear",bg='white',command=self.clear)
        self.button1.pack(side=LEFT)
	
        self.image=Image.new("RGB",(155,275),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

##################################################### clear the paintbox ###############################	    
    def clear(self):
        self.drawing_area.delete("all")
        self.image=Image.new("RGB",(155,275),(255,255,255))
        self.draw=ImageDraw.Draw(self.image)

    def b1down(self, event):
        self.b1 = "down"

    def b1up(self, event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self,event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,self.yold,event.x,event.y,smooth='true',width=7,fill='black')
                self.draw.line(((self.xold,self.yold),(event.x,event.y)),(0,0,0),width=7)

        self.xold = event.x
        self.yold = event.y

if __name__ == "__main__":
   
    root.wm_geometry("%dx%d+%d+%d" % (400, 400, 10, 10))
    root.config(bg='white')
    a = ImageGenerator(root,1,1)

################################## loading model ############################################
def prediction():
   
    loaded_model = tf.keras.models.load_model("model.tf")
    img = a.image
    img = img.convert('L')
    
    img = img.resize((28,28))
    img.save("a.png")
    img = np.array(img.getdata()).reshape(img.size[0],img.size[1],1)
    
    img = np.expand_dims(img, axis=0)
    X_test = img

    X_test = X_test.astype('float32')
    X_test /= 255

    prediction = loaded_model.predict(X_test)

    global num
    num = np.argmax(prediction)
    print("The predicted number is :")
    print(num)

    w = Message(root, background="white", text=num)
    w.pack(side=BOTTOM)

    m = Message(root, background="white",text="The predicted number is:")
    m.pack(side=BOTTOM)	
   	
button = Button(f, text="Prediction", background= "white", command=prediction)
button.pack(side=LEFT)
quitButton = Button(f, text="Quit", background= "white",fg="red", command=f.quit)
quitButton.pack(side=LEFT)
root.geometry("550x550")
root.mainloop()

