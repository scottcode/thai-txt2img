# coding: utf-8
# -*- coding: utf-8 -*- 

'''
th2img.py  vers 9.2
@ AUTHOR: J. Scott Hajek, University of Illinois, hajek3@illinois.edu

Version 5_5 includes code that was in useTh2img_1_4.py and includes it here as another function.
Version 5_6 ...not too much change so far...
Version 5_7  (2012-8-28)
	- deleted commented portions of code that are no longer used
	- revised and added explanatory comments
	- change background to white and text fill to black
	- adapted writeFullText to use textListObj (as a class, with .values, .root, .itemnum) instead of earlier simple list of tuples
Version 6_0
	- add centering adjustment for the shrunken vowels over the consonants
Version 6_1
	- add ability to manipulate mis-segmentation (in writeMask) (still not completed)
Version 6_2
	- fix vertical orientation of vowels below main line
Version 7_0
	- add method to shift delimiters (Mis-segmentation Condition)
			It will only occur on the target word. 
			In the mis-segmented condition, the target window will be expanded so that 
			it includes the immediately preceding (how many?) characters and the following (how many?) characters.
Version 7_1
	- finished adding & fixing method to shift delimiters
Version 8_0
	- stable
Version 8_1
	- improve notes and commenting

Version 9_0
	- a new branch, optimizing for creating just an individual image for each
	sentence, while still keeping track of the coordinates between the window
	boundaries. Purpose of keeping coordinates of windows is to separately script
	something to mask the parts of the sentence not in current window.
	- add method 'writeFullGetCoords'
		- try to make the method able to do either full or masking

Version 9_1
	- decided against making writeFullGetCoords able to do masking, too
	- simplify looping structure 

Version 9_2
	- change image filename for saving to be an argument needed by writeFullGetCoords


'''

import ImageFont
import inspect
import os, time
import Image
import ImageDraw

'Variable Values used as defaults for the Methods below'
fontfile = "courmon_scott6_autohint.ttf"
fgColor = "BLACK"
# establish defaults for mkImage method
myMode = "RGB"
useImgType = "PNG"
imgExt = '.png' #image extension
imgFilename = str(time.time())+imgExt
imgSize = (2560,100)
bgColor = "white"  # used as default for color argument in mkImage()
# establish other defaults
fgColorTagged = "BLACK"
masklinewidth = 2
ascenders = u'ปฝฟโใไ'
descenders = u'ญฎฏฐฤฦ'
toneMarksEtc = u'\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D\u0E4E'
vowelsAbove = u'\u0e31\u0e4d\u0e34\u0e35\u0e36\u0e37'
vowelsBelow = u'\u0e38\u0e39'
aboveOrBelow = ''.join((ascenders,descenders,toneMarksEtc,vowelsAbove,vowelsBelow))
charsToChangeSize = ''.join((toneMarksEtc,vowelsAbove,vowelsBelow))  # concatenate the string categories wished to be shrunk. To remove certain categories, just delete the variable name from the join function
	# have taken 'ascenders,descenders,' out of 'join()' above


validSegmentsStr = u"กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮะาเแโใไๅๆฯ฿๏๚๛๐๑๒๓๔๕๖๗๘๙.1234567890 " # a unicode string or a list of unicode strings specifying which characters to be counted (ones that necessarily occupy horizontal space


#===============================================================================
# --mycount--
#
# General counting function to be used as a generator function 
#===============================================================================

def mycount(start=0, step=1):
	# count(10) --> 10 11 12 13 14 ...
	# count(2.5, 0.5) -> 2.5 3.0 3.5 ...
	n = start
	while True:
		yield n
		n += step

def shiftWin(listOfThree,indices):
	''' Purpose: Take indices of strings to shift between adjacent elements
		Input: 
			listOfThree = [str1,str2,str3]
				-- a list with three string elements
			indices - [[a,b],[c,d],[e,f]]
				-- a list of 3 lists, each with a pair of indices
			
		Output: 
			a list of three strings, with the characters from the first string from indices[0
				example listOfThree: ['hello','happy','world']
				example indices [[2,1],[3,1],[2,2]]
				
				out = ['hel','lohappywo','rld']
		
	'''
	newlist = []
	newlist.append(listOfThree[0][:indices[0][1]])
	newlist.append(listOfThree[0][indices[0][1]:]+listOfThree[1]+listOfThree[2][:indices[2][0]+1])
	newlist.append(listOfThree[2][indices[2][0]+1:])
	return newlist

