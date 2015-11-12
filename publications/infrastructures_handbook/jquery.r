
library(dplyr)
library(ggplot2)
library(stringr)
library(bigrquery)
library(utils)
library(tidyr)

proj = 'metacommunities'
gh = src_bigquery(project ='githubarchive', dataset = 'github', billing=proj)
repos = gh %>% tbl('timeline') %>% select(repository_url, repository_name, repository_created_at, type, created_at)
jq = repos %>% filter(grepl('[Jj][Qq]uery', repository_name)) %>% group_by(repository_name, repository_created_at, ) %>% arrange(repository_created_at)
jqt = collect(jq)
qu= jq$query$sql
jqt2 = query_exec(query=qu, dataset = 'githubarchive', proj, max_pages= Inf )
jqt2 = query_exec(query=qu, default_dataset = 'githubarchive:github', project=proj, max_pages= Inf )

%>% summarise(events = n())
glimpse(jq)
head(jq)
g = ggplot(jqt, aes(x=as.Date(repository_created_at))) + geom_freqpoly(binwidth=10)
g + xlab('Date repository created') + ylab('Number of repositories')
g + geom_freqpoly(aes(x = as.Date(created_at), color='red'), binwidth=10)

