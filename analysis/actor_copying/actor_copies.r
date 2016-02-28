library(dplyr)
library(ggplot2)
library(bigrquery)
query = 'SELECT actor_attributes_login, count(type) AS events
FROM  [githubarchive:github.timeline]
group by actor_attributes_login
order by events desc'
project = 'metacommunities'
#res = query_exec(query, project, ax_pages=Inf)
res = read.csv('actors_events.csv', as.is=TRUE)
colnames(res) = c('actor_number', 'actor', 'events')
head(res)
tail(res)

# this one is a cloud of points along the x asis
g = ggplot(res[sample.int(n=nrow(res), 100000),], aes(x=actor, y=events)) + geom_point(size=0.3) + scale_y_log10()
g = g + theme(axis.ticks = element_blank(), axis.text.x = element_blank()) 
g
ggsave(g, file = 'actor_events_unsorted.svg')

# to order the results, tabulate
actor_event_count = tabulate(res$events)
actor_event_count = as.data.frame(actor_event_count)
colnames(actor_event_count) = c(  'actor_count')
actor_event_count$event_count = as.numeric(rownames(actor_event_count))
actor_event_count = actor_event_count[actor_event_count$actor_count>0,]
head(actor_event_count)
tail(actor_event_count)
g2 = ggplot(actor_event_count[], aes(y=actor_count, x=event_count)) + geom_point(size=0.5)
g2 = g2 + theme(axis.ticks = element_blank(), axis.text.x = element_blank()) 
g2 = g2 + scale_y_log10() + scale_x_log10() +  ggtitle('Events for actors')
g2
ggsave(g2, file='actor_events_counted.svg')

actor_event_count$actor_count)actor_event_count$event_count)2]
sum(actor_event_count$actors[actor_event_count$event_count)2])

total_events = sum(res$events)

first_50 = which(cumsum(res$events) > total_events)/2)[1]
first_90 = which(cumsum(res$events) > 0.9*total_events)[1]
first_90 
