
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
repos = gh %>% tbl('2014') %>% select(repository_name) %>% group_by(repository_name) %>% count
q = "SELECT repository_name, count(type) as evt FROM [githubarchive:year.2014] group by repository_name order by evt desc LIMIT 100000"
pop = query_exec(q, project=proj)
g = ggplot(pop[pop$evt>10000,], aes(x=repository_name, y=evt)) + geom_bar(stat='identity') + ylab('Events') + xlab('Repository Name')+ theme(axis.ticks.y = element_blank(), axis.text.y = element_blank()) + coord_flip() 
g1 = g+ geom_text(data = subset(pop, evt>100000), aes(label=repository_name), vjust=-0.3, hjust= -0.0,  size=3) 
g1
ggsave(g1, file='figure1_github_2014.svg')
ggsave(g1, file='figure1_github_2014.pdf')

