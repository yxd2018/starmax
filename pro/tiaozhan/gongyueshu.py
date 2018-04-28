#coding:utf-8
"""
#求最大公约数

a = 30
b = 50
for i in range(1,min(a,b)+1):
    if a%i == 0 and b%i == 0:
        n = i
print n
"""
"""
#求最小公倍数
a = 7
b = 5
num = max(a, b)
while True:
    if num % a == 0 and num % b == 0:
        n = num
        print n
        break
    else:
        num += 1
        continue
"""

"""
#求出字典key
a = {"1": 1, "2": 2, "3": 3}

b = {1: 1, 2: 2, 3: 3}
s = ''
for key in b.keys():
    # print key
    s = s+str(key)+','
print s

print(','.join(sorted(a.keys())))
"""
"""
#求出100以内的素数
data = [2, ]
for i in range(3, 101):
    for j in range(2, i):
        if i % j == 0:
            break
    else:
        data.append(i)
print ' '.join(map(str, data))
"""

"""
#序列升序排列
L = [8,2,50,3]
for i in range(0, len(L)):
    for j in range(i,len(L)):
        if L[i]>L[j]:
            L[i],L[j]=L[j],L[i]
print L
"""
"""
#查询日期
s = '2018-04-13'
import datetime

day=datetime.datetime.strptime(s,'%Y-%m-%d')
print(day)
print(int(day.strftime('%j')))
print(str(int(day.strftime('%j')))+" "+str(int(day.strftime('%U'))+1))

"""