#===============================================================================
# charindexFromSides method 
# 
# 
# INPUT: an iterable of strings output: a list of strings, with a shift in
# characters between a specified item of the list and its two neighbors 
#===============================================================================
def charindexFromSides(itemiterable,target,shiftLR,validSegmentsStr=validSegmentsStr): # of types (list/tuple,int,list/tuple
	'Purpose: to count target # of Valid Segments from right and left, and return the indices of them'
	# shiftLR --> the number of horizontal character positions to shift the left
	#	 & right boundaries of target window, as a tuple of (left,right)
#	import itertools
	
#	dicOfDics = {}
	myindex = []
	for i in range(target-1,target+2): #recall: range(start #, end #+1)
		uString = itemiterable[i]
		uStrLen = len(uString)
#		fromLeft=range(len(uString))
#		fromRight = list(reversed(fromLeft))
#		iterDict = {'left':fromLeft,'right':fromRight}
#		iterDict = {'left':{'start':0,'step':1},'right':{'start':uStrLen,'step':-1}}
		leftRight = [range(uStrLen),reversed(range(uStrLen))]  # counting from left (start at 0, increment 1; counting from right, start from index of last item, decrement 1 
		indices=[]
		for LorR in (0,1):
#			if i > target:
#				indextuple = tuple(fromLeft)
#			elif i < target:
#				indextuple = tuple(reversed(fromLeft))
			validSegCnt=0
#			for j in iterDict[dirxn]:
#			generatorObj = mycount(dirxn[0],dirxn[1])
			indexToReturn = None
			for j in leftRight[LorR]:
				if uString[j] in validSegmentsStr:
					validSegCnt += 1
					if (LorR==0 and validSegCnt > shiftLR[LorR]):
						indexToReturn = j-1
						break
					elif (LorR==1 and validSegCnt >= shiftLR[LorR]):
						indexToReturn = j
						break
				else: 'not a valid segment'
			if indexToReturn==None:
				indexToReturn=j
			indices.append(indexToReturn)
		myindex.append(indices)			
#		indices.append(getNumSegments(i))
		
	return myindex

# mkImage creates a new image object and creates an associated Draw object to be used in later steps
# returns a tuple of (image, draw) 
def mkImage(mode=myMode,size=imgSize,color=bgColor): # color can be string, lowercase, e.g. 'black'
	image  = Image.new(mode, size, color) # MODE (the first arg.) must be in ALL CAPS; e.g. "RGB"
	# Draw instance allows us to draw onto the image we have opened/created
	# -- any changes are made directly to the Image obj
	draw = ImageDraw.Draw(image)
	return (image, draw) 

def dim1Char(fontDict,useChar=u'ก'):
#	f=open('log','a')  #for debugging

	dim1CharDic = {}
	for key, val in fontDict.iteritems():
		dim1CharDic[key] = val.getsize(useChar)
#		f.write('dim1Char(fsize) = '+str(dim1CharDic)+'\n')  #for debugging
#	f.close()  # for debugging
	return dim1CharDic

def widthAdjust(last,current):
	''' Purpose of widthAdjust:
		
		When characters that are written in vertical orthographic position
		differ in size from the main line character, then their horizontal
		position will be mis-aligned. 
		
		This function returns the difference needed to correct the horizontal
		offset
	'''
	
	diff = int(last) - int(current)
	if diff > 0: 
		adjustAmt = diff/2
	else: 
		adjustAmt = 0
	outDict = {'diff':diff,'adjust':adjustAmt}
	return outDict


