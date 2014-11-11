# ==============================================================================
# acquire data for the power-time plot:
#   - power-law cruve
#   - sample of repos with tiny activity
#   - sample of repos with small activity
#   - sample of repos with large acticity
# ==============================================================================

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

# ------------------------------------------------------------------------------
# all data for these graphs can be found in the following tables:
#   - all_repos_1_3
#   - all_repos_2_3
#   - all_repos_3_3
#   - all_repos_4_3
#
# fields of interest:
#   - repo_created
#   - watchers
#   - forks
#   - pushes
#   - pull requests received; pr_received
#   - pull requests issued; pr_issued
# ------------------------------------------------------------------------------


# big ol' line of activity 
dat.query <- lapply(1:4, function(x) {
    sql <-
      paste("
      SELECT ifnull(watchers, 0) + ifnull(forks, 0) + ifnull(pushes, 0) + ifnull(pr_received, 0) +
        ifnull(pr_issued, 0) AS activity, count(*) as freq, sum(ifnull(watchers, 0) + ifnull(forks, 0) + ifnull(pushes, 0) + ifnull(pr_received, 0) +
        ifnull(pr_issued, 0)) AS totalevents
      FROM all_repos_", x, "_3
      GROUP BY activity
      ", sep="")

    dat <- query_exec("metacommunities", "github_explore", sql,
      billing=billing_project)
    cat(".")
    return(dat)
  }
)

dat <- dat.query

dat <- melt(dat, id=names(dat[[1]]))
dat2 <- ddply(dat, .(activity), summarise, freq=sum(freq), tot = sum(totalevents))

#sdat <- dat[dat$activity < 10^4, ]
#names(sdat) <- c("x", "y")


p <-
  ggplot(dat2, aes(x=activity, y=freq)) +
    labs(x = "Number of events", y = "Number of repos") +
    scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    geom_smooth(colour="blue", size=2, se=FALSE) +
	geom_smooth(aes(y = tot), colour="red", size=2, se=FALSE) +
    theme_bw()
	
	
p <-
  ggplot(dat2, aes(x=activity, y=tot)) +
    labs(x = "Number of events", y = "Number of repos") +
    scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    geom_smooth(colour="blue", size=2, se=FALSE) +
	geom_smooth(aes(y = freq), colour="red", size=2, se=FALSE) +
    theme_bw()	+
	geom_rect(aes(xmin = 10, xmax = 25000, ymin = 0, ymax = 100000000, x = NULL, y = NULL, fill = NULL), alpha = 0.01)+
	opts(panel.grid.major = theme_blank(), panel.grid.minor = theme_blank())
	
	
dat3 = melt(dat2, id.vars = "activity")	
dat3$Measure = dat3$variable
dat3$Measure[dat3$Measure == "tot"] = "Cumulative Events"
dat3$Measure[dat3$Measure == "freq"] = "No. Repositories"

p <-
  ggplot(dat3, aes(x=activity, y=value, colour = factor(variable))) +
    labs(x = "Number of events", y = "Number of repos") +
    scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    geom_smooth(size=2, se=FALSE) +
    theme_bw()	+
	geom_rect(aes(xmin = 10, xmax = 25000, ymin = 0, ymax = 100000000, x = NULL, y = NULL, fill = NULL), alpha = 0.01)+
	opts(panel.grid.major = theme_blank(), panel.grid.minor = theme_blank())	+
	scale_colour_manual(values = c("red", "black"))
	

sdat <- dat3[dat3$activity < 10^4, ]

p <-
  ggplot(sdat, aes(x=activity, y=value, colour = factor(variable))) +
    labs(x = "Number of events", y = "Number of repos") +
    scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    geom_smooth(size=2, se=FALSE) +
    theme_bw()	+
	geom_rect(aes(xmin = 5, xmax = 1000, ymin = 0, ymax = 100000000, x = NULL, y = NULL, fill = NULL), alpha = 0.01)+
	opts(panel.grid.major = theme_blank(), panel.grid.minor = theme_blank())	+
	scale_colour_manual(values = c("red", "black"))	
	
#put in a grey background box covering the middle area


#remove grid-lines

#increase scale size


# find values to write on
sql <-
  "
SELECT count(*) AS Repos, sum(ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events
FROM [github_explore.all_repos_1_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <= 10 
  "
v1.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
sql <-
  "
SELECT count(*) AS Repos, sum(ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events
FROM [github_explore.all_repos_2_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <= 10 
  "
v2.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)  

  sql <-
  "
SELECT count(*) AS Repos, sum(ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events
FROM [github_explore.all_repos_3_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <= 10 
  "
v3.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
sql <-
  "
SELECT count(*) AS Repos, sum(ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events
FROM [github_explore.all_repos_4_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) <= 10 
  "
v4.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)  
  
sp1events = sum(v1.3$Events, v2.3$Events, v3.3$Events, v4.3$Events)  
sp1repos = sum(v1.3$Repos, v2.3$Repos, v3.3$Repos, v4.3$Repos) 


sql <-
  "
SELECT count(*) AS Repos, sum(ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events
FROM [github_explore.all_repos_1_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 1000 
  "
v1.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
sql <-
  "
SELECT count(*) AS Repos, sum(ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events
FROM [github_explore.all_repos_2_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 1000 
  "
v2.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)  

  sql <-
  "
SELECT count(*) AS Repos, sum(ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events
FROM [github_explore.all_repos_3_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 1000 
  "
v3.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)
  
sql <-
  "
SELECT count(*) AS Repos, sum(ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) AS Events
FROM [github_explore.all_repos_4_3] 
WHERE (ifnull(Pushes, 0) + Forks + Watchers + ifnull(PR_Received,0) + ifnull(PR_Issued, 0) + ifnull(PR_intra, 0)) >= 1000 
  "
v4.3 <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)  
  
sp3events = sum(v1.3$Events, v2.3$Events, v3.3$Events, v4.3$Events)  
sp3repos = sum(v1.3$Repos, v2.3$Repos, v3.3$Repos, v4.3$Repos) 



	