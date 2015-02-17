# -*- coding: utf8 -*-

import re

s1 = "|foo"
s2 = "foo|"
s3 = "|bar|"

text = "bar"

reg = "ffff~infoNeededHere~ ddd"

def test(s):
	if "|" in s :
		if s.count('|') == 2 and s.replace("|", "") == text:
			return "doublebar!!"
		if s.startswith("|"):
			s = s.replace("|", "")
			if s in text and text.startswith(s): 
				return "bar debut"
		if s.endswith("|"):
			s = s.replace("|", "")
			if s in text and text.endswith(s): 
				return "bar fin"


def regex(s):
	match = re.search(r"^.*\~(.*)\~.*$", s)
	return match.group(1)

print regex(reg)

