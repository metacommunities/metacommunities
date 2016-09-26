library(bigrquery)

q ="SELECT
  unique(repo.id)
FROM
  [githubarchive:year.2015],
  [githubarchive:year.2014],
  [githubarchive:year.2013],
  [githubarchive:year.2012],
  [githubarchive:year.2011]
WHERE
  repo.id BETWEEN 1
  AND 1000000
group by
  repo.id
order by repo.id"

res = query_exec('metacommunities', query=q, max_pages=Inf)
colnames(res) = 'id'
res$diff = c(1, diff(res$id, lag=1))
max = max(res$id)
min = 1
id_count = max - min
missing_repo_count = max - nrow(res)
missing_repo_count
y = round(res$id/1000,0)
x = res$id %% 1000
res$x=x
res$y=y
ggplot(res, aes(x=x, y=y)) + geom_point(size=0.05,  alpha=0.6)
ggplot(res, aes(x=id)) + geom_histogram(bins=400, alpha=0.4) + geom_density()
ggplot(res, aes(x=diff)) + geom_histogram(bins=400, alpha=0.4)
res[res$diff>50,]

q2 = "SELECT
  repo.id AS id,
  MIN(DATE(created_at)) AS start_date FROM
  --   [githubarchive:year.2015],
  --   [githubarchive:year.2014],
  --   [githubarchive:year.2013],
  [githubarchive:year.2012],
  [githubarchive:year.2011]
WHERE
  repo.id BETWEEN 5000000
  AND 6000000
  AND (type == 'CreateEvent'
    OR type == 'ForkEvent')
  group by id
 ORDER BY
  id"
res2 = query_exec('metacommunities', query = q2, max_pages = 40) 
head(res2)
ggplot(res2, aes(x=as.Date(start_date))) + geom_bar()
ggplot(res2, aes(x=as.Date(start_date))) + geom_freqpoly(bins=60)

#get all repo.ids and creation dates -- sample in this github table. 
# should be around 50MB
q3 = 'select * from [metacommunities:github_explore.repo_id_by_date_sample]'
res3 = query_exec('metacommunities', query = q3, max_pages = Inf) 
head(res3)
ggplot(res3, aes(x=as.Date(start_date))) + geom_bar()
ggplot(res3, aes(x=as.Date(start_date), y=id)) + geom_point(size=.3)

# using downloaded data
library(readr)

r5 = read_csv('data/all_ids.csv')
head(r5)
dim(r5)
ggplot(r5, aes(x=as.Date(start_date), y=id)) + geom_point(size=.3)

#use the 1% sample
r6 = read_csv('data/all_years.csv')
head(r6)
dim(r6)
ggplot(r6, aes(x=as.Date(start_date), y=id)) + geom_point(size=.3)
ggplot(r6, aes(x=as.Date(start_date))) + geom_freqpoly(bins=900 )
r6$start_date = as.Date(r6$start_date)
