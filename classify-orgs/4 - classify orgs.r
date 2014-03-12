# ==============================================================================
# classify the rest of the orgs based on the training data set
# ==============================================================================

source("2 - load.r")

library(randomForest)

dat <- merge(org, org_train, all.x=TRUE)

ev <- c("repos",
        "repos_are_forks",
        "push_events",
        "pushers",
        "push_duration_days")

dat <- dat[, ev]

rf <- randomForest(dat, ntree=1, nodesize=10)
# Error: cannot allocate vector of size 48.0 Gb

