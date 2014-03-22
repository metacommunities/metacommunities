# ==============================================================================
# fit a random forest to the training data set i.e. determine what information
# there is in the training sample
# ==============================================================================

source("2 - load.r")

library(randomForest)
library(ggplot2)

# ------------------------------------------------------------------------------
# combine org types with org fetaures
# ------------------------------------------------------------------------------

dat <- merge(org_train, org, all.x=TRUE)

# ------------------------------------------------------------------------------
# formula builder
# ------------------------------------------------------------------------------

ev <- c("repos",
        "repos_are_forks",
        "push_events",
        "pushers",
        "push_duration_days",
        "repository_homepages",
        "repository_owners",
        "repository_languages",
        "watch_events",
        "fork_events",
        "issue_events",
        "issue_comment_events",
        "f0_", # what is this variable?
        "download_events",
        "pull_requests_merged",
        "so_repos_linked_to",
        "mins_to_20_events",
        "has_blog")

dat <- dat[, c(ev, 'type')]
dat <- na.omit(dat)

# ------------------------------------------------------------------------------
# model if an org has a particular type
# ------------------------------------------------------------------------------

x <- dat[, ev]
y <- factor(dat$type)

rf <- randomForest(x, y, importance=TRUE, proximity=TRUE)

# save
save(ev, rf, file='data/rf.rda')

# variable importance
imp <- as.data.frame(importance(rf))
imp <- imp[, c("MeanDecreaseAccuracy", "MeanDecreaseGini")]
imp$var <- rownames(imp)
rownames(imp) <- NULL
imp <- melt(imp, id="var")
names(imp)[names(imp) == "variable"] <- "measure"



# variable order -- play with this to rearrange how the points are ordered
# pick either;  "MeanDecreaseAccuracy"  "MeanDecreaseGini"
var.order <- order(imp$value[imp$measure == "MeanDecreaseGini"])
var.order <- imp$var[imp$measure == "MeanDecreaseGini"][var.order]
imp$var <- factor(imp$var, levels=var.order)

# produce summary plot of importance of variables across each tag

p.imp <-
  ggplot(imp, aes(x=value, y=var)) +
    geom_point() +
    facet_wrap(~measure, nrow=1) +
    labs(x="", y="variable")

p.imp

ggsave(p.imp, file="img/p_forest_regression_importance.png",
  width=8, height=6)

