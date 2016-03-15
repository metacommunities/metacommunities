library(bigrquery)
# collecting a million names 

query_collect = "SELECT repository_name, repository_owner FROM [githubarchive:github.timeline] LIMIT 1000000"
names = query_exec(query_collect, 'metacommunities', max_pages=1000)
write.csv(names, 'data/one_million_names.csv')

#basic idea here is count the most common names and see if that accounts for a lot of the repos
query = "SELECT lower(repository_name) as repository_name, count(lower(repository_name)) as count FROM [githubarchive:github.timeline] group by repository_name order by count desc LIMIT 1000"
query = "SELECT repository_name, lower(repository_name) as repository_name_lower, count(lower(repository_name)) as count FROM [githubarchive:github.timeline] group by repository_name_lower, repository_name order by count desc LIMIT 1000"
df = query_exec(query, 'metacommunities', max_pages= Inf) 
event_total = 289000000
sum(df$count)/event_total * 100


# do some cleaning on the repo names
df$repo_names_clean = sub(x=df$repository_name_lower, '^\\.', '')
df = df[order(df$repo_names_clean),]
write.csv(df, 'data/repository_names_count_events_top1000.csv')

#load the cleaned repo names
df = read.csv('data/repository_names_count_events_top1000.csv')

# look for config or setup files
# names that include dot, hello, test, build, setting, demo, config, git, learn

q = 'dot|test|hello|build|setting|demo|config|git|learn|issue|doc|homebrew'
q1_sum = sum(df$count[grep(x=df$repo_names_clean, q)])
q2 = 'cv|resume'
q2_sum = sum(df$count[grep(x=df$repo_names_clean, q2)])
total_events = sum(df$count)
config_proportion = (q1+q2)/total_events
top_1000_proportion= round(total_events)/290000000 * 100
timeline_total_events = 290000000

## this was an older attempt to analyse the names by grouping them together manually. Grep approach above is probably better

dfs = read.csv('data/repository_names_count_events_top1000_sorted_by_name.csv', stringsAsFactors=FALSE)
dfs$aggregate_counts = as.numeric(sub(x=dfs$aggregate_counts, pattern='', replacement='0'))

sum(dfs$aggregate_counts, na.rm=TRUE)
sum(dfs$count)
proportion = sum(dfs$aggregate_counts, na.rm=TRUE)/sum(dfs$count)
proportion
