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
        ifnull(pr_issued, 0) AS activity, count(*) as freq
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
dat <- ddply(dat, .(activity), summarise, freq=sum(freq))

sdat <- dat[dat$activity < 10^4, ]
names(sdat) <- c("x", "y")
p <-
  ggplot(sdat, aes(x=x, y=y)) +
    labs(x = "Number of events", y = "Number of repos") +
    scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    scale_x_log10(breaks = trans_breaks("log10", function(x) 10^x),
      labels = trans_format("log10", math_format(10^.x))) +
    geom_smooth(colour="blue", size=2, se=FALSE) +
    theme_bw()

