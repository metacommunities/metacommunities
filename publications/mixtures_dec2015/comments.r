
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
repos = gh %>% tbl('2014') %>% select(repo_url, repo_name,  type, created_at) %>% filter(grepl('[Tt]ensor[Ff]low', repo_name))
