library(bigrquery)
library(brew)
library(data.table)
library(ggplot2)
library(ggthemes)
library(lubridate)
library(plyr)
library(reshape)
library(rjson)
library(Rook)
library(scales)
library(tools)
library(xkcd)

billing_project <- "237471208995"


drv = dbDriver("MySQL")
con = dbConnect(drv,host="localhost",dbname="git",user="root",pass="moo")


sql = "SELECT * FROM PR_relationships_all"

dat <- query_exec("metacommunities", "github_explore", sql,
      billing=billing_project)


data = dbGetQuery(con, "SELECT * FROM repo_pull_requests;")

data$IntraRepoProp = 0
data$IntraRepoProp = data$IntraRepoPullRequestOpenEvents/data$PullRequestOpenEvents
data$IntraRepoProp[is.na(data$IntraRepoProp)] = 0


data$ClosedProp = 0
data$ClosedProp = data$PullRequestCloseEvents/data$PullRequestOpenEvents
#some repos have more closes than opens because of time limits on data, set them to 1
data$ClosedProp[data$ClosedProp > 1] = 1

data$MergedProp = 0
data$MergedProp = data$MergedPullRequests/data$DistinctPullRequests
data$MergedProp[data$MergedProp > 1] = 1
data$MergedProp[is.na(data$MergedProp)] = 0

data$SelfMergeProp = 0
data$SelfMergeProp = data$PullRequestMergedBySameUser/data$MergedPullRequests
data$SelfMergeProp[is.na(data$SelfMergeProp)] = 0
data$SelfMergeProp[data$SelfMergeProp > 1] = 1


#get the number of events and other variables from the census data - import it
load("H:\\goteventdata.RData")



tdata = data[data$events > 0 & data$DistinctPullRequests > 1,]

tdata$distbins = 0
tdata$distbins[tdata$DistinctPullRequests == 2] = "2"
tdata$distbins[tdata$DistinctPullRequests > 2 & tdata$DistinctPullRequests <= 4] = "3-4"
tdata$distbins[tdata$DistinctPullRequests > 4 & tdata$DistinctPullRequests <= 10] = "5-10"
tdata$distbins[tdata$DistinctPullRequests > 10] = "11+"
tdata$distbins = factor(tdata$distbins, levels = c("2", "3-4", "5-10", "11+"))


p.mergeprop = 
	ggplot(tdata) +
	geom_bar(aes(x = MergedProp))+
	facet_wrap(~distbins)
	
p.selfmergeprop = 	
	ggplot(tdata) +
	geom_bar(aes(x = SelfMergeProp))+
	facet_wrap(~distbins)
	
p.closedprop = 
	ggplot(tdata) +
	geom_bar(aes(x = ClosedProp))+
	facet_wrap(~distbins)

p.intraprop = 
	ggplot(tdata) +
	geom_bar(aes(x = IntraRepoProp))+
	facet_wrap(~distbins)	
	
p.disthead = 
	ggplot(tdata) +
	geom_bar(aes(x = DistinctHeadRepos))+
	facet_wrap(~distbins)	


tdata$pullsperhead = tdata$DistinctPullRequests/tdata$DistinctHeadRepos	
tdata$pullsperhead[tdata$pullsperhead < 1] = 1

tdata$pphbin = 0
tdata$pphbin[tdata$pullsperhead == 1] = "1"
tdata$pphbin[tdata$pullsperhead > 1 & tdata$pullsperhead <= 2] = "1.01-2"
tdata$pphbin[tdata$pullsperhead > 2 & tdata$pullsperhead <= 4] = "2.01-4"
tdata$pphbin[tdata$pullsperhead > 4 & tdata$pullsperhead <= 10] = "4.01-10"
tdata$pphbin[tdata$pullsperhead > 10] = "10+"
tdata$pphbin = factor(tdata$pphbin, levels = c("1", "1.01-2", "2.01-4", "4.01-10", "10+" ))

p.pullsperhead = 
	ggplot(tdata) +
	geom_bar(aes(x = pphbin))+
	facet_wrap(~distbins)+
	labs(x = "Pull Requests Per Distinct Head Repo", y = "Freq") 


tdata$mergersbin = 0

#data-set which includes single pull request
sdata = data[data$events > 0,]

sdata$forkbins = 0
sdata$forkbins[sdata$forkevents <= 1] = "0-1"
sdata$forkbins[sdata$forkevents >= 2 & sdata$forkevents <= 4] = "2-4"
sdata$forkbins[sdata$forkevents > 4 & sdata$forkevents <= 10] = "5-10"
sdata$forkbins[sdata$forkevents > 10] = "11+"
sdata$forkbins = factor(sdata$forkbins, levels = c("0-1", "2-4", "5-10", "11+"))

