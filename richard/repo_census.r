library(RMySQL)
library(ggplot2)
drv = dbDriver("MySQL")
con = dbConnect(drv,host="localhost",dbname="git",user="root",pass="moo")



alldata = dbGetQuery(con, "SELECT * FROM repo_events_bq_all;")

singles = dbGetQuery(con, "SELECT * FROM repo_events_bq_single;")

alldata$lastpush = as.numeric(strptime(alldata$repo_pushed_at, "%Y-%m-%d %H:%M:%S"))
alldata$lastpush = unclass(alldata$lastpush)
alldata$created = as.numeric(strptime(alldata$repo_created, "%Y-%m-%d %H:%M:%S"))
alldata$created = unclass(alldata$created)
alldata$duration = alldata$lastpush - alldata$created
alldata$weeks = alldata$duration/(60*60*24*7)


#first thing to note... there are repos with a lot of events but which look 'suspicious' 
# because they have a low number of Actors, WatchEvents	IssueCommentEvents	IssuesEvents	ForkEvents	PullRequestEvents etc.
#could call these 'anti-social' repos, they have low number of actors and don't seem to have many 'social' events, issues, forks, pull requests etc.



#make a 'social event proportion' variable - doesn't work as the 'spam' repos have spammed issues and things like that
#instead look at the proportion of events which are of a particular type
#or - use Actors to identify the spam repos

#do this first

alldata$eventsperactor = alldata$Events/alldata$Actors
alldata$eventsperweek = alldata$Events/alldata$weeks

alldata$spam = 0
alldata$spam[alldata$eventsperweek > 5000 & alldata$eventsperactor > 5000] = 1


#remove repos with size 0
alldata = subset(alldata, alldata$maxSize > 0)
alldata = subset(alldata, alldata$spam == 0)



bigrepos = subset(alldata, alldata$Events > 8192)


#bins: 10k+: 321, 5k-10k: 654, 1k-5k: 7589, 500-1k: 11975, 251-500: 27196, 126-250: 59127, 51-125: 175687, 
# 26-50: 260178, 11-25: 593447, 5-10: 625893, 2-4: 1489326, 1 event: 838443
#2 events: 617477

#power law plots

#plots of the activity per bin, include proportion which are 'spam' or outright exclude these beforehand and deal with them seperately

#so... plots showing where event data lies, and plot showing event proportions by bin

bins = seq(1:14)
repos = seq(1:14)
PushesT = seq(1:14)
PushesA = seq(1:14)


df = data.frame(bins, repos, PushesT, PushesA)

df$repos = 0
df$PushesT = 0
df$PushesA = 0
df$CreatesT = 0
df$CreatesA = 0
df$WatchesT = 0
df$WatchesA = 0
df$IssueCommentsT = 0
df$IssueCommentsA = 0
df$IssuesT = 0
df$IssuesA = 0
df$ForksT = 0
df$ForksA = 0
df$GistsT = 0
df$GistsA = 0
df$PullRequestsT = 0
df$PullRequestsA = 0
df$GollumT = 0
df$GollumA = 0
df$CommitCommentsT = 0
df$CommitCommentsA = 0
df$PullRequestReviewCommentsT = 0
df$PullRequestReviewCommentsA = 0
df$DeletesT = 0
df$DeletesA = 0
df$MembersT = 0
df$MembersA = 0
df$DownloadsT = 0
df$DownloadsA = 0

df$IsForkT = 0
df$IsForkA = 0
df$DurationA = 0

df$maxWatchersT = 0
df$maxWatchersA = 0
df$maxForksT = 0
df$maxForksA = 0
df$maxSizeA = 0

df$low = 0
df$high = 0