def writeFullText(textListObj, xStart, yStart,fontDict):
	image, draw = mkImage()
	
	dim1CharDic = dim1Char(fontDict)
	w1CharCurr = None   # width of one character at settings of current iteration of loop
	w1CharLast = None   # width of one character at settings from previous iteration of loop
	first = True
	for text, size, windowNum, color in textListObj.values:
		if len(text)>0:

			'Determine width of a single character with given font+size (assumes monospaced font)'
			w1CharCurr = dim1CharDic[size][0]
			
			'Find difference in width between current font+size and previous font+size'
			if not first:
				adjust = widthAdjust(w1CharLast,w1CharCurr)
				wAdjust = adjust['adjust']
			else: 
				wAdjust = 0
				first=False
#			f=open('log','a')  # for debugging
#			f.write('w1CharLast: '+str(w1CharLast)+'\tw1CharCurr: '+str(w1CharCurr)+'\tadj '+str(wAdjust)+'\n')  # for debugging

			textSizeTuple = fontDict[size].getsize(text)
			draw.text((xStart - wAdjust, (yStart-size*0.6)), text, font=fontDict[size], fill=color)
			if getNumSegments(text)>0:
				xStart += textSizeTuple[0]  # font.getsize(text) => (width,height)
	#			xStart += (size*0.6)*getNumSegments(text)
	#		print str(textSizeTuple)+"\t"+str(xStart)
			w1CharLast = w1CharCurr
#			f.close()  # for debugging
	return image

def writeMask(textListObj, xStart, yStart,fontDict,misSegment=False,masklinewidth=masklinewidth):
	'''
		writeMask method
		Purpose:
			In self-paced moving-window reading experiment,
			Make an image for each region in an item, drawing a mask for all but the current region.
		Arguments:
			textListObj: an object of class mkTextList (defined below)
			xStart & yStart: the starting xy reference point from which the top-left of the first character will be written
			fontDict: a dictionary of font objects indexed by the corresponding font sizes
			misSegment: Logical. 
			
	'''

	# Find the size of one character and set the starting y-coordinate for the mask line

	dim1CharDic = dim1Char(fontDict)
	sizes = fontDict.keys()
	biggestHeight = dim1CharDic[max(sizes)][1]
	lineheight = yStart + (biggestHeight * 2/3) 
		# 2/3 of height is based on estimating the proportion of the total vertical
		# font space that is occupied by the distance from top of where tone marks are
		# displayed down to base of neutral Vertical Orthagraphic position (base of
		# most consonants in Thai). This gets distorted for really small font sizes
		# and may need to be reduced to make the line in the same relative position as
		# the text


	# figure out total length of sentence and create complete mask

	textList = textListObj.values
	conditions = textListObj.conditions
	imgSubdir = textListObj.imgSubdir
	itemnum = textListObj.itemnum
	xcoords = []
	xNext=xStart  # xStart's original value (how it was defined in the function call)
	for k in range(len(textList)):
		text, size, windowNum, color = textList[k]
		if len(text)>0:
			textSizeTuple = fontDict[size].getsize(text)
			if getNumSegments(text)>0:  # If text has at least one grapheme in Vertical orthographic position = 0, then, increase starting xStart
				xNext = xStart + textSizeTuple[0] # font.getsize(text) => (width,height)
		xcoords.append((xStart,xNext))
		xStart = xNext  
	image, draw = mkImage()
	lineMin = xcoords[0][0]
	lineMax = xcoords[-1][1]
	draw.line([(lineMin, lineheight),(lineMax, lineheight)], fill=fgColor, width=masklinewidth)
	trialid = os.path.join(imgSubdir,imgSubdir + '_'+str(itemnum)+'_')  
	maskExt = 'mask'+imgExt
	image.save(trialid + maskExt,useImgType)
	
	
	# Individual Windows: draw partial mask and text at each window position.
	
	w1CharLast = None
	wAdjust = 0
	yNew = 0
	for m in range(textListObj.totalWindows):
		image, draw = mkImage()
#		text, size, windowNum, color = textList[m]
		first = True
		for p in range(len(textList)):
			text, size, windowNum, color = textList[p]

			'Determine width of a single character with given font+size (assumes monospaced font)'
			w1CharCurr = dim1CharDic[size][0]
			h1CharCurr = dim1CharDic[size][1]
			
			'Find difference in width between current font+size and previous font+size'
			if not first:
				adjust = widthAdjust(w1CharLast,w1CharCurr)
				wAdjust = adjust['adjust']
				if (text in ascenders) or (text in vowelsBelow):
