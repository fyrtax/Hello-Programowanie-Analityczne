from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

def przycisk1(a):
    print('naciśnięto przycisk 1', a)

def przycisk2(a):
    if a.text == 'przycisk 2':
        print('naciśnięto przycisk 2', a)
    else:
        print('naciśnięto przycisk 3', a)

app = App()

app.root = BoxLayout(orientation='vertical')
app.root.add_widget(Label(text='Nasz pierwszy napis'))
app.root.add_widget(Label(text='Druga labelka'))

pb1 = Button(text='pierwszy przycisk')
pb1.bind(on_press=przycisk1)
app.root.add_widget(pb1)

pb2 = Button(text='przycisk 2')
pb2.bind(on_press=przycisk2)
app.root.add_widget(pb2)

pb3 = Button(text='przycisk 3')
pb3.bind(on_press=przycisk2)
app.root.add_widget(pb3)

app.run()