low = 1
high = 2
for(i in df$bins)
	{
	#expand the last bin to include largest repos
	if(high == 16384)
		{
		high = 1987760
		}

	sdata = subset(alldata, alldata$Events <= high & alldata$Events > low)
	
	df$repos[df$bins == i] = length(sdata$Events)
	df$PushesT[df$bins == i] = sum(sdata$PushEvents)
	df$PushesA[df$bins == i] = median(sdata$PushEvents)
	df$CreatesT[df$bins == i] = sum(sdata$CreateEvents)
	df$CreatesA[df$bins == i] = median(sdata$CreateEvents)
	df$WatchesT[df$bins == i] = sum(sdata$WatchEvents)
	df$WatchesA[df$bins == i] = median(sdata$WatchEvents)
	df$IssueCommentsT[df$bins == i] = sum(sdata$IssueCommentEvents)
	df$IssueCommentsA[df$bins == i] = median(sdata$IssueCommentEvents)
	df$IssuesT[df$bins == i] = sum(sdata$IssuesEvents)
	df$IssuesA[df$bins == i] = median(sdata$IssuesEvents)
	df$ForksT[df$bins == i] = sum(sdata$ForkEvents)
	df$ForksA[df$bins == i] = median(sdata$ForkEvents)
	df$GistsT[df$bins == i] = sum(sdata$GistEvents)
	df$GistsA[df$bins == i] = median(sdata$GistEvents)
	df$PullRequestsT[df$bins == i] = sum(sdata$PullRequestEvents)
	df$PullRequestsA[df$bins == i] = median(sdata$PullRequestEvents)
	df$GollumT[df$bins == i] = sum(sdata$GollumEvents)
	df$GollumA[df$bins == i] = median(sdata$GollumEvents)
	df$CommitCommentsT[df$bins == i] = sum(sdata$CommitCommentEvents)
	df$CommitCommentsA[df$bins == i] = median(sdata$CommitCommentEvents)
	df$PullRequestReviewCommentsT[df$bins == i] = sum(sdata$PullRequestReviewCommentEvents)
	df$PullRequestReviewCommentsA[df$bins == i] = median(sdata$PullRequestReviewCommentEvents)
	df$DeletesT[df$bins == i] = sum(sdata$DeleteEvents)
	df$DeletesA[df$bins == i] = median(sdata$DeleteEvents)
	df$MembersT[df$bins == i] = sum(sdata$MemberEvents)
	df$MembersA[df$bins == i] = median(sdata$MemberEvents)
	df$DownloadsT[df$bins == i] = sum(sdata$DownloadEvents)
	df$DownloadsA[df$bins == i] = median(sdata$DownloadEvents)

	df$IsForkT[df$bins == i] = length(sdata$Events[sdata$fork == 1])
	df$IsForkA[df$bins == i] = mean(sdata$fork)
	df$DurationA[df$bins == i] = median(sdata$weeks[!is.na(sdata$weeks)])
	df$DurationSD[df$bins == i] = sd(sdata$weeks[!is.na(sdata$weeks)])

	df$maxWatchersT[df$bins == i] = sum(sdata$maxWatchers)
	df$maxWatchersA[df$bins == i] = median(sdata$maxWatchers)
	df$maxForksT[df$bins == i] = sum(sdata$maxForks)
	df$maxForksA[df$bins == i] = median(sdata$maxForks)
	df$maxSizeA[df$bins == i] = median(sdata$maxSize)

	df$ForksGrowthT[df$bins == i] = sum(sdata$maxForks - sdata$minForks)
	df$WatchersGrowthT[df$bins == i] = sum(sdata$maxWatchers - sdata$minWatchers)
	
	df$low[df$bins == i] = low
	df$high[df$bins == i] = high
	
	low = high 
	high = high * 2
	}
df$binsname = paste(df$low+1, "-", df$high, sep="")
df$binsname[df$binsname == "1-1"] = "1"
df$binsname[df$binsname == "2-2"] = "2"