#					hAdjust = biggestHeight - h1CharCurr
					yNew = round(float(2167)/float(3070) *(biggestHeight - h1CharCurr) + yStart)  # specific numbers based on inspection of glyph specifications in the font being used
				elif (text in vowelsAbove) or (text in toneMarksEtc):
					yNew = round(float(1067)/float(3070) *(biggestHeight - h1CharCurr) + yStart)
				else:
					yNew = yStart
					
			else:
				wAdjust = 0
				yNew = yStart
				first=False
			w1CharLast = w1CharCurr  # set w1CharLast to w1CharCurr (current) for next time in loop 

			# draw the text if current windowNum matches revealed windowNum for current image...
			if m==windowNum:
				draw.text((xcoords[p][0] - wAdjust, yNew), text, font=fontDict[size], fill=color)			
			# ... OR draw a line to serve as a mask if not the currently revealed window
			else:
				draw.line([(xcoords[p][0], lineheight),(xcoords[p][1], lineheight)], fill=color, width=3)
		outfile = trialid + 'win_' + str(m)+imgExt
		image.save(outfile,useImgType)
		
def writeFullGetCoords(textListObj, xStart, yStart,fontDict,misSegment=False,imgFilename=imgFilename,masklinewidth=masklinewidth):
	'''
		writeFullGetCoords method
		Purpose:
			Built from writeMask method as starting point.
			- Create image of full sentence with all manipulations, yet
			
			- Keep track of coordinates of where window (and masks) should be, and give
			those coordinates as output.
			
		Arguments:
			textListObj: an object of class mkTextList (defined below)
			xStart & yStart: the starting xy reference point from which the top-left of the first character will be written
			fontDict: a dictionary of font objects indexed by the corresponding font sizes
			misSegment: Logical. 
		
		Products & Output:
			1. create an image of the full sentence, using manipulations (if specified)

			2. return a tuple with the coordinates where masks would need to be created
			to create a self-paced moving-window reading experiment
	'''

	# Find the size of one character and set the starting y-coordinate for the mask line

	dim1CharDic = dim1Char(fontDict)
	sizes = fontDict.keys()
	biggestHeight = dim1CharDic[max(sizes)][1]
	lineheight = yStart + (biggestHeight * 2/3) 
		# 2/3 of height is based on estimating the proportion of the total vertical
		# font space that is occupied by the distance from top of where tone marks are
		# displayed down to base of neutral Vertical Orthagraphic position (base of
		# most consonants in Thai). This gets distorted for really small font sizes
		# and may need to be reduced to make the line in the same relative position as
		# the text


	# figure out total length of sentence and create complete mask

	textList = textListObj.values
	imgSubdir = textListObj.imgSubdir
	conditions = textListObj.conditions
	itemnum = textListObj.itemnum
	xcoords = []
	xNext=xStart  # xStart's original value (how it was defined in the function call)
	
	for k in range(len(textList)):
		text, size, windowNum, color = textList[k]
		if len(text)>0:
			textSizeTuple = fontDict[size].getsize(text)
			if getNumSegments(text)>0:  # If text has at least one grapheme in Vertical orthographic position = 0, then, increase starting xStart
				xNext = xStart + textSizeTuple[0] # font.getsize(text) => (width,height)
		xcoords.append((xStart,xNext))
		xStart = xNext  
	image, draw = mkImage()  # remove for writeFullGetCoords?
	lineMin = xcoords[0][0]
	lineMax = xcoords[-1][1]
	draw.line([(lineMin, lineheight),(lineMax, lineheight)], fill=fgColor, width=masklinewidth)
