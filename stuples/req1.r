# ==============================================================================
# Request #1
# AM: A fat juicy plot with a lot of points relating to github. I want
# something that shows density of events on the timeline. This is meant to be
# an evocative visualization not analytical.
# ==============================================================================

library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)
library(ggplot2)
library(data.table)
library(plyr)
library(lubridate)

billing_project <- "237471208995"


# only really interested in these event types
event.types <- c("Push", "Create repository", "Watch", "Issues", "IssueComment",
  "Fork", "PullRequest")


# ------------------------------------------------------------------------------
# get a count of the interesting events on github aggregated by week
# the hard part is making sure that the events are actually unique
# ------------------------------------------------------------------------------

sql <-
  "
  SELECT date(created_at) AS date, type, payload_ref_type AS ref,
    count(*) AS count
  FROM timeline
  GROUP BY date, type, ref
  ORDER BY date;
  "

dat.query <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)

dat <- dat.query

# remove 484,172 events without any information
dat <- dat[!is.na(dat$date), ]

# construct a 'real' date
dat$date <- as.POSIXct(dat$date, format="%Y-%m-%d", tz="GMT")

# chop of the first ~6 months because of duplicated events
# 2012/09/17 is a Monday
#start.date <- as.POSIXct("2012-09-17", tz="GMT")
#dat <- dat[dat$date > start.date, ]
# and chop off the last week in the data as it will not be complete
#max.date <- floor_date(max(dat$date), "week") # 2013/11/24
#dat <- dat[dat$date < as.POSIXct("2013-11-24", tz="GMT"), ]

# week of year
dat$yearweek <- paste(year(dat$date), week(dat$date), sep="-")

# tidy up the types
dat$type <- gsub("(.*)Event", "\\1", dat$type)
# add 'ref' value on to the end of 'Create' event types
dat$type[dat$type == "Create"] <-
  paste(dat$type[dat$type == "Create"], dat$ref[dat$type == "Create"], sep=" ")
dat <- subset(dat, select=-ref)
# combine Issues and IssueComment
dat$type[dat$type == "IssueComment"] <- "Issues/IssueComment"
dat$type[dat$type == "Issues"] <- "Issues/IssueComment"

# keep only the 'interesting' events
#dat <- subset(dat, type %in% event.types)

# round to the current month and week
dat$month <- floor_date(dat$date, "month")
dat$week <- floor_date(dat$date, "week")

# ------------------------------------------------------------------------------
# aggregate to just general activity
# ------------------------------------------------------------------------------
agg <- ddply(dat, .(week), summarise, count=sum(count))

p.agg <-
  ggplot(agg, aes(x=week, y=count)) +
    geom_area() +
    labs(x="", y="Number of events per week")

p.agg

ggsave(p.agg, file="~/p_all_events_per_week.png", width=9, height=6)

# ------------------------------------------------------------------------------
# colour in for different events
# ------------------------------------------------------------------------------

agg <- ddply(dat, .(week, type), summarise, count=sum(count))

#agg$type <- ordered(agg$type, levels=rev(c("PullRequest", "Fork",
#  "Create repository", "Watch", "Issues/IssueComment", "Push")))

p.agg <-
  ggplot(agg, aes(x=week, y=count, fill=type, order=desc(type))) +
    geom_area() +
    labs(x="", y="Number of events per week", fill="Event type")

ggsave(p.agg, file="~/p_all_events_per_week_by_type.png", width=9, height=4)

