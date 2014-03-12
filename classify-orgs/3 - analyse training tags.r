# ==============================================================================
# explore and analysising the training data set i.e. the org tags from
# Adrian and Richard
# ==============================================================================

source("2 - load.r")

library(ggplot2)
library(plyr)
library(randomForest)
library(reshape)

# ------------------------------------------------------------------------------
# frequency of tags
# ------------------------------------------------------------------------------

tag <- melt(org_train, id="repository_organization",
  measure=c("is_software", "is_technical", "is_education", "is_business",
    "is_games", "is_social"))

tag <- tag[tag$value != 0, ]

p.tag <-
  ggplot(tag, aes(x=variable)) +
    geom_bar()

ggsave(p.tag, file="img/p_tag_freq.png")


# ------------------------------------------------------------------------------
# dist of how many tags an org has
# ------------------------------------------------------------------------------

table(rowSums(org_train[, grep("^is_", names(org_train))]))


# ------------------------------------------------------------------------------
# combine org tags with org fetaures
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
        "mins_to_20_events",
        "repository_homepages",
        "repository_owners",
        "repository_languages",
        "watch_events",
        "fork_events",
        "issue_events",
        "so_repos_linked_to",
        "has_blog")

sat.frml <- function(x) {
  rhs <- paste(ev, collapse = " + ")
  frml <- paste(x, "~", rhs)
  as.formula(frml)
}


# ------------------------------------------------------------------------------
# model if an org has the tag X
# ------------------------------------------------------------------------------

tags <- grep("^is_", names(dat), value=TRUE)

tag.imp <- list()

for (tag in tags) {
  dat[[tag]] <- factor(dat[[tag]])
  
  sft_frml <- sat.frml(tag)
  
  # fit random forest
  rf <- randomForest(sft_frml, data=dat, importance=TRUE, proximity=TRUE)

  # variable importance
  imp <- as.data.frame(importance(rf))
  imp <- imp[, c("MeanDecreaseAccuracy", "MeanDecreaseGini")]
  imp$var <- rownames(imp)
  rownames(imp) <- NULL
  imp <- melt(imp, id="var")
  names(imp)[names(imp) == "variable"] <- "measure"
  
  # save
  tag.imp[[tag]] <- imp
}

tag.imp.bk <- melt(tag.imp, id=names(tag.imp[[1]]))

tag.imp <- tag.imp.bk

# variable order -- play with this to rearrange how the points are ordered

tag.order <- ddply(tag.imp, .(var, measure), summarize, mean=mean(value))
# pick either;  "MeanDecreaseAccuracy"  "MeanDecreaseGini"
tag.order <- tag.order[tag.order$measure == "MeanDecreaseGini", ]
tag.order <- tag.order$var[order(tag.order$mean)]

tag.imp$var <- factor(tag.imp$var, levels=tag.order)

# produce summary plot of importance of variables across each tag

p.imp <-
  ggplot(tag.imp, aes(x=value, y=var)) +
    geom_point() +
    facet_grid(measure ~ L1) +
    labs(x="", y="variable")

p.imp

ggsave(p.imp, file="img/p_forest_regression_importance.png",
  width=15, height=5)

