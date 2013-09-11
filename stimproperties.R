# Read in stim list, get unique item numbers, and query properties of them


require(stringr)
require(Unicode)
require(plyr)

validSegmentsStr = "[กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮะาเแโใไๅๆฯ฿๏๚๛๐๑๒๓๔๕๖๗๘๙.1234567890 ]"

mydir= "/Users/jsh/Dropbox/UIUC/Thai Reading/workspace/txt2img"
file = "pracTargCoord_fixQuesAm_spell_mergFixQs6.txt"

mypath <- file.path(mydir,file)

sents <- read.delim(mypath,quote="",encoding="UTF-8")
sentsNormal <- sents[sents$List==1 & sents$itemID<900,]  #sents$X.condition=="MH" & 
summary(sents)
names(sents)

#with(sents,Width[Width<80])

attach(sentsNormal)

# Determine the width in horizontal orthographic units (counting valid segments that force more horizontal space to be used)
widths <- sapply(X.Sentence,function(w) {
	ans <- gregexpr(validSegmentsStr,w)
	return(length(ans[[1]]))
})


# Distribution of distances from beginning and end of sentence


# strsplit(enc2utf8("สหดกข/าสวฟ/าดกาหฟส/ดกหฟ 121/กดกหฟ"),"/")
# strsplit("สหดกข/าสวฟ/าดกาหฟส/ดกหฟ 121/กดกหฟ","/")

segs <- sapply(X.Sentence,function(x) strsplit(as.character(x),"/"))

lengths <- sapply(segs,length)

targs <- sapply(segs,function(x) grep("\\(",x))
#junk <- matrix(as.numeric(targs),nrow=length(targs))
targs <- as.numeric(targs)

table(targs)
hist(targs)

# number of words between targets and end of sentence
fromEnd <- lengths - targs #+ matrix(1,length(targs),1)

hist(fromEnd)
table(fromEnd)


detach(sentsNormal)