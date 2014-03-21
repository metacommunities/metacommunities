# ==============================================================================
# Clean-up the data ready for classifying
# ==============================================================================

# ------------------------------------------------------------------------------
# org_train - training data
# ------------------------------------------------------------------------------

# fix column names
names(org_train) <- tolower(names(org_train)) # fucking "Richard.type"
names(org_train) <- gsub("\\.", "_", names(org_train))

# construct a new column with Adrian and Richard reconciled values
org_train$type <- org_train$adrian_type

org_train$type[!is.na(org_train$reconciled)] <- org_train$reconciled[!is.na(org_train$reconciled)]

# some 'types' are dead, I'll remove these
#org_train <- na.omit(org_train)

# create tag indciators
#tags <- c(
#  as.character(org_train$tag1),
#  as.character(org_train$tag2),
#  as.character(org_train$tag3),
#  as.character(org_train$tag4)
#)

#tags <- as.data.frame(table(tags))
#tags <- tags[order(tags$Freq, decreasing=TRUE), ]

# 'software' is the only real tag
# 
# though will also create indicators for other tags;
#   - technical
#   - education
#   - business
#   - games
#   - social

#create_tag_indicator <- function(tag) {
#  tag_cols <- c('tag1', 'tag2', 'tag3', 'tag4')
#  dat <- org_train[, tag_cols] == tag
#  dat <- rowSums(dat)
#  return(dat)
#}

#org_train$is_software  <- create_tag_indicator("software")
#org_train$is_technical <- create_tag_indicator("technical")
#org_train$is_education <- create_tag_indicator("education")
#org_train$is_business  <- create_tag_indicator("business")
#org_train$is_games     <- create_tag_indicator("games")
#org_train$is_social    <- create_tag_indicator("social")

# ------------------------------------------------------------------------------
# org - complete data
# ------------------------------------------------------------------------------

## fix column names
names(org)[names(org) == "Repos"] <- "repos"
names(org)[names(org) == "ReposWhichAreForks"] <- "repos_are_forks"
names(org)[names(org) == "Pushers"] <- "pushers"
names(org)[names(org) == "FirstPush"] <- "first_push"
names(org)[names(org) == "LastPush"] <- "last_push"
names(org)[names(org) == "PushDurationDays"] <- "push_duration_days"
names(org)[names(org) == "PushEvents"] <- "push_events"
names(org)[names(org) == "WatchEvents"] <- "watch_events"
names(org)[names(org) == "ForkEvents"] <- "fork_events"
names(org)[names(org) == "IssuesEvents"] <- "issue_events"
names(org)[names(org) == "IssueCommentEvents"] <- "issue_comment_events"
names(org)[names(org) == "ReleaseEvents"] <- "release_events"
names(org)[names(org) == "DownloadEvents"] <- "download_events"
names(org)[names(org) == "PullRequestsClosed"] <- "pull_requests_closed"
names(org)[names(org) == "PullRequestsMerged"] <- "pull_requests_merged"
names(org)[names(org) == "SO_repos_linked_to"] <- "so_repos_linked_to"
names(org)[names(org) == "SO_posts_linking_to_orgs_repos"] <- "so_posts_linking_to_orgs_repos"
names(org)[names(org) == "SO_answers_linking_to_orgs_repos"] <- "so_answers_linking_to_orgs_repos"
names(org)[names(org) == "FirstEvent"] <- "first_event"
names(org)[names(org) == "EarlyEvents"] <- "early_events"
names(org)[names(org) == "MinsTo20Events"] <- "mins_to_20_events"
names(org)[names(org) == "First20_Creates"] <- "first_20_creates"
names(org)[names(org) == "First20_Forks"] <- "first_20_forks"
names(org)[names(org) == "First20_Pushes"] <- "first_20_pushes"
names(org)[names(org) == "First20_WatchEvents"] <- "first_20_watch_events"
names(org)[names(org) == "First20_IssueEvents"] <- "first_20_issue_events"
names(org)[names(org) == "First20_PullREquests"] <- "first_20_pull_requests"
names(org)[names(org) == "First20_DistinctRepos"] <- "first_20_distinct_repos"
names(org)[names(org) == "First20_OtherEvents"] <- "first_20_other_events"
names(org)[names(org) == "Event20Time"] <- "event_20_time"
# that feels better

# should 'org_created' be dropped?
table(org$org_created == '1000-01-01 00:00:00') # 47% missing; drop it!
org <- org[, names(org) != "org_created"]

# create 'has_blog'
org$has_blog <- factor(org$blog != "", levels=c(FALSE, TRUE), labels=c("no", "yes"))
org <- org[, names(org) != "blog"]