nrepos = length(alldata$Events)
npushes = sum(alldata$PushEvents)
ncreates = sum(alldata$CreateEvents)
nwatches = sum(alldata$WatchEvents)
nissuecomments = sum(alldata$IssueCommentEvents)
nissues = sum(alldata$IssuesEvents)
nforks = sum(alldata$ForkEvents)
npullrequests = sum(alldata$PullRequestEvents)
ngollums = sum(alldata$GollumEvents)
ncommitcomments = sum(alldata$CommitCommentEvents)
npullrequestreviews = sum(alldata$PullRequestReviewCommentEvents)
ndeletes = sum(alldata$DeleteEvents)
nmembers = sum(alldata$MemberEvents)
ndownloads = sum(alldata$DownloadEvents)
nisfork = sum(alldata$fork)
nmaxwatchers = sum(alldata$maxWatchers)
nmaxforks = sum(alldata$maxForks)
nforksgrowth = sum(alldata$maxForks - alldata$minForks)
nwatchersgrowth = sum(alldata$maxWatchers - alldata$minWatchers)


df$reposP = df$repos/nrepos
df$PushesP = df$PushesT/npushes
df$CreatesP = df$CreatesT/ncreates
df$WatchesP = df$WatchesT/nwatches
df$IssueCommentsP = df$IssueCommentsT/nissuecomments
df$IssuesP = df$IssuesT/nissues
df$ForksP = df$ForksT/nforks
df$PullRequestsP = df$PullRequestsT/npullrequests
df$GollumP = df$GollumT/ngollums
df$CommitCommentsP = df$CommitCommentsT/ncommitcomments
df$PullRequestReviewCommentsP = df$PullRequestReviewCommentsT/npullrequestreviews
df$DeletesP = df$DeletesT/ndeletes
df$MembersP = df$MembersT/nmembers
df$DownloadsP = df$DownloadsT/ndownloads
df$IsForkP = df$IsForkT/nisfork
df$maxWatchersP = df$maxWatchersT/nmaxwatchers
df$maxForksP = df$maxForksT/nmaxforks
df$forksgrowthP = df$ForksGrowthT/nforksgrowth
df$watchersgrowthP = df$WatchersGrowthT/nwatchersgrowth



bigrepos = subset(alldata, alldata$Events > 8192)



#graph 1 - actions the owner can take: PushesP, CreatesP, 



data$social = 0

data$social = (data$WatchEvents + data$IssueCommentEvents + data$IssuesEvents + data$ForkEvents + data$PullRequestEvents + data$PullRequestReviewCommentEvents)/data$Events

data$maxtype = max(data$PushEvents, data$WatchEvents)


#look at the 10k+ repos

bigrepos = subset(data, data$Events >= 10000)


#graph 1 - actions the owner can take: PushesP, CreatesP, DeletesP, MembersP
plot(df$reposP~df$bins, type="b", lwd = 3, lty = 1, col="black", axes=FALSE, main = "Number of Events for Repos in Bin", ylab = "Proportion of Events from Repos in Bin", xlab = "Bins - by total number of Events for Repo")
axis(1, at = df$bins, labels=df$binsname, cex.axis = 0.7)
axis(2)
box() #- to make it look "as usual"
points(df$PushesP ~ df$bins, type="b", lwd=3, lty=6, col="blue")
points(df$CreatesP ~ df$bins, type="b", lwd=3, lty=6, col="green")
points(df$DeletesP ~ df$bins, type="b", lwd=3, lty=6, col="red")
points(df$MembersP ~ df$bins, type="b", lwd=3, lty=6, col="grey")
legend("topright", fill = c("black",  "blue", "green", "red", "grey"), legend=c("Repos in Bin", "PushEvents", "CreateEvents", "DeleteEvents", "MemberEvents"), cex = 1, bty = "n")


