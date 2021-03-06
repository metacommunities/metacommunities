library(jsonlite)
library(ggplot2)
library(dplyr)
j = stream_in(file('data/jobs.json'), flatten=TRUE)
colnames(j) 
s=round(sum(na.omit(as.numeric(j$statistics$totalBytesProcessed)))/1e12, 1)
print(s)

bytes = as.numeric(j$statistics$totalBytesProcessed)
dates = as.Date(as.POSIXct(as.numeric(j$statistics$creationTime)/1000, origin="1970-01-01"))
df= data.frame(date = dates, vol = bytes)
ggplot(df, aes(x=date, y=vol)) + geom_point(alpha=0.6, position='dodge')
gbday = df %>% na.omit  %>% arrange((date))  %>% group_by(date) %>% summarize(job_count = n(), gbday = cumsum(vol/1e9))
head(gbday)
dl = data.frame(x = as.Date('2016-07-31'), y =80000, labs = paste(as.character(s), 'terabytes')) 
ggplot(gbday, aes(x=as.Date(date), y=gbday)) + geom_line()  + ggtitle('Gigabytes/day on BigQuery jobs') + ylab('Gb of data (cumulative)')
as.character(s)
g + geom_text(data=dl, aes(x=x, y=y, label=labs, group=NULL))
df2 <- gbday %>% group_by(date) %>% arrange(date) %>% summarize(jobs = n())
ggplot(df2, aes(x=date, y=jobs, size=jobs)) + geom_point(position='dodge') +  scale_y_log10()
