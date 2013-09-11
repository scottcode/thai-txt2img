'''
ebList3.py

Purpose: 
To properly sort a series of files based on aspects of the filenames,
and to return a tab-delimited set with info from the filenames as fields, as
well as the list of files.

What's New?
 - since ebList1 & 2: vers. 3 is for lists that have just one image file per trial

Created on Oct 6, 2012

@author: scott hajek
'''
import re, os, glob#, string

parent = r'D:\Docs-D\Dropbox\UIUC\Thai Reading\workspace\txt2img'
filePattern = r'words_sentences3_expbuilderList_noNumerals_misSeg-*\*.jpg'
pathPattern = os.path.join(parent,filePattern)
picList = glob.glob(pathPattern)

'''picList = ["simple.0.0.jpg", "simple.0.1.jpg", "simple.0.10.jpg",
"simple.0.11.jpg", "simple.0.2.jpg", "simple.0.3.jpg", "simple.0.4.jpg",
"simple.0.5.jpg", "simple.0.6.jpg", "simple.0.7.jpg", "simple.0.8.jpg",
"simple.0.9.jpg", "simple.1.0.jpg", "simple.1.1.jpg", "simple.1.10.jpg",
"simple.1.11.jpg", "simple.1.2.jpg", "simple.1.3.jpg", "simple.1.4.jpg",
"simple.1.5.jpg", "simple.1.6.jpg", "simple.1.7.jpg", "simple.1.8.jpg",
"simple.1.9.jpg", "simple.2.0.jpg", "simple.2.1.jpg", "simple.2.10.jpg",
"simple.2.11.jpg", "simple.2.2.jpg", "simple.2.3.jpg", "simple.2.4.jpg",
"simple.2.5.jpg", "simple.2.6.jpg", "simple.2.7.jpg", "simple.2.8.jpg",
"simple.2.9.jpg", "simple.3.0.jpg", "simple.3.1.jpg", "simple.3.10.jpg",
"simple.3.11.jpg", "simple.3.2.jpg", "simple.3.3.jpg", "simple.3.4.jpg",
"simple.3.5.jpg", "simple.3.6.jpg", "simple.3.7.jpg", "simple.3.8.jpg",
"simple.3.9.jpg", "simple.4.0.jpg", "simple.4.1.jpg", "simple.4.10.jpg",
"simple.4.11.jpg", "simple.4.2.jpg", "simple.4.3.jpg", "simple.4.4.jpg",
"simple.4.5.jpg", "simple.4.6.jpg", "simple.4.7.jpg", "simple.4.8.jpg",
"simple.4.9.jpg"]'''


#===============================================================================
# It would be helpful to build the sequencing function separately
# 
# 
'''
	Input: a list of tuples with length 2. 
		[(a1,b1),
		 (a1,b2),
		 (a1,b3),
		 (a2,b1),
		 (a2,b2),
		 (a2,b3),
		 (a2,b4),
		 ...	]
	
	The first item in each tuple represents a grouping variable
	The second item is the window number
	
	Output:
	- when grouped based on the first item (trialID), you get a sequence of windows
	- include mention of start & end indices relative to original matrix
	
		[ [a1,[b1,b2,b3] ],
		  [a2,[b1,b2,b3,b4] ],
		  ...
		] 
	
'''

'Not using groupWindows for this version of ebList'
#def groupWindows(trialAndWindows):   # trialAndWindows must be a 
#	grouped = [[[]]] # declare triple-embedded list, size 1 by 1 by zero
#	for gw in range(len(trialAndWindows)):
#		oneTuple = trialAndWindows[gw]
#		if len(grouped[-1])==1:
#			grouped[-1].insert(0,oneTuple[0])
#		if grouped[-1][0]==oneTuple[0]:  # if it isn't the first iteration AND if the current and last trialnums match...
#			grouped[-1][1].append(oneTuple[1])
#	return grouped
#===============================================================================



# Define patterns based one which to split the strings 
splitAlpha = '[_a-zA-Z.]+'  # pattern to split based on alpha characters, leaving numbers
splitNum = '[_0-9]+'  # pattern to split based on number characters, leaving alpha characters



# Loop through each pathname 

# declare list variables before loop
listOfNums = []
numbrToNames = {}  # Dictionary that will have the numbers lists as keys and filenames as values
listOfAlphas = []
for i in range(len(picList)):
	base = os.path.basename(picList[i])
	#stripBase = base.strip(splitAlpha)
	alphas = re.split(splitNum,base)
	listOfAlphas.append(alphas)
	nums = re.split(splitAlpha,base)
	listOfNums.append([i]) # put index of original picList as first element in each list
	for j in range(len(nums)):
		if nums[j]=='':
			'do nothing '
		else:
