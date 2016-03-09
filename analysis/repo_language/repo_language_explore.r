library(bigrquery)
library(reshape2)
library(ggplot2)
library(dplyr)

#just the basic language and event counts

ldf = read.csv('../data/repo_language_events.csv')
head(ldf)
plot(ldf$language_count, ldf$repo_url)
m=lm(language_count ~ repo_url, data=ldf)
summary(m)
head(ldf)

# this gets the breakdown of counts by all events
query = "SELECT repository_language, count(distinct(repository_url)) as repo_count, type as event, count(repository_language) as event_count FROM [githubarchive:github.timeline] where repository_language != 'null' group by repository_language, event"
ldf2 = query_exec(query, 'metacommunities')
write.csv(ldf2, '../data/repo_language_events_detailed.csv')
head(ldf2)
dim(ldf2)
ldf2 %>% group_by(repository_language)
ldf2 %>% group_by(repository_language, event)
ldfs = ldf2 %>% group_by(repository_language, event) %>% arrange (desc(repo_count), desc(event_count))
head(dcast(ldf2, repository_language~event))
#to look at javascript style languages in concert
scr = ldf2 %>% filter(repository_language %in% c('JavaScript', 'TypeScript', 'CoffeeScript')) %>% group_by(repository_language) %>% arrange (desc(repo_count), desc(event_count))
head(ldf2)
ggplot(ldf2, aes(x=repo_count, y=event_count)) + geom_point()
ggplot(ldf2[1:50,], aes(x=event, y=event_count)) + geom_bar(stat='identity') + facet_grid(repository_language ~ .)
head(ldf2)
savehistory('repo_language_explore.r')
