library(bigrquery)
q = "select * from github.actor_location"
ds = query_exec(query =q, project ='metacommunities')
ds$log_location <- log(ds$location_count)
ds$log_location <- round(log(ds$location_count), 0) + 1
write.csv(file='location.csv', ds)
