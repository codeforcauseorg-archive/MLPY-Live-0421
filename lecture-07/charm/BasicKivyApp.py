from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
import numpy as np
import cv2

import os

name = input("Enter Your name : ")
images = int(input("Number of images you want to take : "))

faceList = []

class MyLayout(GridLayout):

    def __init__(self, **args):
        super(MyLayout, self).__init__(**args)
        self.classifier = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
        self.capture = cv2.VideoCapture(1)
        self.cols = 2
        self.imgWidget = Image()
        self.faceWidget = Image()
        self.add_widget(self.imgWidget)
        self.add_widget(self.faceWidget)
        btn = Button(text="Take Photo")
        btn.bind(on_press=self.snap)
        self.add_widget(btn)
        Clock.schedule_interval(self.update, 1/30)

    def snap(self, event):
        global images
        faceList.append((self.gray.flatten()))
        images -= 1

        if images == 0:
            y = np.full((len(faceList), 1), name)
            X = np.array(faceList)
            data = np.hstack([y, X])

            if os.path.exists("facedata.npy"):
                old = np.load("facedata.npy")

                data = np.vstack([old, data])

            np.save("facedata.npy", data)
            app.stop()






    def update(self, event):

        ret, img = self.capture.read()

        if ret:
            self.imgArray = img

            faces = self.classifier.detectMultiScale(img, 1.2, 5)

            if len(faces) >= 1:
                x, y, w, h = faces[0]
                faceCut = img[y:y+h, x:x+w]
                outface = cv2.resize(faceCut, (100, 100))
                gray = cv2.cvtColor(outface, cv2.COLOR_BGR2GRAY)
                self.gray = gray
                print(gray.shape)
                fliped = outface[::-1]
                face_buf = fliped.tostring()
                texture = Texture.create(size=(fliped.shape[1], fliped.shape[0]), colorfmt='bgr')
                texture.blit_buffer(face_buf, colorfmt='bgr', bufferfmt='ubyte')

                self.faceWidget.texture = texture




            fliped = img[::-1]
            buf = fliped.tostring()
            texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.imgWidget.texture = texture



class MyApp(App):

    def build(self):
        return MyLayout()


app = MyApp()

app.run()