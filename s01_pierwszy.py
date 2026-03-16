print('Hello world!')

a = 8
print(type(a))
print(type('gg'))
print(type(6.7))
print(type(None))

a, *b = (3, 4, 5, 7)

print(a, type(a))
print(b, type(b))

a, *b, c = (1, 2, 3, 4, 5, 6)
print(a, b, c)

print(2 == 3, type(2 == 3))

li = [1, 2, 3, 5, 6]
tu = (1, 2, 3, 5, 6)
print(li, type(li))
print(tu, type(tu))

# tu[1] = 0
tu = (1, 0, 3, 4, 5, 6)

se = {3, 4, 5, 7, 2, 3, 7}
print(se, type(se))

di = {'k': 2, 's': 9, 'g': 6}
print(di, type(di))

f = {8: [2, 4, 4, 4], (4, 5, 67): (2, 3, 6)}
print(f)

if 2 in tu:
    print('g')
elif 3 in li:
    print('gg')
else:
    print('ggg')

i = 0
while i < 10:
    i += 2

for i in tu:
    continue

for k, v in di.items():
    print(k, v)

for v in di.values():
    print(v, end=',')

for k in di.keys():
    print(k, end=',')


def moj_fun(a=7):
    print(a)


moj_fun(6)
print(type(moj_fun(6)))


def moj_fun2(a, b):
    return a + b


print(moj_fun2(3, 4))


def moj_fun3(a, b, c=0, d=0, e=0, f=0):
    return a, b, c, d, e, f


print(moj_fun3(1, 2))
print(moj_fun3(3, 4, 5, 6, 7))
print(moj_fun3(2, 4, 6))

print('i (%d) ref: %d' % (i, id(i)))
print('a (' + str(a) + ') ref: ' + str(id(a)))
print('b ({}) ref: {}'.format(b, id(b)))
print(f'c ({c}) ref: {id(c)}')

li = [1, 2, 3, 4, 5]


def moj_fun4(lista, idx, val):
    try:
        lista[idx] = val
    except IndexError:
        print('index out of range')
    else:
        return lista


print(li)
print(moj_fun4(li, 4, 10))
print(moj_fun4(li, 5, 10))
print(li)


def moj_dow(*pos, **naz):  # *args, **kwargs
    print(pos)
    print(naz)


moj_dow(1, 2, 3, 4, e=6, f=3, w=1)


class A:
    def __init__(self, a):
        self.a = a

    def show(self):
        print(self.a)


a = A(7)
a.show()
