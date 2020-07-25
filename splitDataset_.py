import csv
import re
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
syou1=len(row1)//10
for i in range(10):
    d={}
    for k in range(syou0):
        key,value=row0.popitem()
        d[key]=value
    for k in range(syou1):
        key,value=row1.popitem()
        d[key]=value
    print(d)
    with open('dataset'+str(i)+'.json', 'w') as f:
        json.dump(d, f, indent=4)
test={}
for k in range(len(row0)):
    key,value=row0.popitem()
    test[key]=value
for k in range(len(row1)):
    key,value=row1.popitem()
    test[key]=value
with open('dataset'+str(10)+'.json', 'w') as f:
        json.dump(d, f, indent=4)
