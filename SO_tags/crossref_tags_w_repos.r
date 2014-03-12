# ==============================================================================
# Cross-reference tags on stackoverflow with repo names on github
# ==============================================================================

library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)

library(RMySQL)

library(ggplot2)
library(scales)
library(reshape)

library(data.table)

# ------------------------------------------------------------------------------
# prepare github repo names
# ------------------------------------------------------------------------------
billing_project <- "237471208995"

# look at frequency of repo pushes
sql <- "
  SELECT pushes, count(*) as repos
  FROM repo_type
  GROUP BY pushes;
"

push_freq <- query_exec("metacommunities", "github_proper", sql,
  billing=billing_project)

ggplot(push_freq, aes(x=pushes, y=repos)) + geom_point()

push_freq <- push_freq[order(push_freq$pushes, decreasing=TRUE), ]
row.names(push_freq) <- NULL
push_freq$max_cum_sum_repos <- cumsum(push_freq$repos)
push_freq$prop <- push_freq$max_cum_sum_repos / sum(push_freq$repos)

push_freq[push_freq$prop < 0.05, ]

# about 1 million repos (25%) have 11 or more pushes
# 100,326 repos (2.4%) have 105 or more pushes

sql <- "
  SELECT SUBSTRING(repository_url, 20) AS full_name,
    date(repo_created) AS created, forks, pushes
  FROM repo_type
  WHERE fork = 0 AND pushes > 104;
"

repo_orig <- query_exec("metacommunities", "github_proper", sql,
  billing=billing_project, max_pages=Inf)

repo <- repo_orig

nrow(repo)        # 86,379 repos (does not include forks)

# remove repo names which are github websites
website <- grep(".*\\.github\\.(com|io)", repo$full_name)
length(website)   # 4,247 repos are websites
repo <- repo[-website, ]

# prep repo names
repo$full_name <- tolower(repo$full_name)
repo <- data.frame(
  repo,
  colsplit(repo$full_name, "/", c("owner", "name"))
)


repo <- data.table(repo)
setkey(repo, name)

# ------------------------------------------------------------------------------
# prepare stackoverflow data
# ------------------------------------------------------------------------------
m   <- dbDriver("MySQL")
con <- dbConnect(m, user="so_import", password="fancyTea", dbname="so")   

# which are the frequent tags?
sql <- "
  SELECT pt.tid, t.tag, count(*) AS count
  FROM posttag AS pt, tag AS t
  WHERE t.id = pt.tid
  GROUP BY pt.tid
  ORDER BY count DESC;
"

tag_count_orig <- dbGetQuery(con, sql)

tag_count <- data.table(tag_count_orig)

setkey(tag_count, tag)


# ------------------------------------------------------------------------------
# lets compare repo names with tags
# ------------------------------------------------------------------------------

# what repos have a tag?
repo_tag <- repo[J(tag_count$tag)]
repo_tag <- na.omit(repo_tag)
repo_tag <- unique(repo_tag)

# repo names are not UNIQUE ... ugh

# what tags have at least one repo with the same name?
tag_repo <- tag_count[J(repo$name)]
tag_repo <- na.omit(tag_repo)
tag_repo <- unique(tag_repo)

for (i in 1:nrow(tag_repo)) {
  tag_repo$repo_count[i] <- sum(repo_tag$name == tag_repo$tag[i])
}

# distribution of repo_count
table(tag_repo$repo_count)

# wtf one tag corresponds to 1245 repos?!
tag_repo[tag_repo$repo_count == 1245, ]
# oh, okay, 'dotfiles'


# ------------------------------------------------------------------------------
# update tag names in the 'so' database
# ------------------------------------------------------------------------------
sql <- "
  ALTER TABLE tag
    ADD repo_count SMALLINT DEFAULT 0;
"
dbGetQuery(con, sql)

for (i in 1:nrow(tag_repo)) {
  tg <- tag_repo$tag[i]
  rc <- tag_repo$repo_count[i]
  sql <- paste("UPDATE tag SET repo_count=", rc, " WHERE tag='", tg, "';", sep="")
  dbGetQuery(con, sql)
  cat(".")
}