#			if not re.search('[^0-9]', nums[j]): 
#				nums[j]=int(nums[j])
			listOfNums[i].append(int(nums[j]))
	numbrToNames.update({str(listOfNums[i]) : picList[i]})

# trials labeled as 'mask' didn't have a window number and therefore listOfNums was one element short for the mask of every trial.
# Fill out those lists to be of length 7
for L2 in listOfNums:
	if len(L2)==6:
		dicKey = str(L2)
		L2.append(None)
		numbrToNames[str(L2)] = numbrToNames[dicKey]

from itertools import groupby
from operator import itemgetter

numSort = sorted(listOfNums,key=itemgetter(2)) # sort by list number

groupByCounterbal = []
counterbalUniqKey = []
for k, g in groupby(numSort, itemgetter(2)):
	groupByCounterbal.append(list(g)) # store group iterator as list
	counterbalUniqKey.append(k)


# Now that the items are grouped by Counterbalancing, 
# go back through within each counterbalancing and group by trial
groupByTrial = []
trialUniqKey = []
for cntrbal in range(len(groupByCounterbal)):
	cntrbalSort = sorted(groupByCounterbal[cntrbal],key=itemgetter(5))  # sort by trial number
	groupByTrial.append([])
	trialUniqKey.append([])
	for k, g in groupby(cntrbalSort,itemgetter(5)):
		groupByTrial[cntrbal].append(list(g))
		trialUniqKey[cntrbal].append(k)


#===============================================================================
# SORT & CREATE DATA SOURCE with ONE TRIAL PER LINE
#------------------------------------------------------------------------------ 
# Go back through structure and sort the order of the windows within each trial
# Also, CREATE OUTPUT to be used as DATA SOURCE for Experiment Builder
# Needs to include List#, Trial#, misSeg (logical), shrunkVowel (logical)
#===============================================================================
ebBasename = 'ebList'
ebExtension = '.txt'
headerIndiv=['lst+1','trial+1','misSegVal','shrunkV','windowNum','winBasename']
for lst in range(len(groupByTrial)):
	groupedFname = ''.join([ebBasename,'_grouped_',str(lst+1),ebExtension])
	groupedPath = os.path.join(parent,groupedFname)
	groupedFile = open(groupedPath,'w')
	indivFname = ''.join([ebBasename,'_1perLine_',str(lst+1),ebExtension])
	indivPath = os.path.join(parent,indivFname)
	indivFile = open(indivPath,'w')
	headerIndivStr = '\t'.join(headerIndiv)+'\n'
	indivFile.write(headerIndivStr)
	for trial in range(len(groupByTrial[lst])):
		groupByTrial[lst][trial] = sorted(groupByTrial[lst][trial],key=itemgetter(6))
		# reminder:
		#	at this point, the structure of the data groupByTrial is:
		#	[List level
		#		[Trial Level
		#			[originalOrderIndex,experNumber,ListNum,misSeg,shrunkV,item,window],
		#			...
		#		],
		#		...
		#	]
		misSegVal = groupByTrial[lst][trial][0][3]  # the 4th item in a window list tells if misSegmented (if =1) 
		shrunkV = groupByTrial[lst][trial][0][4]  # the 5th item in a window list tells if the vowels have been shrunk (if =1)
		trialInfo = [str(lst+1),str(trial+1),str(misSegVal),str(shrunkV)]  # add one to indices to make 1-indexed instead of zero
		trialString = '\t'.join(trialInfo)
		groupedFile.write(trialString)
		groupedFile.write('\t')
		windows = []
		for windowNum in range(len(groupByTrial[lst][trial])):
			window = groupByTrial[lst][trial][windowNum]
			winBasename = os.path.basename(numbrToNames[str(window)]) #use dictionary to look up filenames
			windows.append(winBasename)
			#stringList4indivFile = [trialString,str(windowNum+1),'\"'+winBasename+'\"']
			hValues = []
			for h in headerIndiv:
				hValues.append(eval(h))
				if type(hValues[-1]) is str:
					hValues[-1]='\"'+hValues[-1]+'\"'
				else:
					hValues[-1]=str(hValues[-1])
			joinedString4indivFile='\t'.join(hValues)
#			joinedString4indivFile = '\t'.join(stringList4indivFile)
			indivFile.write(joinedString4indivFile)
			indivFile.write('\n')
		windowsString = ','.join(windows)
		groupedFile.write('[')
		groupedFile.write(windowsString)
		groupedFile.write(']\n')
	groupedFile.close()