#	trialid = os.path.join(imgSubdir,conditions + '_'+str(itemnum))  
#	maskExt = '_mask'+imgExt
#	image.save(trialid + maskExt,useImgType)
	maskimgFile = os.path.join(os.path.dirname(imgFilename),'mask_' + os.path.basename(imgFilename))
	image.save(maskimgFile,useImgType)
	
	
	# Individual Windows: draw partial mask and text at each window position.
	
	w1CharLast = None
	wAdjust = 0
	yNew = 0
	image, draw = mkImage()
	
	prevWindowNum = None
	windowBoundaries = []
#	cntSameWindowNum = 0
	first = True
	for p in range(len(textList)):
		text, size, windowNum, color = textList[p]

		'Determine width of a single character with given font+size (assumes monospaced font)'
		w1CharCurr = dim1CharDic[size][0]
		h1CharCurr = dim1CharDic[size][1]
		
		'Find difference in width between current font+size and previous font+size'
		if not first:
			adjust = widthAdjust(w1CharLast,w1CharCurr)
			wAdjust = adjust['adjust']
			if (text in ascenders) or (text in vowelsBelow):
#					hAdjust = biggestHeight - h1CharCurr
				yNew = round(float(2167)/float(3070) *(biggestHeight - h1CharCurr) + yStart)  # specific numbers based on inspection of glyph specifications in the font being used
			elif (text in vowelsAbove) or (text in toneMarksEtc):
				yNew = round(float(1067)/float(3070) *(biggestHeight - h1CharCurr) + yStart)
			else:
				yNew = yStart
				
		else:
			wAdjust = 0
			yNew = yStart
			first=False
		w1CharLast = w1CharCurr  # set w1CharLast to w1CharCurr (current) for next time in loop 

		# If not the current window for image, or if draw the text
		
		draw.text((xcoords[p][0] - wAdjust, yNew), text, font=fontDict[size], fill=color)
		
		# If the previous window number and the current one are not the same, must
		# mean this is a new window, so record the coordinates for the output
		if not windowNum == prevWindowNum:
			windowBoundaries.append(xcoords[p][0])  # xcoords[p] is the current window's left & right (xmin & xmax) boundaries
													# going thru, add start coords of each window, then after looping add max coord overall as ending point of last window
#			if p >0:
#				windowBoundaries[-1].append(xcoords[p-1][1])
#			else:
#				windowBoundaries[-1].append(xcoords[p][1])
#			cntSameWindowNum = 0
#		elif cntSameWindowNum == 1:
#			
#			
#		cntSameWindowNum += 1 #increment for the next loop
		prevWindowNum = windowNum
	windowBoundaries.append(xcoords[-1][1]) 
	#maskimgFile = os.path.join(imgSubdir,conditions + '_'+str(itemnum)+'_sent'+imgExt)
	image.save(imgFilename,useImgType)
	return tuple(windowBoundaries)

def writeRegion(textListObj, xStart, yStart,fontDict,drawingObj):
	'''
		NOT CURRENTLY MAINTAINED OR USED!!!
	'''
	
	for text, size, windowNum, color in textListObj.values:
		if len(text)>0:
			textSizeTuple = fontDict[size].getsize(text)
			drawingObj.text((xStart, (yStart-size*0.6)), text, font=fontDict[size], fill=color)
			if getNumSegments(text)>0:
				xStart += textSizeTuple[0]  # font.getsize(text) => (width,height)
	#			width += (size*0.6)*getNumSegments(text)
	#		print str(textSizeTuple)+"\t"+str(width)



def genFont(size):
	return ImageFont.truetype(fontfile, size, encoding="unic")
	#return ImageFont.truetype("C:\WINDOWS\Fonts\ANGSA.TTF", size, encoding="unic")


def getNumSegments(text,validSegmentsStr=validSegmentsStr):
	numSegments = 0
#	validSegmentsStr = u"กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮะาเแโใไๅๆฯ฿๏๚๛๐๑๒๓๔๕๖๗๘๙" # a unicode string or a list of unicode strings specifying which characters to be counted
	for char in text:
		if char in validSegmentsStr:
			numSegments += 1
			
	return numSegments


def generateFontDict(sizeList):
	fontDict = {}
	for size in sizeList:
		fontDict[size] = genFont(size)
		
	return fontDict

