require(stringr)

dir = "D:/Docs-D/Dropbox/UIUC/Thai Reading/workspace/txt2img"
setwd(dir)


# =======================
#	SECTION 1
# =======================

list <- read.delim("listWithBounds50-25.txt",header=TRUE)
list$misSeg <- sapply(list$misSegment,function(x) {if(x=="False") 0 else 1})
list$itemID <- list$itemnum

# check for correctness of transformation
list[,c('misSegment','misSeg')]

summary(list); names(list)


assignment <- read.delim("list_assignment.txt",header=TRUE)

# Do itemID, misSeg, and smallSize fields match? yes
names(list)[names(list) %in% names(assignment)]

listAssigned <- merge(list,assignment)

# make file names specific to the sentence images
listAssigned <- transform(listAssigned,sentImg = str_join(nameAs,"sent.jpg"))

summary(listAssigned)
names(listAssigned)

# columns to keep
keepCols <- c('List','itemID','counterbal_index','misSeg','shrunk','bigSize','smallSize','sentImg','xCoords_for_windowBoundaries')

listSlim <- listAssigned[,keepCols]
listSlim <- with(listSlim, listSlim[order(List,itemID),])
summary(listSlim)

write.table(listSlim,file="listWithBounds_Assigned.dat",sep="\t",row.names=FALSE)


# =======================
#	SECTION 2
# =======================

require(stringr)

dir = "D:/Docs-D/Dropbox/UIUC/Thai Reading/workspace/txt2img"
setwd(dir)

list2 <- read.delim('listWithBounds50-25_final.txt',header=TRUE,colClasses=c(rep('factor',4),'logical','character'))
summary(list2)

imglist <- Sys.glob('*COMBINED/*.png')
#imglist[1:10]
imginfo <- data.frame(imglist)

summary(imginfo)

#imginfo$misSeg <- sapply(list$misSegment,function(x) {if(x=="False") 0 else 1})

# stringr::str_match(string,pattern)

# Get list number
matches <- with(imginfo,str_match(imglist,'L_([1234])_'))
imginfo$list <- as.factor(matches[,2]); rm(matches)

# Get Item number
matches <- with(imginfo,str_match(imglist,'item_([0-9]{1,3})_'))
imginfo$itemnum <- as.factor(matches[,2]); rm(matches)

# Get misSegmented Logical value
matches <- with(imginfo,str_match(imglist,'misSeg_([01])_'))
misSegInfo <- matches[,2]; rm(matches)
imginfo$misSegment <- misSegInfo==1
# misSegment <- sapply(misSegment,function(x) paste(substr(x,1,1),tolower(substr(x,2,nchar(x))),sep=""))
#imginfo$misSegment <- misSegment

# Get bigSize
matches <- with(imginfo,str_match(imglist,'cSize_([0-9]+)_'))
imginfo$bigSize <- as.factor(matches[,2]); rm(matches)

# Get smallSize
matches <- with(imginfo,str_match(imglist,'vSize_([0-9]+)_'))
imginfo$smallSize <- as.factor(matches[,2]); rm(matches)

# Calculate Logical variable for whether vertical vowels are shrunk
imginfo$shrunk <- imginfo$smallSize=="25"

# Sort the order of both data frames
list2 <- with(list2,list2[order(list,itemnum),])
imginfo <- with(imginfo,imginfo[order(list,itemnum),])

testmerge <- merge(list2,imginfo,by=c('list','itemnum'),sort=FALSE)

write.table(list2,file='list2.tmp')
write.table(imginfo,file='imginfo.tmp')