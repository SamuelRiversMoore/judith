import io
import re

import os.path
from flask import request
from time import gmtime, strftime
import json

from random import randint

# DATABASES :
from db.corrections import *
from db.master import *
from db.gen.integral import *

import sys
reload(sys) # Reload does the trick!
sys.setdefaultencoding('UTF8')

# -*- coding: utf8 -*-


def get_time(request):
	date = strftime("%Y-%m-%d", gmtime())
	entry_time = strftime("%H:%M:%S", gmtime())
	hour = strftime("%H", gmtime())
	if request == "date":
		return date
	if request == "entry_time":
		return entry_time
	if request == "hour":
		return int(hour)+1

def get_client_ip():
	return request.environ["REMOTE_ADDR"] # request.headers['X-Real-IP']

def read_db(text): 

	# Get db
	if get_file("read", "general", "get_db" ):
		db = globals()[get_file("read", "general", "get_db" )]
	else : db = db_master

	# Make corrections :
	text = text.lower().encode('utf-8')
	text = make_corrections(text, db_correction)
	
	# Sent_text processing - returns a list of keys of the possible answers :
	entry_list = parse_entry(text, db)
	print entry_list

	# Write the sent text in archive :
	get_file("write", "archive", get_time("entry_time")+" USER : "+text)

	# Possible_answers processing - returns the best one as a string. :
	if entry_list: 
		result = str(get_output(entry_list, text, db))
		result = make_corrections(result, db_correctionbot)
	else:
		result = "..."
	return result











# Compare each input of the database with text to find matches :
def parse_entry(text, db):
	key_list = []
	for key in db:
		tmp_stock = []
		s = db[key][0].lower()
		rep = db[key][1]
		if "~" in s:
			s = test_tilde(s, text)
		if "{" in s or "[" in s:
			s = test_cond(s, text)
		if "(*)" in s:	
			s = test_star(s, text)
		if "|" in s:
			s = test_bar(s, text)
		if "<-continuer->" in rep :
			if "[" in rep or "{" in rep:
				stored_rep = rep.replace("[","{").replace("]","}")
				tmp_stock = re.findall(r"(\{.*?\})", stored_rep)
		if s in text:
			key_list.append(key)
			if tmp_stock:
				get_file("write", "archive", get_time("entry_time")+" BOT : "+str(tmp_stock))
	return key_list

def test_cond(s, text):
	if "[" in s:
		for e in re.findall(r"(\[.*?\])", s):
			s = s.replace(e, "")
	if "{" in s:
		cond = re.findall(r"({.*?})", s)
		for e in cond:
			e2 = e.replace("{", "").replace("}", "")
			if e2.startswith("nulle"):
				if not get_file("read", "general", e2.replace("nulle ", "") ):
					s = s.replace(e, "")
			elif e2.startswith("temp:"):
				if get_file("read", "archive", e2 ):
					s = s.replace(e, "")
			elif e2.startswith("var"):
				if get_file("read", "general", e2.replace("var ", "") ):
					s = s.replace(e, "")
			elif e2.startswith("heure"):
				val = e2.replace("heure ", "").split("-")
				if int(val[0]) <= get_time("hour") < int(val[1]):
					s = s.replace(e, "")
			else:
				if get_file("read", "general", e2):
					s = s.replace(e, "")
	return s

def test_tilde(s, text):
	for e in re.findall(r"~(.*?)~", s):
		gen = globals()["db_"+e]
		for k in gen:
			sub = gen[k]
			if "|" in sub:
				sub = test_bar(sub, text)
			if sub in text:
				s = s.replace('~'+e+'~', sub)
	return s

def test_star(s, text):
	splt = s.split("(*)")
	tmp_list = []
	for num, e in enumerate(splt):
		if "|" in e:
			e = test_bar(e, text)
			splt[num] = e
		if e in text:
			tmp_list.append(e)
	if tmp_list == splt:
		s = text
	return s

def test_bar(s, text):
	s1 = s.replace("|", "")
	if s.count('|') == 2 and s1 == text:
		return s1
	elif s.startswith("|") and not s.endswith("|") and s1 in text and text.startswith(s1): 
		return s1
	elif s.endswith("|") and not s.startswith("|") and s1 in text and text.endswith(s1): 
		return s1
	else:
		return s








