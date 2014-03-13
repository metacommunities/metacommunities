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
        "repository_homepages",
        "repository_owners",
        "repository_languages",
        "watch_events",
        "fork_events",
        "issue_events",
        "issue_comment_events",
        "f0_",
        "download_events",
        "pull_requests_merged",
        "so_repos_linked_to",
        "mins_to_20_events",
        "has_blog",
        "is_software",
        "is_technical",
        "is_education",
        "is_business",
        "is_games",
        "is_social")


# ------------------------------------------------------------------------------
# model if an org has a particular type
# ------------------------------------------------------------------------------

x <- dat[, ev]
y <- factor(dat$type)

rf <- randomForest(x, y, data=dat, importance=TRUE, proximity=TRUE)

# variable importance
imp <- as.data.frame(importance(rf))
imp <- imp[, c("MeanDecreaseAccuracy", "MeanDecreaseGini")]
imp$var <- rownames(imp)
rownames(imp) <- NULL
imp <- melt(imp, id="var")
names(imp)[names(imp) == "variable"] <- "measure"

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

# ------------------------------------------------------------------------------
# been reading up on random forests, trying some more things
# ------------------------------------------------------------------------------

tag = "is_software"

MDSplot(rf[[tag]], dat[[tag]])


# http://stats.stackexchange.com/a/30701/16290
library(ROCR)

OOB.votes <- predict(rf[[tag]], dat, type="prob")
OOB.pred <- OOB.votes[,2]

pred.obj <- prediction(OOB.pred, dat[[tag]])

RP.perf <- performance(pred.obj, "rec", "prec")
plot(RP.perf)

ROC.perf <- performance(pred.obj, "fpr", "tpr")
plot(ROC.perf)

plot(RP.perf@alpha.values[[1]], RP.perf@x.values[[1]])
lines(RP.perf@alpha.values[[1]], RP.perf@y.values[[1]])
lines(ROC.perf@alpha.values[[1]], ROC.perf@x.values[[1]])






