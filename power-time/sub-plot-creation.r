library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)
library(ggplot2)

billing_project <- "237471208995"


#1% sample of all_repos_1_3
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_1_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <= 5 AND (HASH(repo_created)%100 == 0)  
  "

dat1.1 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
 
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_2_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <= 5 AND (HASH(repo_created)%100 == 0)
  "

dat2.1 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project) 
  
 sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_3_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <= 5 AND (HASH(repo_created)%100 == 0) 
  "

dat3.1 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project) 
  
  
  sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_4_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <= 5 AND (HASH(repo_created)%100 == 0) 
  "

dat4.1 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)  
  
  
dat1 = rbind(dat1.1, dat2.1)  
dat1 = rbind(dat1, dat3.1)
#dat1 = rbind(dat1, dat4.1)

dat1$repo_created =  as.POSIXct(dat1$repo_created, origin = "1970-01-01")

p.plot1 = ggplot(dat1, aes(x = repo_created, y = DurationDays)) + geom_point(stat = "identity", alpha = 0.05) 

sdat1 = dat1[sample(1:nrow(dat1), 10000),]


#so... this one shows 10k repos with the duration on a log scale, needs to be trimmed and have the Y axis labelled
p.plot1 = ggplot(sdat1, aes(x = repo_created, y = log(DurationDays), size = log(Events))) + geom_point(stat = "identity", alpha = 0.4) +
#scale_size(range = c(0.5, 2))
#scale_area(range = c(0.5, 1))
scale_area(range = c(min(log(sdat1$Events)), max(log(sdat1$Events))))


sdat1$logevents = log(sdat1$Events)
sdat1$logevents[sdat1$logevents == 0] = 0.001

p.plot1 = ggplot(sdat1, aes(x = repo_created, y = log(DurationDays), size = log(Events))) + geom_point(stat = "identity", alpha = 0.4) +
scale_area(range = c(min(sdat1$logevents), max(sdat1$logevents)))

#p.plot1 = ggplot(sdat1, aes(x = repo_created, y = DurationDays, size = Events)) + geom_point(stat = "identity", alpha = 0.2) 

#subplot 1 types
dat1$type = "Isolate"
dat1$type[dat1$Fork == 'true'] = "Isolate Fork"
dat1$type[dat1$Pushers > 1] = "Collaborative Pushing"
dat1$type[dat1$Fork == 'true' & dat1$Pushers > 1] = "Collaborative Fork"
dat1$type[dat1$PR_Issued > 1] = "PR Issuer"
dat1$type[dat1$PR_Received > 1] = "PR Receiver"
dat1$type[dat1$Watchers > 10] = "Watched Repo"
dat1$type[dat1$Forks > 10] = "Repo which is Forked"
dat1$type[dat1$Watchers > 10 | dat1$Forks > 10] = "Social Repo"
dat1$type[dat1$PR_Received > dat1$Watchers] = "Social PR Receiver"

sdat1 = dat1[sample(1:nrow(dat1), 10000),]
sdat1$logevents = log(sdat1$Events)
sdat1$logevents[sdat1$logevents == 0] = 0.001

p.plot1 = ggplot(sdat1, aes(x = repo_created, y = log(DurationDays), size = log(Events), colour = factor(type))) + geom_point(stat = "identity", alpha = 0.4) +
scale_area(range = c(min(sdat1$logevents), max(sdat1$logevents)))

# sub-plot 2 - repos with 50-100 events

sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_1_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 50 AND (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <=100   AND (HASH(repo_created)%100 == 0)  
  "
dat1.2 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
  
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_2_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 50 AND (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <=100   AND (HASH(repo_created)%100 == 0)  
  "
dat2.2 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)  
  
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_3_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 50 AND (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <=100   AND (HASH(repo_created)%100 == 0)  
  "
dat3.2 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)    
  
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_4_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 50 AND (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <=100   AND (HASH(repo_created)%100 == 0)   
  "
dat4.2 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)      

dat2 = rbind(dat1.2, dat2.2)  
dat2 = rbind(dat2, dat3.2)
#dat2 = rbind(dat2, dat2.4)

dat2$repo_created =  as.POSIXct(dat2$repo_created, origin = "1970-01-01")

sdat2 = dat2[sample(1:nrow(dat2), 500),]  
  
p.plot2 = ggplot(sdat2, aes(x = repo_created, y = log(DurationDays), size = log(Events))) + geom_point(stat = "identity", alpha = 0.4) +
#scale_size(range = c(0.5, 2))
#scale_area(range = c(0.5, 1))
scale_area(range = c(min(log(sdat2$Events)), max(log(sdat2$Events))))


#give these repos a type
dat2$type = "Isolate"
dat2$type[dat2$Fork == 'true'] = "Isolate Fork"
dat2$type[dat2$Pushers > 1] = "Collaborative Pushing"
dat2$type[dat2$Fork == 'true' & dat2$Pushers > 1] = "Collaborative Fork"
dat2$type[dat2$PR_Issued > 1] = "PR Issuer"
dat2$type[dat2$PR_Received > 1] = "PR Receiver"
dat2$type[dat2$Watchers > 10] = "Watched Repo"
dat2$type[dat2$Forks > 10] = "Repo which is Forked"
#dat2$type[dat2$Watchers > 10 | dat2$Forks > 10] = "Social Repo"


sdat2 = dat2[sample(1:nrow(dat2), 200),]  
  
p.plot2 = ggplot(sdat2, aes(x = repo_created, y = log(DurationDays), size = log(Events), colour = factor(type))) + geom_point(stat = "identity", alpha = 0.6) +
scale_area(range = c(min(log(sdat2$Events)), max(log(sdat2$Events)))) +
scale_colour_brewer(palette="Set1")




#sub-plot3
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_1_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 1000  AND (HASH(repo_created)%100 == 0)  
  "
dat1.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)

  
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_2_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 1000  AND (HASH(repo_created)%100 == 0)  
  "
dat2.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)  
  
  
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_3_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 1000  AND (HASH(repo_created)%100 == 0)  
  "
dat3.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)    
  
sql <-
  "
SELECT *, (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events, (PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(repo_created))/86400000000 AS DurationDays
FROM [github_explore.all_repos_4_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 1000  AND (HASH(repo_created)%100 == 0)  
  "
dat4.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)    
  
  

dat3 = rbind(dat1.3, dat2.3)  
dat3 = rbind(dat3, dat3.3)
dat3 = rbind(dat3, dat4.3)

dat3$repo_created =  as.POSIXct(dat3$repo_created, origin = "1970-01-01")

p.plot3 = ggplot(dat3, aes(x = repo_created, y = log(DurationDays), size = log(Events))) + geom_point(stat = "identity", alpha = 0.4) +
scale_area(range = c(min(log(dat3$Events)), max(log(dat3$Events))))


#give these repos a type
dat3$type = "Isolate"
dat3$type[dat3$Fork == 'true'] = "Isolate Fork"
dat3$type[dat3$Pushers > 1] = "Collaborative Pushing"
dat3$type[dat3$Fork == 'true' & dat3$Pushers > 1] = "Collaborative Fork"
dat3$type[dat3$PR_Issued > 1] = "PR Issuer"
dat3$type[dat3$PR_Received > 1] = "PR Receiver"
dat3$type[dat3$Watchers > 10] = "Watched Repo"
dat3$type[dat3$Forks > 10] = "Repo which is Forked"
dat3$type[dat3$Watchers > 10 | dat3$Forks > 10] = "Social Repo"
dat3$type[dat3$PR_Received > dat3$Watchers] = "Social PR Receiver"

p.plot3 = ggplot(dat3, aes(x = repo_created, y = log(DurationDays), size = log(Events), colour = factor(type))) + geom_point(stat = "identity", alpha = 0.4) +
scale_area(range = c(min(log(dat3$Events)), max(log(dat3$Events))))