#graph 2 - social events: WatchesP, IssuesP, IssueCommentsP, PullRequestsP, DownloadsP, ForkEvents
plot(df$IssueCommentsP~df$bins, type="b", lwd = 3, lty = 1, col="orange", axes=FALSE, main = "Number of Events for Repos in Bin", ylab = "Proportion of Events from Repos in Bin", xlab = "Bins - by total number of Events for Repo")
axis(1, at = df$bins, labels=df$binsname, cex.axis = 0.7)
axis(2)
box() #- to make it look "as usual"
points(df$WatchesP ~ df$bins, type="b", lwd=3, lty=6, col="blue")
points(df$PullRequestsP ~ df$bins, type="b", lwd=3, lty=6, col="green")
points(df$IssuesP ~ df$bins, type="b", lwd=3, lty=6, col="red")
points(df$reposP ~ df$bins, type="b", lwd=3, lty=6, col="black")
points(df$DownloadsP ~ df$bins, type="b", lwd=3, lty=6, col="grey")
points(df$ForksP ~ df$bins, type="b", lwd=3, lty=6, col="purple")
legend("top", fill = c("black",  "blue", "green", "purple", "red", "orange", "grey"), legend=c("Repos in Bin", "WatchEvents", "PullRequestEvents", "ForkEvents", "IssueEvents", "IssueCommentEvents", "DownloadEvents"), cex = 1, bty = "n")


#graph 3 - some medians
plot(df$PushesA~df$bins, type="b", lwd = 3, lty = 1, col="orange", axes=FALSE, main = "Median number of Events for Repos in Bin", ylab = "Median no. of Events for Repos in Bin", xlab = "Bins - by total number of Events for Repo")
axis(1, at = df$bins, labels=df$binsname, cex.axis = 0.7)
axis(2)
box() #- to make it look "as usual"
points(df$WatchesA ~ df$bins, type="b", lwd=3, lty=6, col="blue")
legend("topleft", fill = c("blue",  "orange"), legend=c("WatchEvents", "PushEvents"), cex = 1, bty = "n")


#duration
plot(df$DurationA~df$bins, type="b", lwd = 3, lty = 1, col="black", axes=FALSE, main = "Mean Duration in Weeks", ylab = "Mean Duration in Weeks for Repos in Bin", xlab = "Bins - by total number of Events for Repo")
axis(1, at = df$bins, labels=df$binsname, cex.axis = 0.7)
axis(2)
box() #- to make it look "as usual"

p.duration =
ggplot(df) +
aes(x = bins, y = DurationA) +
geom_errorbar(aes(ymin=DurationA-DurationSD, ymax=DurationA+DurationSD), colour="black", width=.1)



#graph 4 legacy events?
plot(df$maxForksP~df$bins, type="b", lwd = 3, lty = 1, col="orange", axes=FALSE, main = "Historical Forks and Watchers numbers", ylab = "Proportion of total number", xlab = "Bins - by total number of Events for Repo", ylim = c(0, 0.15))
axis(1, at = df$bins, labels=df$binsname, cex.axis = 0.7)
axis(2)
box() #- to make it look "as usual"
points(df$maxWatchersP ~ df$bins, type="b", lwd=3, lty=6, col="blue")
legend("topleft", fill = c("blue",  "orange"), legend=c("LegacyWatchers", "LegacyForks"), cex = 1, bty = "n")

#growth in legacy measures
plot(df$watchersgrowthP~df$bins, type="b", lwd = 3, lty = 1, col="orange", axes=FALSE, main = "GROWTH IN Forks and Watchers numbers", ylab = "Proportion of total growth", xlab = "Bins - by total number of Events for Repo", ylim = c(0, 0.15))
axis(1, at = df$bins, labels=df$binsname, cex.axis = 0.7)
axis(2)
box() #- to make it look "as usual"
points(df$forksgrowthP  ~ df$bins, type="b", lwd=3, lty=6, col="blue")
legend("topleft", fill = c("blue",  "orange"), legend=c("Growth in Watchers", "Growth in Forks"), cex = 1, bty = "n")