#version which includes 1 pull request
sdata$distbins = 0
sdata$distbins[sdata$DistinctPullRequests == 1] = "1"
sdata$distbins[sdata$DistinctPullRequests == 2] = "2"
sdata$distbins[sdata$DistinctPullRequests > 2 & sdata$DistinctPullRequests <= 4] = "3-4"
sdata$distbins[sdata$DistinctPullRequests > 4 & sdata$DistinctPullRequests <= 10] = "5-10"
sdata$distbins[sdata$DistinctPullRequests > 10] = "11+"
sdata$distbins = factor(sdata$distbins, levels = c("1", "2", "3-4", "5-10", "11+"))


p.forks = 
	ggplot(sdata) +
	geom_bar(aes(x = distbins))+
	facet_wrap(~forkbins)+
	labs(x = "Panels show number of forkevents, bars show number of distinct pull requests", y = "Freq") 


sdata$usermergebins = 0
sdata$usermergebins[sdata$UsersWhoMerge == 2] = "0-1"
sdata$usermergebins[sdata$UsersWhoMerge >= 2 & sdata$UsersWhoMerge <= 4] = "2-4"
sdata$usermergebins[sdata$UsersWhoMerge > 4 & sdata$UsersWhoMerge <= 10] = "5-10"
sdata$usermergebins[sdata$UsersWhoMerge > 10] = "11+"
sdata$usermergebins = factor(sdata$usermergebins, levels = c("0-1", "2-4", "5-10", "11+"))	

tempdata = sdata[sdata$UsersWhoMerge > 1 & sdata$UsersWhoMerge <= 20,]
	
p.userswhomerge = 
	ggplot(tempdata) +
	geom_bar(aes(x = UsersWhoMerge))+
	facet_wrap(~distbins)+
	labs(x = "Panels show number of distinct pull requests, bars show number of mergers (> 1)", y = "Freq") 






	
	
	
	
	
	
	
	
	
	
	
	

#INTERNAL USE
data$type = 0

#self-merge
data$type[data$SelfMergeProp >= 0.5] = 4

#INTRA REPO - Internal Use
#single pull request intra-repo
data$type[data$IntraRepoProp == 1 & data$PullRequestOpenEvents == 1] = 1
#95%+ pull requests are intra repo
data$type[data$IntraRepoProp >= 0.95 & data$PullRequestOpenEvents > 1] = 2
#50-95% are intra-repo or has 100+
data$type[(data$IntraRepoProp < 0.95 & data$IntraRepoProp >= 0.5) | (data$IntraRepoPullRequestOpenEvents >= 100 & data$IntraRepoProp < 0.95)] = 3


#Failure to use
data$type2 = 0
#repos with a single pull request - merged
data$type2[data$MergedPullRequests == 0 & data$DistinctPullRequests == 1] = 1

#repos with a single pull request - not merged
data$type2[data$MergedPullRequests == 1 & data$DistinctPullRequests == 1] = 2

#repos with more than one pull request - less than 10% merged
data$type2[data$DistinctPullRequests > 1 & data$MergedProp < 0.1] = 3

#repos with more than one pull request - less than 10% closed
data$type2[data$DistinctPullRequests > 1 & data$ClosedProp < 0.1] = 4


data$PullsPerHeadRepo = data$DistinctPullRequests/data$DistinctHeadRepos

data$pphbins = 0
data$pphbins[data$DistinctPullRequests == 1] = "1"
data$pphbins[data$DistinctPullRequests > 1 & data$DistinctPullRequests <= 4] = "2-4"
data$pphbins[data$DistinctPullRequests > 4 & data$DistinctPullRequests <= 8] = "5-8"
data$pphbins[data$DistinctPullRequests > 8 & data$DistinctPullRequests <= 16] = "9-16"
data$pphbins[data$DistinctPullRequests > 16 & data$DistinctPullRequests <= 32] = "17-32"
data$pphbins[data$DistinctPullRequests > 32 & data$DistinctPullRequests <= 64] = "33-64"
data$pphbins[data$DistinctPullRequests > 64] = "64+"

data$dhrbins = 0
data$dhrbins[data$DistinctHeadRepos == 1] = "1"
data$dhrbins[data$DistinctHeadRepos > 1 & data$DistinctHeadRepos <= 4] = "2-4"
data$dhrbins[data$DistinctHeadRepos > 4 & data$DistinctHeadRepos <= 8] = "5-8"
data$dhrbins[data$DistinctHeadRepos > 8 & data$DistinctHeadRepos <= 16] = "9-16"
data$dhrbins[data$DistinctHeadRepos > 16 & data$DistinctHeadRepos <= 32] = "17-32"
data$dhrbins[data$DistinctHeadRepos > 32 & data$DistinctHeadRepos <= 64] = "33-64"
data$dhrbins[data$DistinctHeadRepos > 64] = "64+"

