from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line, Ellipse, Rectangle, Color
from kivy.clock import Clock
from random import randint

class NaszePrzyc(BoxLayout):
    def rysuj(self, co):
        print(co)
        with self.canvas:
            if co == 'linia':
                Line(points=(200, 200, 100, 210, 300, 300))
            if co == 'kolko':
                Ellipse(pos=(400, 300), size=(50, 50))
            if co == 'prost':
                Rectangle(pos=(450, 400), size=(70, 70))
    
    def start_anim(self):
        self.popx = randint(20, 600)
        self.popy = randint(100, 400)
        Clock.schedule_interval(self.animuj, 1)
    
    def animuj(self, cos):
        nx = randint(20, 600)
        ny = randint(100, 400)
        print(f'Animuj {nx} {ny}')
        with self.canvas:
            Line(points=(self.popx, self.popy, nx, ny))
        self.popx = nx
        self.popy = ny


class s08_NaszeRysunki(App):
    lastpos = (100, 100)
    def dotyk(self, pozinf, ek):
        obj, poz = pozinf
        print(poz)
        with ek.canvas:
            Color(0,1,0)
            Line(points=(*self.lastpos, *poz.pos))
        self.lastpos = poz.pos

app = s08_NaszeRysunki()
app.run()