from kivy.app import App
from kivy.uix.filechooser import FileChooserListView

class S06_NaszEdit(App):
    def build(self):
        return self.root

    def przycisk_open(self, nazwaed, oknoed):
        print('Naciśnięto Open')
        
        self.oknoed = oknoed
        self.nazwaed = nazwaed
        fc = FileChooserListView(path='.')
        fc.bind(on_submit=self.load)
        self.root.add_widget(fc)
        
        # tinaz = self.root.ids['tiNazwa']
        # print(tinaz.text)
        
        # with open(nazwa.text) as plik:
        #     tekst = plik.read()
        #     print(tekst)
        
        # print(self.root.ids)
        # tint = self.root.ids['lbNaszTekst']
        # tint.text = tekst
        # lab.text = tekst
    
    def load(self, *args):
        print(args)
        fc, nazwa, *reszta = args
        print(nazwa)
        self.nazwaed.text = nazwa[0]
        with open(nazwa[0]) as plik:
             tekst = plik.read()
             print(tekst)
        self.oknoed.text = tekst
        self.root.remove_widget(fc)

    def zapisz(self, nazwa, tekst):
        with open(nazwa.text, 'w') as plik:
            plik.write(tekst.text)

app = S06_NaszEdit()
app.run()