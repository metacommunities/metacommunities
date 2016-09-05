# queries gha   for most watched repos each month over the last few years
# and saves the results as a spreadsheet
library(bigrquery)
library(dplyr)
library(tidyr)
library(reshape2)

options(dplyr.width = Inf)

event_rep_count <- function(type='ForkEvent', event_count=200){
        query =paste("
            SELECT
                month(created_at) as month,
                year(created_at) as year,
                repo.name,
                repo.url,
                count(*) as events
            FROM
                [githubarchive:year.2011],
                [githubarchive:year.2012],
                [githubarchive:year.2013],
                [githubarchive:year.2014],
                [githubarchive:year.2015] 
            WHERE LENGTH(repo.name) >= 2 AND type == '",
            type, "'
            GROUP EACH BY year, month, repo.name, repo.url 
            HAVING events > ",
            event_count,
            " ORDER BY year, month ASC, events DESC",sep='')

        df = query_exec(query, project='metacommunities')
        head(df)
        df = data.frame(df)
        return(df)
}

events_to_count = 200
types = c('MemberEvent', 'PushEvent', 'PullRequestEvent', 'WatchEvent', 'ForkEvent', 'IssuesEvent')
type = types[3]
df = event_rep_count(type, events_to_count)
pos_df = df %>% group_by(year, month) %>% mutate(pos =min_rank(desc(events))) %>% filter(pos <=10)
head(pos_df)
file_name = paste('../data/repos_most_', type, '.csv', sep='')
write.csv(file =file_name, pos_df)

# reshape rankings into year x repo

pos_df = read.csv('../data/repos_most_watched_2012-2016.csv')
wide = pos_df %>% dcast(year+month ~ repo_name, value.var='pos')
head(wide)
