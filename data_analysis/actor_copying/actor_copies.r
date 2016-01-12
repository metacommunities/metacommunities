library(bigrquery)
library(Matrix)
library(dplyr)
library(ggplot2)
library(reshape2)

q = "SELECT actor, repository_owner, count(*) as forkcount FROM [githubarchive:github.timeline] 
where type=='ForkEvent' 
group by actor, repository_owner
order by forkcount desc LIMIT 100000"

res =query_exec(project ='metacommunities', q)
write.csv(res, file='data/actor_actor.csv')
mat = as.matrix(table(res$actor,  res$repository_owner))
matdf = melt(mat)


#further analysis on saved results

res = read.csv('data/actor_actor.csv')
mat = Matrix(as.matrix(table(res$actor, res$repository_owner)), sparse=TRUE)
