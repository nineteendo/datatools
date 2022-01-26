#JSON SEARCHER by CLC2020
a=input("Search: ")
import os
for dir in sorted(os.listdir()):
    if os.path.isdir(dir):
        b=0
#change ZOMBIETYPES.json in a repeating path to search in folders/repeating path
        for c in open(os.path.join(dir,"ZOMBIETYPES.json"),'r').readlines():
            b+=c.count(a)
        print(dir+":"+str(b))
