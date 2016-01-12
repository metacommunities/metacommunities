-- Find the top forking actors and look at what they are copying
-- Then construct a table of who copies whom


"SELECT actor, repository_owner, count(*) as forkcount FROM [githubarchive:github.timeline] 
where type=='ForkEvent' 
group by actor, repository_owner
order by forkcount desc LIMIT 100000"
