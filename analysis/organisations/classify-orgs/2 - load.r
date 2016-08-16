# ==============================================================================
# load existing data set, otherwise create it
# ==============================================================================

rda_file <- "data/org.rda"

if (!file.exists(rda_file)) {
  source("1a - data.r")
  source("1b - clean.r")
  save(org_train, org, file=rda_file)
  rm(list=ls())
}

rda_file <- "data/org.rda"
load(rda_file)

