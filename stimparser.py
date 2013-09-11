moduleInfo = '''
stimparser.py

Purpose: to process input strings and separate them into lists based on delimiter characters
Encoding of Input: expected to be Thai (Unicode)

Delimiters Expected:
/ (slash) --> to separate words or regions in the text
() parentheses --> to 

Created on Aug 2, 2012

@author: Scott Hajek
'''
def stims(fname,colid=u'Sentence'):
    import codecs,re #,unicodedata
    
    # read in file
    f = codecs.open(fname, 'r','utf_16')
    
    lines = f.readlines()
    
    # Which column (zero-indexed) contains the delimited sentence?
    #colid = u'Sentence'  # needs to be specified in Unicode!!!!!
    table=list()
    #table = [line.split('\t') for line in lines]  #strip() might be useful here too
    head=lines[0].strip().split('\t')
    # start with index 1 (2nd row), because 1st row is header
    openparen = re.compile('\(', flags=re.UNICODE)
    closeparen = re.compile('\)', flags=re.UNICODE)
    for L in range(0,len(lines)):
        fields = lines[L].strip().split('\t')
        table.append(dict())
        for c in range(len(fields)):
            keyval = {head[c]:fields[c]}
            table[L].update(keyval)
        if colid in table[L]: 
            table[L][colid] = openparen.sub('/(',table[L][colid])
            table[L][colid] = closeparen.sub(')/',table[L][colid])
            chunks = {'segments':table[L][colid].split('/')}
            # identify which word(s) were tagged with parentheses '()'
            tagged = list()
            for s in range(len(chunks['segments'])):
                curritem = chunks['segments'][s]
                if curritem.startswith('('):
                    curritem = re.sub('[\(\)]','',curritem)
                    tagged.append(s)
            chunks.update({'tagged' : tagged})
            table[L].update(chunks)
    return table

