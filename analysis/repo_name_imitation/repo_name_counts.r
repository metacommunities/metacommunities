#basic idea here is count the most common names and see if that accounts for a lot of the repos
library(bigrquery)
query = "SELECT lower(repository_name) as repository_name, count(lower(repository_name)) as count FROM [githubarchive:github.timeline] group by repository_name order by count desc LIMIT 1000"
df = query_exec(query, 'metacommunities') 
write.csv(df, 'data/repository_names_count_events_top1000.csv')
event_total = 289000000
sum(df$count)/event_total * 100

dfs = df[order(df$repository_name),]
write.csv(dfs, 'data/repository_names_count_events_top1000_sorted_by_name.csv')

df = read.csv('data/repository_names_count_events_top1000.csv')
