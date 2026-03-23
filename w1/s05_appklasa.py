from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class Druga(App):
    przycisk_licznik = {}

    def build(self):
        self.root = BoxLayout(orientation='vertical')

        self.dodaj_napis('Nasz pierwszy napis')
        self.dodaj_napis('Druga labelka')
        self.dodaj_przycisk(f'pierwszy przycisk')
        self.dodaj_przycisk(f'przycisk 2')
        self.dodaj_przycisk(f'przycisk 3')

        return self.root

    def dodaj_napis(self, napis):
        self.root.add_widget(Label(text=napis))

    def przycisk(self, a):
        self.przycisk_licznik[id(a)]['licznik'] += 1
        print(f'nacisnieto przycisk', a.text)

        przycisk = self.przycisk_licznik[id(a)]

        a.text = f"{przycisk['napis']} ({przycisk['licznik']})"

    def dodaj_przycisk(self, napis):
        pb = Button(text=napis)
        pb.bind(on_press=self.przycisk)
        self.przycisk_licznik[id(pb)] = {'napis': napis, 'licznik': 0}
        self.root.add_widget(pb)


app = Druga()
app.run()
