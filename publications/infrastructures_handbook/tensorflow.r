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
gh = src_bigquery(project ='githubarchive', dataset = 'day', billing=proj)
repos = gh %>% tbl('201511') %>% select(repo_url, repo_name,  type, created_at) %>% filter(grepl('[Tt]ensor[Ff]low', repo_name))

q = "select repo.name, created_at,actor.login, org.login,  type from (table_date_range([githubarchive:day.events_], TIMESTAMP('2015-11-01'), TIMESTAMP('2015-11-15'))) where repo.name contains 'tensorflow' "
res = query_exec(proj, query=q)

ggplot(res, aes(x=as.Date(created_at), group=org_login)) + geom_freqpoly()