low = 1
high = 2
for(i in df$bins)
	{
	
	
	df$low[df$bins == i] = low
	df$high[df$bins == i] = high
	
	low = high 
	high = high * 2
	}
df$binsname = paste(df$low+1, "-", df$high, sep="")
df$binsname[df$binsname == "1-1"] = "1"
df$binsname[df$binsname == "2-2"] = "2"



#Histograms of proportion variables for type 0 repos  mergeprop, closedprop, selfmergeprop
#Histogram of distinct head repos

sdata = data[data$type ==0 & data$type2 == 0,]


sdata$PullsPerHeadRepo = sdata$DistinctPullRequests/sdata$DistinctHeadRepos

sdata$distbins = 0
sdata$distbins[sdata$DistinctPullRequests == 1] = "1"
sdata$distbins[sdata$DistinctPullRequests > 1 & sdata$DistinctPullRequests <= 4] = "2-4"
sdata$distbins[sdata$DistinctPullRequests > 4 & sdata$DistinctPullRequests <= 8] = "5-8"
sdata$distbins[sdata$DistinctPullRequests > 8 & sdata$DistinctPullRequests <= 16] = "9-16"
sdata$distbins[sdata$DistinctPullRequests > 16 & sdata$DistinctPullRequests <= 32] = "17-32"
sdata$distbins[sdata$DistinctPullRequests > 32 & sdata$DistinctPullRequests <= 64] = "33-64"
sdata$distbins[sdata$DistinctPullRequests > 64] = "64+"

data3 = data[data$type == 3,]





headtab = as.data.frame(table(data$DistinctHeadRepos[data$type == 0 & data$type2 == 0]))

