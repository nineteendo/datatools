import os
added=[]
removed=[]
for dir in os.listdir():
	if os.path.isdir(dir):
		current=[]
		added.append(5*" "+dir)
		c=d=e=0
		for b in open(os.path.join(dir,"ZOMBIETYPES.json"),'r').readlines():
#1st check
			f=c==2 and e==2
#{}
			if "{" in b:
				c+=b.count("{")
			if "}" in b:
				c-=b.count("}")
#[]
			if "[" in b:
				e+=b.count("[")
			if "]" in b:
				e-=b.count("]")
#2nd check
			if c==2 and e==2 and f:
				a=b[17:-2]
				current.append(a)
				if not a in added:
					added.append(a)
		for b in added:
			if not b in current and not b in removed:
				removed.append(b)
for a in added:
	if " " in a:
		e+=1
	else:
		c=0
		for b in removed:
			if a==b:
				a=" "
			if " " in b:
				f=a
				if e>c:
					f=" "
				print(f)
				e+=1