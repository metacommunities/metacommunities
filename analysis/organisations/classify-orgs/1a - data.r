# ==============================================================================
# Data - org features
# ==============================================================================

library(gdata)
library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)


# training data

org_train <- read.xls('../data/orgs_manual_coding_sample_reconciled.xlsx',
  sheet='Sheet1', skip=6)

# compelte data (includes training data)

project <- "237471208995"

sql <- "
  SELECT repository_organization, Repos, ReposWhichAreForks, PushEvents,
    Pushers, date(FirstPush) AS FirstPush, date(LastPush) AS LastPush,
    PushDurationDays, repository_homepages, repository_owners,
    repository_languages, WatchEvents, ForkEvents, IssuesEvents,
    IssueCommentEvents, ifnull(ReleaseEvents, 0), DownloadEvents,
    PullRequestsClosed,
    PullRequestsMerged, SO_repos_linked_to, SO_posts_linking_to_orgs_repos,
    SO_answers_linking_to_orgs_repos, org_created, blog, FirstEvent,
    EarlyEvents, MinsTo20Events, First20_Creates, First20_Forks, First20_Pushes,
    First20_WatchEvents, First20_IssueEvents, First20_PullREquests,
    First20_DistinctRepos, First20_OtherEvents, Event20Time
  FROM org_ultimate_1;
"

org <- query_exec("metacommunities", "github_proper", sql, billing=project)

