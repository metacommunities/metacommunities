# Null language repos

Null language repos may comprise 70% of the total repo count on Github. 
So much effort has gone to show how different languages are used, and how they have different communities. What about all of the repos that have no language? Do they matter?


```r
knit_hooks$set(inline = function(x) {
  prettyNum(x, big.mark=",")
  })
library(bigrquery)
query =  "SELECT count(distinct(repository_url)) as repo_count FROM [githubarchive:github.timeline] WHERE repository_language IS NULL"
query3 =  "SELECT count(distinct(repository_url)) as repo_count FROM [githubarchive:github.timeline] WHERE repository_language IS NOT NULL"
query2 =  "SELECT count(distinct(repository_url)) as repo_count FROM [githubarchive:github.timeline]"
null_count = query_exec(query, 'metacommunities')
full_count = query_exec(query2, 'metacommunities')
lang_count = query_exec(query3, 'metacommunities')
null_count
```

```
##   repo_count
## 1   11977813
```

```r
full_count
```

```
##   repo_count
## 1   15895325
```

```r
lang_count
```

```
##   repo_count
## 1    9422190
```

```r
query4 =  "SELECT count(repository_url) as Events FROM [githubarchive:github.timeline] WHERE repository_language IS NULL"
null_event_lang_count = query_exec(query4, 'metacommunities')
null_event_lang_count
```

```
##     Events
## 1 49341663
```

```r
query5 =  "SELECT count(repository_url) as Events FROM [githubarchive:github.timeline]"
total_events = query_exec(query5, 'metacommunities')
total_events
```

```
##      Events
## 1 280754610
```

```r
null_proportion =round( null_event_lang_count/total_events*100)
null_proportion
```

```
##   Events
## 1     18
```


That's pretty amazing -- 11,977,813 repositories of the total 15,895,325 repositories do not have a language recorded. 9,422,190 repositories do have a language recorded or detected. Put differently, of the 280,754,610 in the timeline data, 49,341,663 come from repositories with no programming language. That is, around 18%. A significant amount of work is going into these repositories.  

What is going on here? 


