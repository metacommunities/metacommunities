library(dplyr)
library(ggplot2)
library(tidyr)
library(lubridate) 

df = read.csv('data/bootstrap_fork_events.csv', stringsAsFactors=FALSE)

df$created_at = as.Date(df$created_at, '%Y-%m-%d')
df2 <-  df %>% group_by(repository_name) %>%  count(created_at)
head(df2)
head(df)
fork_count = 10
forks_to_use = which(table(df$repository_name)>fork_count )
ggplot(df[], aes(x=created_at,  fill=repository_name, group= repository_name)) + geom_area(stat='bin') + guides(fill=FALSE)

