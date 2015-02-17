# -*- coding: utf8 -*-

import io

def file_len(fname):
    with open(fname) as f:
    	i = 0
        for l in f:
        	if "==" in l:
        		pass
        	elif "//" in l:
        		pass
        	else:
        		i += 1
    return i

def make_list(name):
	db1 = name+".txt"
	db2 = name+".py"
	dictName = name+"_"
	length = file_len(db1)
	print length

	with io.open(db1,'r', encoding='utf8') as f1, io.open(db2,'wb') as f2:
		count = 0

		f2.write("# -*- coding: utf8 -*-\n\n"+dictName+" = {\n")
		for line in f1:
			line = line.encode('utf-8')
			if "==" in line:
				pass
			elif "//" in line:
				pass
			else:
				if "'" in line:
					line = line.replace("'", "\\\'")
				if '"' in line:
					line = line.replace('"', '\\\"')
				count += 1
				A = line.rstrip('\n\r ')
				if count != length:
					f2.write(str(count)+" : "+"('"+A+"'), \n")
				else:
					f2.write(str(count)+" : "+"('"+A+"') \n")
		f2.write("}")

files = ["adjectif", "bonjour", "chiffre", "chiffrelitt", "congen", "non", "oui", "plein", "smileys", "smileystristes", "super"]

for e in files:
	make_list(e)


# -*- coding: utf8 -*-

