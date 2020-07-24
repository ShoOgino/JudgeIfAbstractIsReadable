import csv
import neologdn
import re
import MeCab
import copy
import pandas as pd
import json

dataset=[]
row0={}
row1={}
with open('dataset.json') as f:
    d = json.load(f)
    for k in d:
        if(d[k]["isReadable"]==0):
            row0[k]=d[k]
        else:
            row1[k]=d[k]

syou0=len(row0)//10
amari0=len(row0)%10
syou1=len(row1)//10
amari1=len(row1)%10
for i in range(10):
    d={}
    f0=0
    if(i<amari0):
        f0=1
    f1=0
    if(i<amari1):
        f1=1
    for k in range(syou0+f0):
        key,value=row0.popitem()
        d[key]=value
    for k in range(syou1+f1):
        key,value=row1.popitem()
        d[key]=value
    print(d)
    with open('dataset'+str(i)+'.json', 'w') as f:
        json.dump(d, f, indent=4)