def fixSaraAm(text):
	'For the ำ  /am/ character in Thai, separate the two images by encoding as the circle, any diacritics, and then /a/'
	# Possibly has a bug that inserts a mai-tho character
	
	import re, itertools
	saraAmPattern = ur'(['+vowelsAbove+toneMarksEtc+ur']*)'+u'\u0E33'+ur'(['+vowelsAbove+toneMarksEtc+ur']*)'   #with potential preceding vowels and/or other diacritics; u'' denotes unicode; r'' denotes raw string; ur'' combines the two
						# the unicode value \u0E33 represents Thai coda u'ำ'
	reSaraAm= re.compile(saraAmPattern, flags=re.UNICODE)
	found = reSaraAm.findall(text)  # assigns a list of all the matches to the groups
	found2 = itertools.chain(*found)  # flattens it into an iterable with just one level
	replaceText = u'\u0E4D'+''.join(found2)+u'\u0E32'
	replaced = reSaraAm.sub(replaceText,text)
	return replaced

def stims(fname,colid=u'Sentence'):  # colid is a key that refers to the sentence; by default, it will look for 'Sentence'
	'''
	stims function
	original built as separate module: stimparser.py
		Created on Aug 2, 2012; @author: Scott Hajek
	
	Purpose: to process input strings and separate them into lists based on delimiter characters
	Expected Input: 
		String, such as  u"ชาว/ล้านนา/มี/วิธี/การ/ทำ/(น้ำพริก)/หลาย/วิธี/ ซึ่ง/แตกต่าง/กัน/ไป/ตาม/ความ/นิยม/ของ/แต่/ละ/ท้องถิ่น"
		Encoding -> Thai (Unicode)
	#===============================================================================
	# stims function processes marked up sentence 
	#
	# sentence example = u"ชาว/ล้านนา/มี/วิธี/การ/ทำ/(น้ำพริก)/หลาย/วิธี/ ซึ่ง/แตกต่าง/กัน/ไป/ตาม/ความ/นิยม/ของ/แต่/ละ/ท้องถิ่น"
	# stims splits the sentence at each slash "/" juncture, and returns a dictionary with the following keys:
	#	'segments' : list of segments
	#	'tagged'	: list of indices for segments list for items that were originally tagged by being surrounded by parentheses '()'
	#===============================================================================

	Delimiters Expected:
	/ (slash) --> to separate words or regions in the text
	() parentheses --> to denote the region to undergo special manipulation; it becomes 'tagged'
	
	Output: an object which has following structure
		
		object
			list of lines
				dict of properties
					'Index' :  the index number specified in the input table (?)
					'segments' : list of segments (when split string in colid field by slashes '/' 
					'tagged'  :  a list of dictionaries of, one dict. for each tagged element in sentence (which were originally tagged by being surrounded by parentheses '()')
						[listindex]
							'text' : the text contained in the tagged element for this current index
							'window' : number index of the window it's contained in
							'startEnd' : tuple with the (starting, ending) character number of this tagged portion relative to the current window
					[values from the other fields in the input table, in the form of {'field' : value}]

		Example of accessing various elements
		
			myline = object[5]
			myline['segments'][0:8]	<-- gets segments 0 thru 8 of stimuli line 5 
			myline['tagged'][0]		<-- gets the index of the first (if any) segment in line 5 that was surrounded by parentheses ()
				
	'''
	import codecs,re #,unicodedata
	
	# read in file  (uses fname, as specified as first argument to stims function)
	f = codecs.open(fname, 'r','utf_8')
	
	lines = f.readlines()
	
	# Which column (zero-indexed) contains the delimited sentence?
	#colid = u'Sentence'  # needs to be specified in Unicode!!!!!
	table=list()
	#table = [line.split('\t') for line in lines]  #strip() might be useful here too
	head=lines[0].strip().split('\t')
	# start with index 1 (2nd row), because 1st row is header
	reParenthetical = re.compile(u'\(([^\)]+)\)', flags=re.UNICODE)
	for L in range(0,len(lines)):
		fields = lines[L].strip().split('\t')
		table.append(dict())
		for c in range(len(fields)):
			keyval = {head[c]:fields[c]}
			table[L].update(keyval)
		# purpose next 'if'? to make sure that the specified field to look for in 'colid' is actually in the input table? 
		if colid in table[L]: 
			fulltext = table[L][colid]
			
			# fixSaraAm, a func defined above, takes a certain character
			#  composed of two graphs but encoded as one, and splits it into the
			#  separate two encodings of its component parts
			fulltext = fixSaraAm(fulltext)
			chunks = {'segments':fulltext.split('/')}
			# identify which word(s) were tagged with parentheses '()'
			tagged = list()
			for s in range(len(chunks['segments'])):
				curritem = chunks['segments'][s]
				match = reParenthetical.search(curritem)
				if match:
					taggedtext = match.group(1)
					startEnd = (match.start(1)-1,match.end(1)-2)  # tuple with indices (relative to chunk) for start and end (assuming the parentheses aren't there
					chunks['segments'][s] = re.sub('[\(\)]','',curritem)   # delete parentheses
					tagged.append({'window':s,'text':taggedtext,'startEnd':startEnd})
			chunks.update({'tagged' : tagged})
			table[L].update(chunks)
	return table


