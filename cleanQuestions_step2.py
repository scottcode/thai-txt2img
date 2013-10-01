'''
cleanQuestions_step2.py

PURPOSE 
To merge hand-corrected questions back into parameter file.

Created on Oct 30, 2012

@author: jsh
'''

import th2img, os, codecs

#wrapAfter = 44


#===============================================================================
# Read in comprehension questions from stim file
#===============================================================================

projDir = '/Users/jsh/Dropbox/UIUC/Thai Reading/workspace/txt2img'

quesFixedPath = os.path.join(projDir,'stimuli_Thai.txt')
quesFixedFile = codecs.open(quesFixedPath,'r','utf_8')
quesFixed = quesFixedFile.readlines()
quesFixed = [Qitem.strip() for Qitem in quesFixed ]

paramTablePath = os.path.join(projDir,'pracTargCoord_fixQuesAm_spell.txt')
paramTableFile = codecs.open(paramTablePath,'r','utf_8')
paramHeader = paramTableFile.readline().strip().split('\t')

pieces = th2img.stims(paramTablePath,colid=u'question')

itemsiterator = range(1,len(pieces))  # 2nd arg in range() must be 1 greater than the last number wanted in the sequence 

# Open new List outfile connection
outPathList = os.path.join(projDir,'pracTargCoord_fixQuesAm_spell_mergFixQs.txt')
outList = open(outPathList,'w')
outList.write('\t'.join(paramHeader)+'\n')

#quesList = []

for itemnum in itemsiterator:
	
	pieces[itemnum]['question'] = quesFixed[itemnum-1]  #quesFixed has no header and thus 1 fewer element, so must subtract 1
	
	listLine = [pieces[itemnum][h] for h in paramHeader]
	outList.write('\t'.join(listLine)+'\n')
	print 'finished item no. '+str(itemnum)

outList.close()

#outPathQonly = os.path.join(projDir,'pracTargCoord_fixQuesAm_Qonly.txt')
#outQonly = open(outPathQonly,'w')
#outQonly.write('\n'.join(quesList))
#outQonly.close()