library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)

billing_project <- "237471208995"

sql <-
  "
  SELECT repo, repolinkDistinctQuestions AS question, repolinkAnswers AS answers
  FROM repos_linked_to_from_SO
  "

dat <- query_exec("metacommunities", "github_explore", sql,
  billing=billing_project)

