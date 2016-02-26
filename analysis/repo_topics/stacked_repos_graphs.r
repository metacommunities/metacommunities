#to run this you would need to download stacked_repos_events and stacked_repos_posts from bigquery github_explore
#you would also want to add an index on the repo field for both tables


library(MASS)
library(RMySQL)
library(lmtest)
library(pscl)
library(sandwich)
library(ggplot2)
library(splines)
library(gridExtra)


drv = dbDriver("MySQL")
con = dbConnect(drv,host="localhost",dbname="git",user="root",pass="moo")

repos = dbGetQuery(con, "SELECT distinct(repo) AS repo FROM stacked_repos_posts;")

repo = "/AFNetworking/AFNetworking"


sql = paste("SELECT unix_timestamp(created_at) AS created FROM stacked_repos_events WHERE repo = '", repo, "';", sep = "")
events = dbGetQuery(con, sql)

sql = paste("SELECT unix_timestamp(created_at) AS created FROM stacked_repos_posts WHERE repo = '", repo, "';", sep = "")
posts = dbGetQuery(con, sql)

#start point is 1218032158 (stackoverflow)
#end point is 1385542885 (github)
#277 weeks

week = seq(1:277)
pfreq = seq(1:277)
efreq = seq(1:277)
wdf = data.frame(week, pfreq, efreq)
wdf$pfreq = 0
wdf$efreq = 0

starttime = 1218032158 
endtime = 1218032158 + (60*60*24*7)


for(i in wdf$week)
	{
	wdf$pfreq[wdf$week == i] = length(posts$created[posts$created >= starttime & posts$created < endtime])
	wdf$efreq[wdf$week == i] = length(events$created[events$created >= starttime & events$created < endtime])
	wdf$time[wdf$week == i] = starttime 

	starttime = starttime + (60*60*24*7)
	endtime = endtime + (60*60*24*7)
	}
	
wdf$time = as.POSIXct(wdf$time, origin = "1970-01-01")

p.postweek = ggplot(wdf, aes(x = time, y = pfreq)) + geom_bar(stat = "identity") +
	labs(x="Week of Observation", y="Stackoverflow Posts")	
	
p.eventweek = ggplot(wdf, aes(x = time, y = efreq)) + geom_bar(stat = "identity") +
	labs(x="Week of Observation", y="Github events")	
	
	
gridplot = grid.arrange(p.postweek, p.eventweek, nrow=2)
	
	


plotrepo = function(repo, type = "all")
	{
	if(type == "all") 
		{
		sql = paste("SELECT unix_timestamp(created_at) AS created FROM stacked_repos_events WHERE repo = '", repo, "';", sep = "")
		events = dbGetQuery(con, sql)
	
		}
	if(type != "all")
		{
		sql = paste("SELECT unix_timestamp(created_at) AS created FROM stacked_repos_events WHERE repo = '", repo, "' AND type = '", type, "';", sep = "")
		events = dbGetQuery(con, sql)		
		}
	
	sql = paste("SELECT unix_timestamp(created_at) AS created FROM stacked_repos_posts WHERE repo = '", repo, "';", sep = "")
	posts = dbGetQuery(con, sql)
	
	#start point is 1218032158 (stackoverflow)
	#end point is 1385542885 (github)
	#277 weeks

	week = seq(1:277)
	pfreq = seq(1:277)
	efreq = seq(1:277)
	wdf = data.frame(week, pfreq, efreq)
	wdf$pfreq = 0
	wdf$efreq = 0

	starttime = 1218032158 
	endtime = 1218032158 + (60*60*24*7)


	for(i in wdf$week)
		{
		wdf$pfreq[wdf$week == i] = length(posts$created[posts$created >= starttime & posts$created < endtime])
		wdf$efreq[wdf$week == i] = length(events$created[events$created >= starttime & events$created < endtime])
		wdf$time[wdf$week == i] = starttime 

		starttime = starttime + (60*60*24*7)
		endtime = endtime + (60*60*24*7)
		}
		
	wdf$time = as.POSIXct(wdf$time, origin = "1970-01-01")

	p.postweek = ggplot(wdf, aes(x = time, y = pfreq)) + geom_bar(stat = "identity") +
		labs(x="Week of Observation", y="Stackoverflow Posts")	+
		labs(title = paste("Repo:", repo, "  Event Type:", type, "", sep=""))
		
	p.eventweek = ggplot(wdf, aes(x = time, y = efreq)) + geom_bar(stat = "identity") +
		labs(x="Week of Observation", y="Github events")	
		
		
	combiplot = grid.arrange(p.postweek, p.eventweek, nrow=2)
	return(combiplot)	

	}



