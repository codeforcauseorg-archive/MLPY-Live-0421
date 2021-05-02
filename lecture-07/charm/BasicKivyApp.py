from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.button import Button

import cv2

class MyLayout(GridLayout):

    def __init__(self, **args):
        super(MyLayout, self).__init__(**args)
        self.capture = cv2.VideoCapture(1)
        self.cols = 2
        self.imgWidget = Image()
        self.add_widget(self.imgWidget)
        btn = Button(text="Take Photo")
        btn.bind(on_press=self.snap)
        self.add_widget(btn)
        Clock.schedule_interval(self.update, 1/30)

    def snap(self, event):
        cv2.imwrite("myphoto.png", self.imgArray)

    def update(self, event):

        ret, img = self.capture.read()

        if ret:
            self.imgArray = img
            buf = img.tostring()
            texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            self.imgWidget.texture = texture



class MyApp(App):

    def build(self):
        return MyLayout()


MyApp().run()