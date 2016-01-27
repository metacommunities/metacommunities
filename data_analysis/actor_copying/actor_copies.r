library(bigrquery)
library(dplyr)
library(ggplot2)
library(reshape2)
library(tidyr)

q = "SELECT actor, repository_owner, count(*) as forkcount FROM [githubarchive:github.timeline] 
where type=='ForkEvent' 
group by actor, repository_owner
order by forkcount desc LIMIT 100000"

res =query_exec(project ='metacommunities', q)
write.csv(res, file='data/actor_actor.csv')



#further analysis on saved results

res = read.csv('data/actor_actor.csv')
resd = dcast(res[c(1:10000),], actor ~ repository_owner)
resd = as.matrix(resd)
resd[is.na(resd)] <- 0
#recode as boolean

x = apply(resd, 2, function(x) as.numeric(x>0))

ggplot
