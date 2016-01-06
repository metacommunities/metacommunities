library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)
library(ggplot2)

billing_project <- "237471208995"


#get pushes and distinctpushes by day
sql <-
  "
SELECT date(created_at) AS date, count(created_at) AS Pushes, count(distinct(payload_commit_id)) AS DistinctPushes
FROM [github_explore.timeline] 
WHERE type = 'PushEvent'
GROUP BY date
ORDER BY date  "

dupdat <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
dupdat$date =  as.POSIXct(dupdat$date, origin = "1970-01-01")

dupdat = melt(dupdat, id = "date")

p.dup = ggplot(dupdat, aes(x = date, y = value, colour = variable)) + 
  geom_line() + 
  labs(colour = "Measure", x = "", y = "Count")
	
	


#this bit is to generate a list of pushes which we know are duplicates - so that we can look at the relevant githubarchive file to see if they are duplicated there	
sql = 
"
SELECT payload_commit_id, min(created_at) AS mincreated, max(created_at) AS maxcreated, count(payload_commit_id) AS freq, min(repository_url) AS repo
FROM [github_explore.timeline] 
WHERE type = 'PushEvent' AND created_at > '2012-08-22 00:00:01' AND created_at < '2012-08-23 00:00:01'
GROUP BY payload_commit_id
ORDER BY freq DESC 
"	

dupdat <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
#the duplicate hashes only appear once each in the githubarchive files 
#also, there's around a 7 hour time difference between timestamps on bigquery and on githubarchive