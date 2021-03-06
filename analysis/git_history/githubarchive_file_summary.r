library(ggplot2)
library(stringr)
fs = sapply(dir(), file.size)
file_date = str_replace(names(fs), '\\.json\\.gz', '')
datetimes = strptime(file_date, '%Y-%m-%d-%H')
day_of_week = strftime(datetimes, '%w')
weekend = day_of_week==0 | day_of_week == 6
df = data.frame(date = datetimes, day = day_of_week, weekend = factor(weekend, labels = c('weekday', 'weekend')), filesize = fs)
g = ggplot(df, aes(x=date, y=filesize, group = weekend, colour=weekend, alpha=0.7 )) + geom_point() 
g = g+ ggtitle('File sizes of events by the hour from GithubArchive.org')
g = g + geom_smooth()
print(g)
ggsave(g, file='../all_events_file_size.svg')
