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
gh = src_bigquery(project ='githubarchive', dataset = 'year', billing=proj)
year = '2013'
repos = gh %>% tbl(year) %>% select(repository_url, repository_name,  type, created_at, payload_comment_body) 

## bootstrap
repos_comment_bootstrap = repos %>% filter(repository_name == 'bootstrap', !is.na(payload_comment_body)) %>% group_by(repository_name) %>% arrange(created_at)

repos_comment = repos %>% filter(grepl('bootstrap', repository_name), !is.na(payload_comment_body)) %>% group_by(repository_name) %>% arrange(repository_name) %>% summarise(evt = n()) 
repos_comment_bootstrap = repos %>% filter(repository_name == 'bootstrap', !is.na(payload_comment_body)) %>% group_by(repository_name) %>% arrange(created_at)

bootstrap_comments_2014 = repos_comment_bootstrap %>% collect
bootstrap = repos_comment %>% collect
head(repos_comment)[, c('repository_name', 'payload_comment_body')]

head(repos_comment)

## hadoop
repos_comment = repos %>% filter(grepl('hadoop', repository_name), !is.na(payload_comment_body)) %>% group_by(repository_name) %>% arrange(repository_name) %>% summarise(evt = n()) 
repos_comment_hadoop = repos %>% filter(repository_name == 'hadoop', !is.na(payload_comment_body)) %>% group_by(repository_name) %>% arrange(created_at)


hadoop_comments = repos_comment_hadoop %>% collect
hadoop = repos_comment %>% collect
write.csv(file=paste('hadoop_comment_summary_', year, '.csv', sep=''), hadoop)
write.csv(file=paste('hadoop_comment_', year, '.csv', sep=''), hadoop_comments)
head(repos_comment)[, c('repository_name', 'payload_comment_body')]

