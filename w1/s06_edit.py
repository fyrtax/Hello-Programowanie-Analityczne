from kivy.app import App
from kivy.uix.filechooser import FileChooserListView


class S06_NaszEdit(App):
    def build(self):
        return self.root

    def przycisk_open(self, nazwaed, oknoed):
        print('naciśnięto open')

        self.oknoed = oknoed
        self.nazwaed = nazwaed
        fc = FileChooserListView(path='.')
        fc.bind(on_submit=self.load)
        self.root.add_widget(fc)

    def load(self, *args):
        fc, nazwa, *reszta = args
        self.nazwaed.text = nazwa[0]
        with open(nazwa[0]) as plik:
            tekst = plik.read()

        self.oknoed.text = tekst
        self.root.remove_widget(fc)

    def zapisz(self, nazwaed, oknoed):
        self.nazwaed = nazwaed
        self.oknoed = oknoed
        fc = FileChooserListView(path='.')
        fc.bind(on_submit=self.do_save)
        self.root.add_widget(fc)

    def do_save(self, *args):
        fc, nazwa, *reszta = args
        self.nazwaed.text = nazwa[0]
        with open(nazwa[0], 'w') as plik:
            plik.write(self.oknoed.text)

        self.root.remove_widget(fc)


app = S06_NaszEdit()
app.run()
