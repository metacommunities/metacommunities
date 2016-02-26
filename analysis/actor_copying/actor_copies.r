library(dplyr)
library(ggplot2)
library(bigrquery)
query = 'SELECT actor_attributes_login, count(type) AS events
FROM  [githubarchive:github.timeline]
group by actor_attributes_login
order by events desc'
project = 'metacommunities'
#res = query_exec(query, project, ax_pages=Inf)
res = read.csv('actors_events.csv')
head(res)
tail(res)
hist(res$events)
g = ggplot(res, aes(x=events)) + geom_histogram(binwidth=2)
ggplot(res, aes(x=events)) + geom_histogram(binwidth=2) + scale_y_log10()
ggplot(res, aes(x=events)) + geom_histogram(binwidth=10) + scale_y_log10()
actor_event_count = table(res$events)
actor_event_count = as.data.frame(actor_event_count)
colnames(actor_event_count) = c('actors', 'events')
actor_event_count$actors= as.numeric(actor_event_count$actors)
head(actor_event_count)
ggplot(actor_event_count, aes(x=actors, y=events)) + geom_point()
ggplot(actor_event_count, aes(x=actors, y=events)) + geom_point() + scale_y_log10()
ggplot(actor_event_count, aes(y=actors, x=events)) + geom_point() + scale_y_log10()
ggplot(actor_event_count, aes(y=actors, x=events)) + geom_point() + scale_y_log10()
ggplot(actor_event_count, aes(y=actors, x=events)) + geom_point(size=0.5) + scale_y_log10() + scale_x_log10()
actor_event_count$actors[actor_event_count$events <2]
sum(actor_event_count$actors[actor_event_count$events <2])

total_events = sum(res$events)

first_50 = which(cumsum(res$events) > total_events)/2)[1]
first_90 = which(cumsum(res$events) > 0.9*total_events)[1]
first_90 
g = ggplot(res[1:10000,], aes(x=actor_attributes_login, y=events)) + geom_point(size=0.5)
g + theme(axis.ticks = element_blank(), axis.text.x = element_blank()) 
