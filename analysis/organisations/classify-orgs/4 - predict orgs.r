# ==============================================================================
# classify the rest of the orgs based on the training data set
# ==============================================================================

library(randomForest)

rf_file <- 'data/rf.rda'

if (!file.exists(rf_file)) {
  source("3b - training random forest.r")
}

load('data/rf.rda')

# Tried to get rf to predict 'type' for test sample and kept getting:
#   Error: cannot allocate vector of size 48.0 Gb

# ------------------------------------------------------------------------------
# try 'bigrf': "Big Random Forests: Classification and Regression Forests for
# Large Data Sets"
# ------------------------------------------------------------------------------

library(bigrf)

bigrfc()