p.distincthead = 
	ggplot(data) +
	geom_bar(aes(DistinctHeadRepos)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")
	

	
p.merge = 
	ggplot(sdata) +
	geom_bar(aes(MergedProp)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")

p.selfmerge = 
	ggplot(data) +
	geom_bar(aes(SelfMergeProp)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")

p.distincthead = 
	ggplot(headtab) +
	geom_bar(aes(x =Var1 , y = Freq)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")

	
	labs(x = "Age", y = "No. of Respondents") +
	xlab("Age") + ylab("No. of Respondents")	

#of the remainder..... the 'social coding' repos, are there any dominant patterns?

#repos with a single head repo and more than one pull request (how many?)

#repos which have merged all (or almost all?) pull requests






#could do a plot showing number of repos of each type within activity bins? 
#could do stacked bars, bars are bins and colours are the PERCENTAGE of repos in a bin of each type



#link this data up to event census
#data$full_name = paste("/", data$full_name, sep="")

census = dbGetQuery(con, "SELECT * FROM repo_pull_requests WHERE PullRequestEvents > 0;")

census = dbGetQuery(con, "SELECT * FROM repo_pull_requests AS pulltable LEFT JOIN (SELECT * FROM repo_events_bq_all) AS alltable ON pulltable.full_name = alltable.full_name;")



for(i in data$full_name[is.na(data$events)])
	{
	sql = paste("SELECT * FROM repo_events_with_pullrequests WHERE full_name = '", i, "';", sep="")
	cdata = dbGetQuery(con, sql)
	
	if(length(cdata$Events) > 0)
		{
		
		data$events[data$full_name == i] = cdata$Events
		data$pushevents[data$full_name == i] = cdata$PushEvents
		data$forkevents[data$full_name == i] = cdata$ForkEvents
		}
	if(length(cdata$Events) == 0)
		{
		data$events[data$full_name == i] = 0
		data$pushevents[data$full_name == i] = -1
		data$forkevents[data$full_name == i] = -1	
		}
	
	}

	
sdata = subset(data, data$events > 0)	
sdata$eventbins = 0
sdata$eventbins[sdata$events > 0 & sdata$events <= 10] = "1-10"
sdata$eventbins[sdata$events > 10 & sdata$events <= 20] = "11-20"
sdata$eventbins[sdata$events > 20 & sdata$events <= 40] = "21-40"
sdata$eventbins[sdata$events > 40 & sdata$events <= 80] = "41-80"
sdata$eventbins[sdata$events > 80 & sdata$events <= 160] = "81-160"
sdata$eventbins[sdata$events > 160 & sdata$events <= 320] = "161-320"
sdata$eventbins[sdata$events > 320 & sdata$events <= 640] = "321-640"
sdata$eventbins[sdata$events > 640] = "640+"

sdata$eventbins = factor(sdata$eventbins, levels = c("1-10", "11-20", "21-40", "41-80", "81-160", "161-320", "321-640", "640+"))

eventstype = as.data.frame(xtabs(~type+eventbins, data=sdata))

p.type = 
	ggplot(eventstype) +
	geom_bar(aes(x = eventbins, y = Freq, fill=type)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")  +
	labs(x = "Repo Event Bins", y = "Frequency") 

eventstype2 = as.data.frame(xtabs(~type2+eventbins, data=sdata))

p.type2 = 
	ggplot(eventstype2) +
	geom_bar(aes(x = eventbins, y = Freq, fill=type2)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")  +
	labs(x = "Repo Event Bins", y = "Frequency") 

	
#bin by number of pushes or forks

sdata$pushbins = 0
sdata$pushbins[sdata$pushevents > 0 & sdata$pushevents <= 10] = "1-10"
sdata$pushbins[sdata$pushevents > 10 & sdata$pushevents <= 20] = "11-20"
sdata$pushbins[sdata$pushevents > 20 & sdata$pushevents <= 40] = "21-40"
sdata$pushbins[sdata$pushevents > 40 & sdata$pushevents <= 80] = "41-80"
sdata$pushbins[sdata$pushevents > 80 & sdata$pushevents <= 160] = "81-160"
sdata$pushbins[sdata$pushevents > 160 & sdata$pushevents <= 320] = "161-320"
sdata$pushbins[sdata$pushevents > 320 & sdata$pushevents <= 640] = "321-640"
sdata$pushbins[sdata$pushevents > 640] = "640+"

sdata$pushbins = factor(sdata$pushbins, levels = c("1-10", "11-20", "21-40", "41-80", "81-160", "161-320", "321-640", "640+"))	

pusheventstype = as.data.frame(xtabs(~type+pushbins, data=sdata))

p.type = 
	ggplot(pusheventstype) +
	geom_bar(aes(x = pushbins, y = Freq, fill=type)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")  +
	labs(x = "Repo Push Event Bins", y = "Frequency") 	
	
	

sdata$forkbins = 0
sdata$forkbins[sdata$forkevents > 0 & sdata$forkevents <= 10] = "1-10"
sdata$forkbins[sdata$forkevents > 10 & sdata$forkevents <= 20] = "11-20"
sdata$forkbins[sdata$forkevents > 20 & sdata$forkevents <= 40] = "21-40"
sdata$forkbins[sdata$forkevents > 40 & sdata$forkevents <= 80] = "41-80"
sdata$forkbins[sdata$forkevents > 80 & sdata$forkevents <= 160] = "81-160"
sdata$forkbins[sdata$forkevents > 160 & sdata$forkevents <= 320] = "161-320"
sdata$forkbins[sdata$forkevents > 320 & sdata$forkevents <= 640] = "321-640"
sdata$forkbins[sdata$forkevents > 640] = "640+"

sdata$forkbins = factor(sdata$forkbins, levels = c("1-10", "11-20", "21-40", "41-80", "81-160", "161-320", "321-640", "640+"))	

forkeventstype = as.data.frame(xtabs(~type+forkbins, data=sdata))

p.type = 
	ggplot(forkeventstype) +
	geom_bar(aes(x = forkbins, y = Freq, fill=type)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")  +
	labs(x = "Repo fork Event Bins", y = "Frequency") 		

	
	
tdata = sdata[sdata$DistinctPullRequests > 1,]
	
p.mergeprop = 
	ggplot(tdata) +
	geom_bar(aes(x = MergedProp))+
	facet_wrap(~eventbins)
	
p.selfmergeprop = 	
	ggplot(tdata) +
	geom_bar(aes(x = SelfMergeProp))+
	facet_wrap(~eventbins)
	
p.closedprop = 
	ggplot(tdata) +
	geom_bar(aes(x = ClosedProp))+
	facet_wrap(~eventbins)

p.intraprop = 
	ggplot(tdata) +
	geom_bar(aes(x = IntraRepoProp))+
	facet_wrap(~eventbins)	
	
p.disthead = 
	ggplot(tdata) +
	geom_bar(aes(x = DistinctHeadRepos))+
	facet_wrap(~eventbins)	
	
tdata$pullsperhead = tdata$DistinctPullRequests/tdata$DistinctHeadRepos	

p.pphead = 
	ggplot(tdata) +
	geom_bar(aes(x = pullsperhead))+
	facet_wrap(~eventbins)	


	
pr.type = as.data.frame(xtabs(~type+distbins, data=sdata))

p.type2 = 
	ggplot(pr.type) +
	geom_bar(aes(x = distbins, y = Freq, fill=type)) +
	scale_fill_brewer(type="seq", palette="RdYlBu")  +
	labs(x = "Repo Event Bins", y = "Frequency") 

data$forkbins

data$pushbins	

	