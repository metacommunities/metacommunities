## ----event_table,  echo=FALSE, results='markup'--------------------------
## ----event_table,  echo=FALSE, results='markup'--------------------------
library(xtable)
options(xtable.comment = FALSE)
df = read.csv('data/event_counts.csv', stringsAsFactors=FALSE)
kable(df[df$events>0, c(1,2)], row.names=FALSE, caption='Github event counts 2012-2015')


## ----repo_names, echo=FALSE, cache=TRUE----------------------------------
knit_hooks$set(inline = function(x) {
  prettyNum(x, big.mark=" ")
  })
library(bigrquery)
if (file.exists('data/repository_names_count_events_top1000.csv')) {
    df = read.csv('data/repository_names_count_events_top1000.csv')
} else {   
    query = 'SELECT lower(repository_name) as repository_name, count(lower(repository_name)) as count FROM [githubarchive:github.timeline] group by repository_name order by count desc LIMIT 1000'
    # need to actually run this query if file does not exist
}

q = 'dot|test|hello|build|setting|demo|config|git|learn|issue|doc|homebrew'
q1_sum = sum(df$count[grep(x=df$repo_names_clean, q)])
q2 = 'cv|resume'
q2_sum = sum(df$count[grep(x=df$repo_names_clean, q2)])
total_events = sum(df$count)
config_proportion = (q1_sum+q2_sum)/total_events
top_1000_proportion= round(total_events)/290000000 * 100
timeline_total_events = 290000000

library(xtable)
options(xtable.comment = FALSE)
df = read.csv('data/event_counts.csv', stringsAsFactors=FALSE)
kable(df[df$events>0, c(1,2)], row.names=FALSE, caption='Github event counts 2012-2015')


## ----repo_names, echo=FALSE, cache=TRUE----------------------------------
knit_hooks$set(inline = function(x) {
  prettyNum(x, big.mark=" ")
  })
library(bigrquery)
if (file.exists('data/repository_names_count_events_top1000.csv')) {
    df = read.csv('data/repository_names_count_events_top1000.csv')
} else {   
    query = 'SELECT lower(repository_name) as repository_name, count(lower(repository_name)) as count FROM [githubarchive:github.timeline] group by repository_name order by count desc LIMIT 1000'
    # need to actually run this query if file does not exist
}

q = 'dot|test|hello|build|setting|demo|config|git|learn|issue|doc|homebrew'
q1_sum = sum(df$count[grep(x=df$repo_names_clean, q)])
q2 = 'cv|resume'
q2_sum = sum(df$count[grep(x=df$repo_names_clean, q2)])
total_events = sum(df$count)
config_proportion = (q1_sum+q2_sum)/total_events
top_1000_proportion= round(total_events)/290000000 * 100
timeline_total_events = 290000000