class mkTextList:
	def __init__(self,segmentsList,taggedList,onlyChangeTagged=False,big=60,small=40,fgColor=fgColor,fgColorTagged=fgColorTagged):  # 'big' and 'small' are given default values, but new vals can be assigned when calling this function
		
		''' Create a List of window numbers that are tagged with parentheses '()'. '''
		
		windowNumsTagged = []
		for w in taggedList:
			windowNumsTagged.append(w['window'])
		#textList= tuple((k,small) for k in segmentsList)
		textList = []
			# windowNum keeps track of which window (or region) each string belongs to. 
			# Important when writing sub-parts of same region to image but doing so separately
		
		totalWindows = len(segmentsList)
		self.totalWindows = totalWindows
		
		
		# Cycle through each window. 
		# Can go letter-by-letter, using special (small) font size for only the characters in Vertical Orthographic Position
		# if onlyChangeTagged option is False, then go letter-by-letter for ALL text
		# if onlyChangeTagged option is True, then assign same size to all text in segment (window) 
		for windowNum in range(totalWindows):	
			# Choose text color for text depending on whether windows is tagged
			if windowNum in windowNumsTagged:
				fgColorNow = fgColorTagged
			else: fgColorNow = fgColor
			
			if (windowNum in windowNumsTagged) or not onlyChangeTagged:  # onlyChangeTagged is an optional argument, default=False
				for lttr in segmentsList[windowNum]:
					if lttr in charsToChangeSize:
						size = small
					else:
						size = big
					textList.append((lttr,size,windowNum,fgColorNow))
			else:
				size = big
				textList.append((segmentsList[windowNum],size,windowNum,fgColor))
		self.values = textList
		
		# textList ends up with the following kinds of data 
		#			 ((u"ปัจจุบ", big, 0), 
		#			 (u"\u0e31", small, 1), 
		#			 (u"นค", big, 2),
		#			 (u"\u0e31\u0e49", small, 2),  # if same window number, then will be presented in the same viewing period 
		#			 (u"นค\u0e31\u0e49", big, 3),
		#			 (u"น", big, 4),
		#			 (u"ไ", small, 5),
		#			 (u"ทย", big, 5))
	
def getUniqSizes(textList):
	sizesAll = []
	for (txt,size,windowNum,color) in textList:
		sizesAll.append(size)
	sizesUniq = set(sizesAll)
	return sizesUniq

def saveimg(image,imgtype=useImgType,extension=imgExt):
	# Get script filename
	scriptpath = inspect.getfile(inspect.currentframe()) # script filename (usually with path)
	# Get basename of script file
	scriptfilename = os.path.basename(scriptpath)
	# Get time/date of script 
	scriptdate = os.path.getmtime(scriptfilename)
	# Save as filename including script name with its date last modified
	imgfilename = scriptfilename.replace(".","_")+str(scriptdate)+extension 
	image.save(imgfilename, imgtype)
	return "Image saved as -> "+imgfilename+"\nin same directory as -> "+scriptpath



