class Pierwsza:
    def pierwsza(zmienna):
        print("pierwsza")
        print(zmienna, id(zmienna))

    def metoda(self):
        print("metoda pierwsza")


p1 = Pierwsza()
print(p1, type(p1), hex(id(p1)))
p1.pierwsza()  # p1.pierwsza(p1)


class Druga:
    b = 2

    def druga(self):
        print("metoda w klasie druga", id(self))

    def wyswietl(self):
        print(f'attr: b {self.b}, d: {self.d}')

    def metoda(self):
        print("metoda druga")


d1 = Druga()
print(d1, id(d1))
d1.druga()
d1.d = 9
d1.wyswietl()
print(d1.d)


class Trzecia:
    def __init__(self, w=0):
        print(f'inicjalizacja ze zmienną w {w}, ref: {id(self)}')
        self.war = w

    def __str__(self):
        return f'war: {self.war}'

    def metoda(self):
        print("metoda trzecia")


t1 = Trzecia(5)
print(t1, id(t1))

t2 = Trzecia(6)
print(t2.war)
print(t2)


class Wspolna(Pierwsza, Druga, Trzecia):
    def __str__(self):
        # orgciag = Trzecia.__str__(self)
        orgciag = super().__str__()
        return f'{orgciag} {self.b} {self.b}'

    def wszystkie_m(self):
        # Pierwsza.metoda(self)
        # Druga.metoda(self)
        # Trzecia.metoda(self)

        # r = Wspolna.__mro__
        # for i in r:
        #     if hasattr(i, 'metoda'):
        #         i.metoda(self)

        [i.metoda(self) for i in self.__class__.__mro__ if hasattr(i, 'metoda')]


w1 = Wspolna(4)
print(w1.b, w1)
w1.metoda()

print(Wspolna.__mro__)
w1.wszystkie_m()


class Piedzie:
    def a(self):
        print("a")

    def b(self):
        print("b")

    def c(self):
        print("c")


class Duodzie:
    def d(self):
        print("d")

    def e(self):
        print("e")

    def f(self):
        print("f")

    def g(self):
        print("g")


class MojaDzie(Piedzie, Duodzie):
    def __init__(self, *args, **kwargs):
        self.a = args
        self.k = kwargs

    def __str__(self):
        return str((self.a, self.k))

    def wyswietl(self):
        print(f'attr: a: {self.a}, k: {self.k}')


m1 = MojaDzie()
print(m1)

m2 = MojaDzie(6)
print(m2)

m3 = MojaDzie(4, 5, 5)
print(m3)

m4 = MojaDzie(5, a=5, b=9)
print(m4)

m4.wyswietl()
# MojaDzie conajmniej 10 metod, max 4 w niej zdefiniowane
