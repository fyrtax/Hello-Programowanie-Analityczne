from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
class LewyPrzyc(Button):
    pass

class NScreen(Screen):
    def switch(self, root, name, dir):
        root.manager.transition.direction = dir
        root.manager.current = name
class NaszSc1(NScreen):
    pass
class NaszSc2(NScreen):
    pass
class NaszSc3(NScreen):
    pass
class NaszSc4(NScreen):
    pass

class S07_NaszScreen(App):
    def build(self):
        smr = ScreenManager()
        smr.add_widget(NaszSc1(name='pierwszy'))
        smr.add_widget(NaszSc2(name='drugi'))
        smr.add_widget(NaszSc3(name='trzeci'))
        smr.add_widget(NaszSc4(name='czwarty'))
        return smr
    
    # def switch(self, root, name, dir):
    #     root.manager.transition.direction = dir
    #     root.manager.current = name
    

app = S07_NaszScreen()
app.run()