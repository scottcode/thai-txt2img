'''
Created on Aug 18, 2012

@author: USER
'''


import re, glob, os

def renamer(files, pattern, replacement):
    for pathname in glob.glob(files):
        basename= os.path.basename(pathname)
        dirname = os.path.dirname(pathname)
        new_basename= re.sub(pattern, replacement, basename)
        new_pathname= os.path.join(dirname,new_basename)
        if new_pathname != pathname:
            os.rename(pathname, new_pathname)
            
#os.chdir(r'D:\Docs-D\Dropbox\UIUC\Thai Reading\workspace\txt2img\shrunk_60_40')
#
#files = '*.jpg'
##renamer(files,'^[^_]+_[^_]+_[^_]+_','')
#renamer(files,'(\.jpg)','_shrunk_.jpg')

#os.chdir(r'C:\Documents and Settings\USER\Desktop\thaiSPR1_stims\words_sentences3_expbuilderList_noNumerals_60-60_noMisSeg_3072x2304px')

#files = '*.jpg'
#namePattern = r'words_sentences3_expbuilderList_noNumerals_([0-9]{1,3})_(mask|win_)([0-9]{1,3}|).jpg'
#fullPathPattern = os.path.join(os.getcwd(),namePattern)
#replaceWith = r'thaiSPR1_LN_misSeg0_shrunkV0_item\1_win\3.jpg'
#renamer(files,namePattern,replaceWith)

# Create a dictionary for the old file and the new file (with list assigned) names

# glob 
parentDir = r'D:\Docs-D\Dropbox\UIUC\Thai Reading\workspace\txt2img\combined_2012_10_12_1624'
files = os.path.normpath(os.path.join(parentDir,'*.png'))
#namePattern = r'words_sentences3_expbuilderList_noNumerals_([0-9]{1,3})_(mask|win_)([0-9]{1,3}|).jpg'
namePattern = r'(.+)_(\d{1,3})(_sent.png)'

#fullPathPattern = os.path.join(os.getcwd(),namePattern)
#replaceWith = r'thaiSPR1_LN_misSeg1_shrunkV1_item\1_win\3.jpg'
replaceWith = r'item_\2_\1\3'
renamer(files,namePattern,replaceWith)


#renamer(files,'(\.jpg)','_normal.jpg')

