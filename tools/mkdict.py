# -*- coding: utf8 -*-

import io

def make_dict(name):
	db1 = name+".txt"
	db2 = name+".py"
	dictName = name+"_"
	with io.open(db1,'r', encoding='utf8') as f1, io.open(db2,'wb') as f2:
		count = 0
		f2.write("# -*- coding: utf8 -*-\n\n"+dictName+" = {\n")
		for line in f1:
			line = line.encode('utf-8')
			if "==" in line:
				pass
			elif "//" in line:
				pass
			elif "=" in line:
				if "'" in line:
					line = line.replace("'", "\\\'")
					print "simple : "+str(count)
				if '"' in line:
					line = line.replace('"', '\\\"')
					print "simple : "+str(count)
				count += 1
				A, B = line.rstrip('\n\r ').split('=')
				A1 = A
				B1 = B
				f2.write(str(count)+" : "+"('"+A1+"' , '"+B1+"'), \n")
		f2.write("}")

make_dict("silence")
