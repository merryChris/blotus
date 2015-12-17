
f = open('cache', 'r')
aaa = f.readlines()
f.close()

ff = open('ccc', 'wb')
for x in aaa[::-1]:
    ff.write(x)
ff.close()
