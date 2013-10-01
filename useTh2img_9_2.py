# coding: utf-8

'''
script to call th2imgX_Y.py module. 
Primary Version number of th2img and useTh2img now correspond to one another,
however, subversion numbers are independent 

useTh2img_9_2 being used with th2img9_2 on 2012-11-12
	- embedded font size and misSeg into the loop
useTh2img_9_1 being used with th2img9_1 on 2012-10-12
useTh2img_9_0 being used with th2img9_1 on 2012-10-05

Created on Aug 18, 2012

@author: Scott Hajek
'''

# Modules to import
import os, time, th2img
#from itertools import chain

initialX = 5
initialY = 20

## Set working directory
#os.chdir(r'D:\Docs-D\Dropbox\UIUC\Thai Reading\workspace\txt2img')

stimfile = 'stimuli_Thai.txt'
root = os.path.splitext(stimfile)[0] # splitext() returns (root,extension)
mytime = time.strftime('%Y-%m-%d_%H%Mh')
imgSubdir = unicode(root+'_' + mytime) #+conditions
try:
	os.mkdir(imgSubdir)
except OSError:
	'Directory already exists'
pieces = th2img.stims(stimfile,colid=u'$Sentence')

# Specify file to be used for window boundary coordinates
coordsFilename = imgSubdir + '.txt'
coordsFile = open(os.path.join(imgSubdir,coordsFilename),'w')
coordsFile.write('itemnum\tbigSize\tsmallSize\tmisSegment\txCoords_for_windowBoundaries\n')

itemsiterator = range(1,len(pieces))  # 2nd arg in range() must be 1 greater than the last number wanted in the sequence 

for itemnum in itemsiterator:
	# Shift windows to create mis-segmented effect?
	misSegment = pieces[itemnum]['misSeg'] == u'True'  # value must be Logical (True/False)
	myBig = int(pieces[itemnum]['bigSize'])
	mySmall = int(pieces[itemnum]['smallSize'])
	conditions = 'misSeg-'+str(misSegment)+'_sizes_'+str(myBig)+'-'+str(mySmall)

	
	print 'Creating item number '+str(itemnum)+' of '+str(itemsiterator[-1])
	segmentsList = pieces[itemnum]['segments']
	taggedList = pieces[itemnum]['tagged']
	if misSegment:  # misSegment is a logical value (True/False)
		for tag in taggedList:  # For now, works if there's just one tagged window. If more, won't work.
			target = tag['window']
			indicesToShift = th2img.charindexFromSides(segmentsList,target,shiftLR=(1,1)) # shiftLR tells how many horizontal units to shift the target window vs adjacent windows (left side, right side)
			targetAndNeighbors = segmentsList[target-1:target+2]  #index range goes from [start,next index after stopping index]
			newTargetAndNeighbors = th2img.shiftWin(targetAndNeighbors,indicesToShift)
			segmentsList[target-1:target+2] = newTargetAndNeighbors
		try:
			segmentsList.remove('')
			segmentsList.remove('')
		except ValueError:
			'segmentsList did not have empty elements after shifting windows'
	
	textList = th2img.mkTextList(segmentsList,taggedList,big=myBig,small=mySmall)
	setattr(textList,'imgSubdir',imgSubdir)
	setattr(textList,'conditions',conditions)
	setattr(textList,'itemnum',itemnum)
	#print textList.root+str(textList.itemnum)
	
	sizesUniq = th2img.getUniqSizes(textList.values)
	fontDict = th2img.generateFontDict(sizesUniq)
	
	currImgFilename = pieces[itemnum]['$sentImg']
	currImgPath = os.path.join(imgSubdir,currImgFilename)
	#image = th2img.writeFullText(textList, 100, 100,fontDict)
	#image.save('itemCtr_'+str(itemnum)+'.jpg', "JPEG")
	windowBounds = th2img.writeFullGetCoords(textList, initialX, initialY,fontDict,imgFilename=currImgPath)  # args: (textList, start x-coord, start y-coord, fontdict,optional_image_output_path)
	
	#coordSet=[]
	#for b in range(len(windowBounds)):
	coordsStr = [str(x) for x in windowBounds]  # turn each item into a string using a List comprehension
	coordLine = '['+','.join(coordsStr)+']'
		#coordsFile.write(coordSet+'\t')
	coordLineLabeled = '\t'.join([str(pieces[itemnum]['itemID']),str(myBig),str(mySmall),str(misSegment),coordLine])
	coordsFile.write(coordLineLabeled + '\n')
coordsFile.close()