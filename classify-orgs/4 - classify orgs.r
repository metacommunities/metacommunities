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

ytest <- factor(xtest$is_software)

x <- org
x <- x[!(x$repository_organization %in% xtest$repository_organization), ]

xtest <- xtest[, ev]
xtest <- sapply(xtest, as.numeric)

x <- x[, ev]
x <- sapply(x, as.numeric)

rf <- randomForest(x=x, xtest=xtest, ytest=ytest, ntree=50, nodesize=25)
# Error: cannot allocate vector of size 48.0 Gb

# ------------------------------------------------------------------------------
# try 'bigrf': "Big Random Forests: Classification and Regression Forests for
# Large Data Sets"
# ------------------------------------------------------------------------------

library(bigrf)

bigrfc()
