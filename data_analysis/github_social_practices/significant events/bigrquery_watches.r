library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)
library(ggplot2)

billing_project <- "237471208995"

sql <-
  "
SELECT old.repository_url AS repository_url,
old.repo_created AS repo_created,
new.date AS date,
new.Watches AS Watches
FROM
	(SELECT repository_url,
	repo_created
	FROM [github_explore.allrepos_1_social])
AS old
INNER JOIN EACH 
	(SELECT repository_url, 
	date(created_at) AS date,
	count(repository_url) AS Watches
	FROM [github_explore.timeline]
	WHERE type = 'WatchEvent'
	GROUP EACH BY repository_url, date)
AS new
ON new.repository_url = old.repository_url
ORDER BY repository_url DESC
  "

dat <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
 
repo = "https://github.com/codrops/SidebarTransitions"

sdat = dat[dat$repository_url == repo,]

sdat$date <- as.POSIXct(sdat$date, format="%Y-%m-%d", tz="GMT") 

sdat = sdat[order(sdat$date),]
sdat$cumwatchers = cumsum(sdat$Watches)

p.watches =
	ggplot(sdat, aes(x=date, y=cumwatchers)) +
    geom_line() +
    labs(x="", y="Number of Watches per day") 

p.cumwatchers <-
  ggplot(sdat, aes(x=date, y=cumwatchers)) +
    geom_line() +
    labs(x="", y="Cumulative number of Watches per day") 

#function which plots watchers per day for a specified repo
plotwatches = function(repo) 
	{
	sdat = dat[dat$repository_url == repo,]

	sdat$date <- as.POSIXct(sdat$date, format="%Y-%m-%d", tz="GMT") 

	p.watches <-
	  ggplot(sdat, aes(x=date, y=Watches)) +
		geom_line() +
		labs(x="", y="Number of Watches per day") 
	
	return(p.watches)

	}
	
	
#custom bigquery

repo = "https://github.com/balanced/balanced-dashboard"	
#repo = "https://github.com/amanuel/JS-HTML5-QRCode-Generator"

sql = paste("SELECT repository_url, 
	date(created_at) AS date,
	count(repository_url) AS Watches
	FROM [githubarchive:github.timeline]
	WHERE type = 'WatchEvent' AND repository_url = '", repo, "'
	GROUP EACH BY repository_url, date", sep = "")
	
sdat <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)	


sdat$date <- as.POSIXct(sdat$date, format="%Y-%m-%d", tz="GMT") 

sdat = sdat[order(sdat$date),]
sdat$cumwatchers = cumsum(sdat$Watches)

p.watches =
	ggplot(sdat, aes(x=date, y=Watches)) +
    geom_line() +
    labs(x="", y="Number of Watches per day") 
