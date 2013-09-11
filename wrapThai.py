import th2img9_1, string, re, os, codecs, math

th2img= th2img9_1

questionMod1=u''

wrapAfter = 44
delimChar= u'#'

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
        
        questionMod3 = delimChar.join(qParts)
else: 
        questionMod3 = questionMod1

print questionMod3
print 'Length without delims: ' + str(len(questionMod3)-(len(qParts)-1))
print 'Number of Lines: '+str(len(qParts))
