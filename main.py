from PIL import Image, ImageDraw
from itertools import combinations
from logic import xor
import os
lineList = 'ABCDEFGHIJK'

if not os.path.exists('./results'):
   os.makedirs('./results')

#set up constants for size constraints
x = 5
y = 10
wid = 40
hei = 80

# x = 20
# y = 20
# wid = 180
# hei = 360

spriteWidth = 10

width = 2 * x + wid
height = 2 * y + hei

#set up colors for 
white = (255, 255, 255)
black = (0, 0, 0)

#Take an input string and create an image of the coresponding rune
def runeToPic(s):
	filename = F"./results/{s}.png"
	print(filename)
	im = Image.new('RGB', (width, height), white)
	d = ImageDraw.Draw(im)

	#set up some constants for the positions of the lines
	p1 = (x, y)
	p2 = (x + wid, y)
	p3 = (x, y + int(.5 * hei))
	p4 = (x + wid, y + int(.5 * hei))
	p5 = (x, y + hei)
	p6 = (x + wid, y + hei)
	
	#pseudoSwitch for the line segments
	runeLineSwitch = {
		"A": [p4, p5],
		"B": [p3, p5],
		"C": [p2, p3],
		"D": [p1, p3],
		"E": [p1, p2],
		"F": [p3, p4],
		"G": [p5, p6],
		"H": [p2, p4],
		"I": [p1, p4],
		"J": [p4, p6],
		"K": [p3, p6]
	}
	for char in s:
		d.line(runeLineSwitch[char], black)
	im.save(filename)


#gets all possible combinations of lineList that are n long
def getAll(n):
	i = combinations(lineList, n)
	istr = map(''.join, i)
	return istr

#based upon a predetermined diagram (included),
#checks whether or not the current rune string 
#has a mirror pair
def isMirrorable(runeString):
	mirrorCheck = lambda a, b : xor(a in runeString, b in runeString)
	ak = mirrorCheck('A', 'K')
	bj = mirrorCheck('B', 'J')
	ci = mirrorCheck('C', 'I')
	dh = mirrorCheck('D', 'H')
	if any([ak,bj,ci,dh]):
		return True
	else:
		return False

#returns the rune string of the mirror pair for the given input
def returnMirror(runeString):
	mirrorString = ''
	for c in runeString:
		mirrorString += returnMirrorChar(c)
	mirrorString = ''.join(sorted(mirrorString))
	return mirrorString


#returns the character at the mirror spot on the diagram
def returnMirrorChar(mChar):
	mirrorSwitch = {
		"A": "K",
		"B": "J",
		"C": "I",
		"D": "H",
		"E": "E",
		"F": "F",
		"G": "G",
		"H": "D",
		"I": "C",
		"J": "B",
		"K": "A"
	}
	return mirrorSwitch[mChar]

#creates a list of possible rune combinations
#and separates them into two lists based upon LR mirroring
#if the rune is its' own mirror, -> uniqueList
#if the rune has a mirror pair,
#and the mirrored pair is not already in mirrorList -> mirrorList
def runeListCreate(n):
	lst = getAll(n)
	mirrorList = []
	uniqueList = []
	for rune in lst:
		if isMirrorable(rune):
			if not returnMirror(rune) in mirrorList:
				mirrorList.append(rune)
		else:
			uniqueList.append(rune)
	return (mirrorList, uniqueList)


def runeSheetCreate(n):
	#initialize lists of runes
	runeList = runeListCreate(n)
	mirrorList = runeList[0]
	uniqueList = runeList[1]
	#create the sheet
	drawSheet(mirrorList, 'mirror_' + str(n))
	drawSheet(uniqueList, 'unique_' + str(n))

def drawSheet(runeList, name):
	spriteHeight = len(runeList)//spriteWidth + 1
	img = Image.new("RGB", (width*spriteWidth, height*spriteHeight), white)
	dr = ImageDraw.Draw(img)
	num = 0
	for rune in runeList:
		#print(str(rune) + ' at ' + str(num))
		xloc = (num % spriteWidth) * width
		yloc = (num // spriteWidth) * height
		drawRuneSprite(xloc, yloc, dr, rune)
		num += 1
	img.save(F"./results/{name}.png")

def drawRuneSprite(xn, yn, dr, rune):
	xtemp = x + xn
	ytemp = y + yn

	p1 = (xtemp,ytemp)
	p2 = (xtemp + wid, ytemp)
	p3 = (xtemp, ytemp + int(.5*hei))
	p4 = (xtemp + wid, ytemp + int(.5*hei))
	p5 = (xtemp, ytemp + hei)
	p6 = (xtemp + wid, ytemp + hei)

	runeLine = {
		"A": [p4,p5],
		"B": [p3,p5],
		"C": [p2,p3],
		"D": [p1,p3],
		"E": [p1,p2],
		"F": [p3,p4],
		"G": [p5,p6],
		"H": [p2,p4],
		"I": [p1,p4],
		"J": [p4,p6],
		"K": [p3,p6]
	}

	for c in rune:
		dr.line(runeLine[c], black)

runeToPic("AKBJ")

#print(isMirrorable("AKBJ"))		
# for i in range(1,11):
# 	runeSheetCreate(i)