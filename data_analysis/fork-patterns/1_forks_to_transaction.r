library(arules)
library(plyr)
library(dplyr)
library(reshape)

query = "SELECT count(repository_name) as repo_count, repository_name, actor_attributes_login, created_at FROM [githubarchive:github.timeline],
WHERE type = 'ForkEvent' 
group each by actor_attributes_login, repository_name, created_at
order by repo_count desc
limit 10000"
#to create table of forking actors
query_forking_actors = "SELECT  
  actor_attributes_login, count(type) as fork_count,
  if(ABS(HASH(actor_attributes_login)) % 2 == 1, 'True', 'False') 
        as included_in_sample 
  FROM [githubarchive:github.timeline]  
  where
    type = 'ForkEvent'
  group by
    actor_attributes_login, included_in_sample"

#query for forks made by sample of forking actors

query_forking_actor_forks = "select repository_name, actor_attributes_login, DATE(TIMESTAMP(created_at)) as date from [githubarchive:github.timeline]
where actor_attributes_login IN 
(
   SELECT  
       actor_attributes_login
     FROM github.fork_actor_counts
       where
         fork_count > 4
     ) AND type='ForkEvent'
group by repository_name, date, actor_attributes_login
order by repository_name asc, date asc
limit 500000"

# to download the results of this query from Google BigQuery (if it has been saved in a storage bucket, and you have gsutil installed

 #gsutil cp gs://fork_actors_repos_500k/*.csv data/
forks_500k = read.csv('data/fork_actors_repos_500k.csv')
forks = forks_500k
forks = read.csv('data/results-20141115-215517.csv')

fork_counts = as.data.frame(table(forks$actor_attributes_login))
names(fork_counts) <- c('actor_attributes_login', 'count')
top_forkers = fork_counts$actor_attributes_login[fork_counts$count>4]
repo_count = as.data.frame(sort(table(forks$repository_name), decreasing=TRUE))
colnames(repo_count) = c('count')
top_repos = rownames(repo_count[repo_count$count>4,])
top_basket = forks[forks$repository_name %in% top_repos & forks$actor_attributes_login %in% top_forkers,]
summary(top_basket)
top_basket$repo_count <- NULL
top_basket = top_basket[order(top_basket$actor_attributes_login),]
tbm = melt(top_basket, id = c('repository_name', 'actor_attributes_login'))
dim(tbm)
head(tbm) 
tbm = unique(tbm[, 1:2])
tbm1 = dlply(tbm, 'actor_attributes_login', function(x){x[,1]})
head(tbm1)
tail(tbm1)
trans = as(sample(tbm1, 4000), 'transactions')
image(trans)
summary(trans)
itemFrequencyPlot(trans, support=0.009, cex.names=0.7)
rules = apriori(trans, parameter = list(support=0.01, confidence=0.6))
summary(rules)
