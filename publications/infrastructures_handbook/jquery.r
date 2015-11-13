library(dplyr)
library(xts)
library(scales)
library(zoo)
library(ggplot2)
library(stringr)
library(bigrquery)
library(utils)
library(tidyr)
library(xts)
library(scales)
library(zoo)

proj = 'metacommunities'
gh = src_bigquery(project ='githubarchive', dataset = 'github', billing=proj)
repos = gh %>% tbl('timeline') %>% select(repository_url, repository_name, repository_created_at, type, created_at) 

## jquery search
jq = repos %>% filter(grepl('[Jj][Qq]uery', repository_name)) %>% group_by(repository_name, repository_created_at ) %>% arrange(repository_created_at)
jqt = jq %>% sample_n(50000) %>% collect

glimpse(jq)
head(jq)
g = ggplot(jqt, aes(x=as.Date(repository_created_at))) + geom_freqpoly(binwidth=10)
g + xlab('Date repository created') + ylab('Number of repositories')
g + geom_freqpoly(aes(x = as.Date(created_at), color='red'), binwidth=10)

## deployment events
## nothing comes back from these -- they are private/

gh2 = src_bigquery(project ='githubarchive', dataset = 'year', billing=proj)
deploy = gh2 %>% tbl('2014') %>% select(repository_url, repository_name, repository_created_at, type, created_at) 
ddr = deploy %>% filter(grepl('Dd]eploy',type)) %>% group_by(repository_name, repository_created_at, type ) %>% arrange(repository_created_at) %>% summarize(d = n())
ddrt = ddr %>% collect

# public events -- making repos public
public = gh2 %>% tbl('2014') %>% select(repository_url, repository_name, repository_created_at, type, created_at) 
ppr = public %>% filter(grepl('Public',type)) %>% group_by(repository_name, repository_created_at, type ) %>% arrange(repository_created_at) %>% summarize(d = n())
pprt = ppr %>% collect

ggplot(pprt, aes(x=repository_created_at)) + geom_freqpoly() + scale_x_date(breaks='2 months')
qu2 = "SELECT [repository_url] AS [repository_url], [repository_name] AS [repository_name], [repository_created_at] AS [repository_created_at], [type] AS [type], [created_at] AS [created_at] FROM [2014] WHERE REGEXP_MATCH('[Dd]eploy', [type]) ORDER BY [repository_name], [repository_created_at], [repository_created_at]"
res = query_exec(project=proj, default_dataset='githubarchive:year', query=qu2)

z = zoo(pprt$repository_created_at, d)
plot(z)
ggplot(pprt, aes(x=repository_created_at)) + geom_freqpoly()
cut(as.Date(ev$created_at), 20)
table(cut(as.Date(ev$created_at), 20))
p = as.Date(pprt$repository_created_at)
p = na.omit(p)
ps = cut(p, breaks=54)
table(ps)
head(ps)
ps = as.Date(cut(p, breaks=54))
pst = table(ps)
pst = as.data.frame(pst)
ggplot(pst, aes(x=as.Date(ps), y=Freq)) + geom_line()
ts1 =as.ts(pst)
plot(ts1)

## jquery events
j = 'api.jquery.com'
jqt %>% filter(grepl(j, repository_url)) %>% count(type)
ev = jqt %>% filter(grepl(j, repository_url), grepl('Fork|Push|Pull', type)) %>% arrange(created_at)
g = ggplot(ev, aes(x=as.Date(created_at), group=type, linetype=type )) + geom_freqpoly(binwidth=9)
g+ scale_x_date(labels = date_format('%m/%Y'), breaks= '1 month')
