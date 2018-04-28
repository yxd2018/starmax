L = [8, 3, 2, 3, 1, 5, 4, 7, 0, 9]
L = sorted(L)
print L
a, b = divmod(len(L), 2)
print "a:%s,b:%s"%(a,b)
if b == 0:
    print (L[a-1]+L[a])/2.0
else:
    print L[a]