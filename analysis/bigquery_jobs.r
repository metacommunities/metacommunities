library(jsonlite)
library(ggplot2)
j = stream_in(file('../test.json'), flatten=TRUE)
s=sum(na.omit(as.numeric(j$statistics$totalBytesProcessed)))/1e12
print(s)

bytes = as.numeric(j$statistics$totalBytesProcessed)
dates = as.Date(as.POSIXct(as.numeric(j$statistics$creationTime)/1000, origin="1970-01-01"))
df= data.frame(date = dates, vol = bytes)
dim(df)
#ggplot(df, aes(x=date, y=vol)) + geom_bar(stat='identity')
ggplot(df, aes(x=date, y=vol)) + geom_point(position='dodge')