# Corrections for input and output texts :
def make_corrections(text, db):
	for key in db:
		if db[key][0] in text:
			text = text.replace(db[key][0], db[key][1]+" ").replace("  "," ")
	return text

# Process each possible answers to format it and find the best one :
def get_output(entry_list, text, db):
	if entry_list:
		rep2 = ""
		list_length = []
		for e in entry_list:
			list_length.append(e)

		for e in list_length:
			bestEntry = entry_list[0]
			print bestEntry
			s = db[bestEntry][0]
			rep = db[bestEntry][1]
			continuer = False
			if '|' in rep: # Randomly chose one output between the proposed ones
				rep = rep.split('|')
				length = len(rep)
				randNum = randint(0, length-1)
				rep = rep[randNum]
			if "<-continuer->" in rep: # Get next answer and remember this one
				rep2 = rep2+rep
				if bestEntry in entry_list: 
					entry_list.remove(bestEntry)
					print "removing "+str(bestEntry)+" (continuer)"
					continuer = True
			if "<-ignorer->" in rep: # Forget this answer
				rep2 = rep2+rep.replace("<-ignorer->", "")
				while bestEntry in entry_list: 
					entry_list.remove(bestEntry)
					print "removing "+str(bestEntry)+" (ignorer)"
					rep = rep.replace("<-ignorer->", "")
					continuer = True
			if "<-noreut->" in rep: # Don't re-use this answer next time
				rep = rep.replace("<-noreut->", "")
				if get_file("read", "general", bestEntry):
					while bestEntry in entry_list:
						entry_list.remove(bestEntry)
						print "removing "+str(bestEntry)+" (noreut)"
						continuer = True
				else:
					get_file("write", "general", e)
			if "(*" in rep: # Fill blank jockers with variable text
				is_number = re.findall(r"\(\*(.*?)\)", rep)
				splited_val = s.lower().split("(*)")
				jocker = text
				for e in splited_val:
					if e in jocker : jocker = jocker.replace(e,'#')
				jocker = jocker.split('#')
				jocker = filter(None, jocker)
				if s.count("(*)") < len(jocker):
					jocker.pop(0)
				jocker = filter(None, jocker)
				for e in is_number:
					if e:
						if e > 1: 
							rep = rep.replace("(*"+str(e)+")", jocker[int(e)-1])
					else:
						rep = rep.replace("(*)", jocker[-1])			
			if "<-modvar" in rep: # Add or modify a variable in bot's memory
				modvar = re.findall(r"<-modvar\((.*?)\)->", rep)
				modvar = filter(None, modvar)
				for e in modvar:
					get_file("write", "general", e)
					rep = rep.replace("<-modvar("+e+")->","")
			if "<-var" in rep: # Use a variable in bot's memory
				var = re.findall(r"<-var\((.*?)\)->", rep)
				var = filter(None, var)
				for e in var:
					if get_file("read", "general", "var "+e):
						result = get_file("read", "general", "var "+e)
						rep = rep.replace("<-var("+e+")->", result)
					else:
						while bestEntry in entry_list:
							entry_list.remove(bestEntry)
							print "removing "+str(bestEntry)+" (var)"
							continuer = True
			if "<-compter" in rep:
				compter = re.findall(r"<-compter\((.*?)\)->", rep)
				compter = filter(None, compter)
				for e in compter:
					if any(char.isdigit() for char in e):
						if "x" in e: e = e.replace("x", "*")
						calc = eval(e)
						print e
						if "*" in e: e = e.replace("*", "x")
						rep = rep.replace("<-compter("+e, "").replace(")->", str(calc))
					else :
						while bestEntry in entry_list:
							entry_list.remove(bestEntry)
							print "removing "+str(bestEntry)+" (no digit)"
							continuer = True
			if rep == "":
				while bestEntry in entry_list:
					entry_list.remove(bestEntry)
					print "removing "+str(bestEntry)+" (empty rep)"
					continuer = True

			if continuer == False:
				print "stop"
				break
			else : print "continue"
						
		if entry_list :
			bestEntry = entry_list[0]

		print bestEntry
		rep = rep2+rep

	if "<-" in rep: # Database switch
		if "<-chgcerva" in rep:
			print "insultes"
			chgcerva = re.findall(r"<-chgcerva\((.*?)\)->", rep)
			chgcerva = filter(None, chgcerva)
			print chgcerva
			for e in chgcerva:
				get_file("write", "general", "get_db=="+e)
				rep = rep.replace("<-chgcerva("+e+")->", "")
				print "db change : "+e

		if "<-url" in rep:
			pass

		if "<-date->" in rep:
			rep = rep.replace("<-date->", get_time("date"))

		if "<-heure->" in rep:
			rep = rep.replace("<-heure->", get_time("hour"))

		if "<-random" in rep:
			random = re.findall(r"<-random\((.*?)\)->", rep)
			random = filter(None, random)
			for e in random:
				if ',' in e:
					rNum = e.split(',')
					randNum = randint(int(rNum[0]), int(rNum[1]))
				else:
					randNum = randint(0, int(e))
				rep = rep.replace("<-random("+e, "").replace(")->", str(randNum))

		if "<-inc" in rep:
			pass


	tmp_memory = []
	if "[" in s : # Write things to remember from user :
		write_gen = re.findall(r"\[(.*?)\]", s)
		for e in write_gen:
			if "temp:" in e:
				tmp_memory.append(e)
			else:
				get_file("write", "general", write_gen)

	if "[" in rep : # Write things to remember from user :
		write_gen = re.findall(r"\[(.*?)\]", rep)
		for e in write_gen:
			if "temp:" in e:
				tmp_memory.append(e)
			else:
				get_file("write", "general", write_gen)

	if tmp_memory:
		tmp_memory = str(tmp_memory)
	else:
		tmp_memory = ""
	
	if "<-continuer->" in rep: # Answer in multiple times
		rep = rep.split("<-continuer->")
		rep = filter(None, rep)
		print rep
		for e, _ in enumerate(rep) : 
			get_file("write", "archive", get_time("entry_time")+" BOT : "+tmp_memory+" "+rep[e])
	else :
		get_file("write", "archive", get_time("entry_time")+" BOT : "+tmp_memory+" "+rep)
		
	if type(rep) is list : rep = '<-continuer->'.join(rep)
	if "[" in rep or "{" in rep:
		rep = test_cond(rep, text)			
	return rep


