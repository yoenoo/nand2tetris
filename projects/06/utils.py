import re

def remove_comment(x):
	return re.sub(r"//.*$", "", x)

def remove_whitespace(x):
	return re.sub("\s", "", x)
