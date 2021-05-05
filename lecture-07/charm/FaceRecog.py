from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.button import Button
import numpy as np
import cv2

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

data = np.load("facedata.npy")

X = data[:, 1:]
y = data[:, 0]

model = KNeighborsClassifier(4)
model.fit(X, y)

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
        lbl = Label(text="Person name")
        self.lbl = lbl
        self.add_widget(lbl)
        Clock.schedule_interval(self.update, 1/30)


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

                names = model.predict([gray.flatten()])
                self.lbl.text = str(names[0])


                fliped = outface[::-1]
                face_buf = fliped.tobytes()
                texture = Texture.create(size=(fliped.shape[1], fliped.shape[0]), colorfmt='bgr')
                texture.blit_buffer(face_buf, colorfmt='bgr', bufferfmt='ubyte')

                self.faceWidget.texture = texture




            fliped = img[::-1]
            buf = fliped.tobytes()
            texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.imgWidget.texture = texture



class MyApp(App):

    def build(self):
        return MyLayout()


app = MyApp()

app.run()