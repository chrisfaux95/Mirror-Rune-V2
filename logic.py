#just a simple library of logic functions


#XOR
def xor(a,b):
	if (a and b) or (not a and not b):
		return False
	elif (a and not b) or (not a and b):
		return True


#XAND
def xand(a,b):
	if (a and b) or (not a and not b):
		return True
	elif (a and not b) or (not a and b):
		return False