# Read or write into memory :
def get_file(action, target, data):
	IP = get_client_ip()
	data = str(data)

	dir_path = "judithApp/logs/"+IP
	if not os.path.exists(dir_path): 
		os.makedirs(dir_path)

	if target == "general":
		path = dir_path+"/general.txt"
	if target == "archive":
		path = dir_path+"/archive_"+get_time("date")+".txt"
	if not os.path.exists(path) and action == "read":
		with io.open(path, 'ab') as f:
			f.write("start\n")
		return False

	if action == "read":
		if target == "archive":
			with io.open(path, 'r') as f:
				last_line = (list(f)[-1]).strip()
				if data.replace("{", "").replace("}", "") in last_line:
					return True

		if target == "general":				
			with io.open(path, 'r') as f:
				if data.startswith("var "):
					data = data.replace("var ", "")
					for line in f:
						line = line.rstrip()
						if line.startswith(data):
							result = line.split("==")
							return result[1]
				if data.startswith("get_db"):
					for line in f:
						line = line.rstrip()
						if line.startswith(data):
							result = line.split("==")
							return result[1]
				else:
					for line in f:
						if data.replace("{", "").replace("}", "") in line:
							return True
	if action == "write":
		if target == "archive":
			with io.open(path, 'ab') as f:
				f.write("\n"+data)
		if target == "general":
			memory = []
			memory.append(unicode(data+"\n"))
			with io.open(path, 'rb') as f:
				for line in f:
					if line:
						memory.append(line)
				if "==" in data:
					datasplit = data.split("==")
					for l, line in enumerate(memory):
						if "==" in line and line.startswith(datasplit[0]):
							line = line.replace(line,data+"\n")
							memory[l] = line

			memory = list(set(memory))							
			with io.open(path, 'wb') as f:
				for line in memory:
					f.write(line)

