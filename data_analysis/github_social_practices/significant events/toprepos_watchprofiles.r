library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)
library(ggplot2)

billing_project <- "237471208995"

sql <-
  "
SELECT repository_url, count(repository_url) AS watchevents
FROM [githubarchive:github.timeline]
WHERE type = 'WatchEvent' AND created_at > '2012-09-17 00:00:00'
GROUP EACH BY repository_url
ORDER BY watchevents DESC
LIMIT 500;  
  "
topwatch = query_exec("metacommunities", "github_explore", sql, billing=billing_project)
 
i = 1
 
setwd("C:\\git\\significant events\\watcher-profiles") 
for(r in topwatch$repository_url)
	{
	sql = paste("SELECT repository_url, 
	date(created_at) AS date,
	count(repository_url) AS Watches
	FROM [githubarchive:github.timeline]
	WHERE type = 'WatchEvent' AND repository_url = '", r, "' AND created_at > '2012-09-17 00:00:00'
	GROUP EACH BY repository_url, date", sep = "")
	sdat <- query_exec("metacommunities", "github_explore", sql,
	billing=billing_project)	

	sdat$date <- as.POSIXct(sdat$date, format="%Y-%m-%d", tz="GMT") 

	sdat = sdat[order(sdat$date),]


	p.watches =
	ggplot(sdat, aes(x=date, y=Watches)) +
    geom_line() +
    labs(x="", y="Number of Watches per day", title = paste("Repo: ", r, "", sep = "")) 
	
	
	ggsave(filename = paste("watchevent_time_", i, ".png", sep=""), plot = p.watches, scale = 1, width = 8, height = 5, dpi = 300)
	
	i = i + 1
	
	}
