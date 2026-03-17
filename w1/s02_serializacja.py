ciag = 'ala ma kota'
plik = open('a', 'w')

print(type(plik))

plik.write(ciag)
plik.write('\ngg')

plik.close()

plik = open('a', 'r')
print(plik.read())
plik.close()

with open('a', 'a') as f:
    f.write(ciag)

with open('b', 'wb') as f:
    f.write(b'ala ma kota\x0aipsa')

# def zapli(li, plik):
#     with open(plik, 'w') as f:
#         for x in li:
#             f.write(str(x) + '\n')
#
#
# def wczyli(plik):
#     li = []
#     with open(plik, 'r') as f:
#         for x in f.readlines():
#             d = x.rstrip('\n')
#             li.append(int(d))
#
#     return li

zapli = lambda li, plik: open(plik, 'w').writelines(f"{x}\n" for x in li)
wczyli = lambda plik: [int(line) for line in open(plik)]

lista = [6, 4, 1, 9, 4, 7, 2]

print(lista)
zapli(lista, 'li')
now_lista = wczyli('li')
print(now_lista)

slow = {'k1': 3, 'k2': 9, 'k3': 3, 'k4': 4}

import json

with open('li.json', 'w') as f:
    json.dump(slow, f, indent=2)

with open('li.json', 'r') as f:
    gg = json.load(f)

print(gg)

import pickle


class A:
    def __init__(self, a):
        self.a = a

    def show(self):
        print(self.a)


a = A(7)
a.show()

with open('obj.pickle', 'wb') as f:
    pickle.dump(a, f)

with open('obj.pickle', 'rb') as f:
    b = pickle.load(f)

b.show()
