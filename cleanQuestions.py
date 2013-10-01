'''
cleanQuestions.py

PURPOSE To parse comprehension questions and change specific aspects of the
character encoding and character order that aren't printing properly with PIL or
Experiment Builder

Created on Oct 27, 2012

@author: jsh
'''

import th2img, string, re, os, codecs, math

wrapAfter = 44


#===============================================================================
# Read in comprehension questions from stim file
#===============================================================================

projDir = '/Users/jsh/Dropbox/UIUC/Thai Reading/workspace/txt2img'

stimfile = os.path.join(projDir,'stimuli_Thai.txt')
#root = os.path.splitext(stimfile)[0] # splitext() returns (root,extension)

raw_stimfile = codecs.open(stimfile,'r','utf_8')
stimHeader = raw_stimfile.readline().strip().split('\t')

pieces = th2img.stims(stimfile,colid=u'question')

itemsiterator = range(1,len(pieces))  # 2nd arg in range() must be 1 greater than the last number wanted in the sequence 

# Open new List outfile connection
outPathList = os.path.join(projDir,'pracTargCoord_fixQuesAm.txt')
outList = open(outPathList,'w')
outList.write('\t'.join(stimHeader)+'\n')

quesList = []

for itemnum in itemsiterator:

	# Parse questions out of stimuli file
	questionMod1 = pieces[itemnum]['question']

	# remove spaces and parentheses
	questionMod1 = re.sub('[ ()]','',questionMod1)

	# Split Sara Am vowel into separate characters
	questionMod1 = th2img.fixSaraAm(questionMod1)

	# remove extra tone marker (mai thoo)
	questionMod1 = string.replace(questionMod1, u'\u0e49\u0e49', u'\u0e49')



	widthUnit=0
	questionMod2 = questionMod1
	insertions = 0
	
	# Add space Wrap text every 45 character widths

	#questionMod1='abcdefghijklmnopqrstuvwxyz'
	mypatt = r'[' + th2img.validSegmentsStr + r']'
	myiter = re.finditer(mypatt,questionMod1)
	mymat = [(m.group(), m.start()) for m in myiter]
	numWidthUnits = len(mymat)
	numWraps = int(math.floor((numWidthUnits -1) / wrapAfter))
	if numWraps >0:
		splitIDs=[0]
		qParts = []
		for w in range(numWraps): # +1, b/c range(a,b) goes from a to b-1
			splitID = mymat[(w+1) * wrapAfter][1]
			splitIDs.append(splitID)
			qParts.append(questionMod1[splitIDs[w]:(splitIDs[w+1])]) # in a mylist[x:y] construction, it includes indices from x up to (y-1)
		qParts.append(questionMod1[splitIDs[-1]:(len(questionMod1))])
		
		questionMod3 = '#'.join(qParts)
	else: 
		questionMod3 = questionMod1

#	for char in range(len(questionMod1)):
#		if questionMod1[char] in th2img.validSegmentsStr:
#			widthUnit += 1
#			if widthUnit == wrapAfter:
#				questionMod2


	questionFinal = questionMod3

	# append the current question to the output list & replace variable value of original data
	quesList.append(questionFinal)
	pieces[itemnum]['question'] = questionFinal
	
	listLine = [pieces[itemnum][h] for h in stimHeader]
	outList.write('\t'.join(listLine)+'\n')
	print 'finished item no. '+str(itemnum)

outList.close()

outPathQonly = os.path.join(projDir,'pracTargCoord_fixQuesAm_Qonly.txt')
outQonly = open(outPathQonly,'w')
outQonly.write('\n'.join(quesList))
outQonly.close()