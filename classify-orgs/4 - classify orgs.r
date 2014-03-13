# ==============================================================================
# classify the rest of the orgs based on the training data set
# ==============================================================================

source("2 - load.r")

library(randomForest)

# list of preditors
ev <- c("repos",
        "repos_are_forks",
        "push_events",
        "pushers",
        "push_duration_days")


# need to split out the test and train sets
xtest <- merge(org_train, org, all.x=TRUE)
ytest <- xtest$is_software

xtest <- xtest[, ev]



x <- org[, ev]



rf <- randomForest(dat, ntree=1, nodesize=10) # run as an unsupervised classifier
# Error: cannot allocate vector of size 48.0 Gb

