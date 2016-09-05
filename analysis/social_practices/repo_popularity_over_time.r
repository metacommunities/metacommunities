# queries gha   for most watched repos each month over the last few years
# and saves the results as a spreadsheet
library(dplyr)

options(dplyr.width = Inf)
library(bigrquery)

query ="
    SELECT
        month(created_at) as month,
        year(created_at) as year,
        repo.name,
        repo.url,
        count(*) as events
    FROM
        [githubarchive:year.2012],
        [githubarchive:year.2013],
        [githubarchive:year.2014],
        [githubarchive:year.2015] 
    WHERE LENGTH(repo.name) >= 2 and type =='WatchEvent'
    GROUP EACH BY year, month, repo.name, repo.url 
    HAVING events > 300
    ORDER BY year, month asc, events desc
"

df = query_exec(query, project='metacommunities')
head(df)
dim(df)
df = data.frame(df)

pos_df
table(pos_df$year, pos_df$month)
pos_df = df %>% group_by(year, month) %>% mutate(pos =min_rank(desc(events))) %>% filter(pos <=10)
write.csv(file = '../data/repos_most_watched_2012-2016.csv', pos_df)
