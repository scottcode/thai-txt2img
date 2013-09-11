require(stringr)

#dir = "D:/Docs-D/Dropbox/UIUC/Thai Reading/workspace/txt2img"
dir = '~/Dropbox/UIUC/Thai Reading/workspace/txt2img'
setwd(dir)

# =====================
# CREATE COUNTERBALANCING SCHEME
#	using the itemnumbers that i'll actually be using
# ----------------------

conxn <- file("sentsWidthLess83.txt","r")
lines <-readLines(conxn)
#close(cnxn)  # not necessary(?)

items <- str_split(lines, " ")
items <- sapply(items,strtoi)
bal <- data.frame(items)

cond <- c("mh","MH","mH","Mh")
# m --> missegmented
# h --> shrunk
# capital letters denote NOT the condition (i.e. M=normal segmented, H=notShrunk

indices <- 1:length(items)

randInd <- sample(indices) # get random permutation of indices
quarters <- c(0,length(items)/4,length(items)/2,length(items)*3/4,length(items))

bal$L1 <- NA
bal$L2 <- NA
bal$L3 <- NA
bal$L4 <- NA

for(count in 1:4){
	
	IDs <- randInd[(quarters[count]+1):quarters[count+1]]
	
	bal$L1[IDs] = cond[(1+count) %% 4 + 1]
	bal$L2[IDs] = cond[(2+count) %% 4 + 1]
	bal$L3[IDs] = cond[(3+count) %% 4 + 1]
	bal$L4[IDs] = cond[(4+count) %% 4 + 1]
}

bal2 <- data.frame("itemnum"=rep(items,4),"list"=c(rep(1,length(items)),rep(2,length(items)),rep(3,length(items)),rep(4,length(items))))

bal2$condition <- with(bal,c(L1,L2,L3,L4))

# code missegmented variable
bal2$misSegment <- sapply(bal2$condition, function(x) substr(x,1,1)=="m")

# code whether Vowel shrunk condition
bal2$shrunk <- sapply(bal2$condition, function(x) substr(x,2,2)=="h")

# code the small size {25,50}
bal2$smallSize <- (bal2$shrunk * -25) + 50  # a number times a logical is the number (if L=TRUE) or zero (if L=FALSE)

# test random sample of rows
bal2[sample(1:dim(bal2)[1],10),]



# ========================
# ADD COORDINATES
# 	Read in info about the coordinates & merge with existing list
# -------------------------

coordFiles <- Sys.glob("*_50*/*_50*.txt")

first = TRUE
for (file in coordFiles) {
	tmpCoords <- read.delim(file,quote="",colClasses=c(rep('factor',3),'logical','character'))
	if(first){
		catcoords <- tmpCoords
		first=FALSE
	}else{
		catcoords <- merge(catcoords,tmpCoords,all=TRUE)
	}
}



bal3 <- merge(bal2,catcoords,by=c("itemnum","misSegment","smallSize"))

# test random sample of rows
bal3[sample(1:dim(bal3)[1],10),]

# =======================================
# ADD PICTURE FILENAMES
# -----------------------------------

imglist <- Sys.glob('combined*1624/*.png')
#imglist[1:10]
imginfo <- data.frame(imglist)

summary(imginfo)

# calculate variable of ONLY the filename (not including any part of the path)
imginfo$imgnames <- as.factor(sapply(imginfo$imglist,function(x) sub('.+/','',x)))

# get item#, shrunk(T/F), bigSize,smallSize
item_size <- sapply(imginfo$imgnames,function(x) str_match_all(x,'([0-9]+)'))

imginfo$itemnum <- as.factor(sapply(item_size,function(x) x[1,2]))
imginfo$bigSize <- as.factor(sapply(item_size,function(x) x[2,2]))
imginfo$smallSize <- as.factor(sapply(item_size,function(x) x[3,2]))

#summary(imginfo)
#imginfo[,2:length(imginfo)]

# counterbalancing with coordinates AND filenames
balCrdNam <- merge(bal3,imginfo)
dim(balCrdNam)
# Did the right number of specs get assigned to each unique list-condition set?
xtabs(~ list + shrunk + misSegment,data=balCrdNam)

#random sampling of rows, excluding cols 'imglist' 'sCoords...'
#balCrdNam[sample(1:dim(balCrdNam)[1],10),names(balCrdNam)[!(names(balCrdNam) %in% c('imglist','xCoords_for_windowBoundaries'))]]

# re-order columns and get rid of the one that includes parent directory name (imglist)
fieldOrder <- c('list','itemnum','condition','shrunk','bigSize','smallSize','misSegment','xCoords_for_windowBoundaries','imgnames')

balCrdNam <- balCrdNam[,fieldOrder]

# sort row order based on list and item#
balCrdNam <- with(balCrdNam,balCrdNam[order(list,itemnum),])


#==========================
# ADD COMPREHENSION ?s, ETC
#--------------------------

rawstim <- read.delim('words_sentences3_expbuilderList_noNumerals.txt',encoding='UTF-8')


# remove a few unnecessary fields
fieldsRawStim <- names(rawstim)
dropFields <- c("SourceURL",'Modified','SentNoMarkup','Onset')

rawstim <- rawstim[,!is.element(fieldsRawStim,dropFields)]

# Merge item additional item information (incl. compreh. ?s) with counterbalanced list
names(balCrdNam)
names(rawstim)

balCrdNamQues <- merge(balCrdNam,rawstim,by.x=c('itemnum'),by.y=c('Index'))


write.table(balCrdNamQues,file='listCoordNamesQues.dat',sep="\t",row.names=FALSE)#,fileEncoding='UTF-8')



