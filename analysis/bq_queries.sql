/* How many events of different types */

SELECT type, count(type) as events FROM [githubarchive:github.timeline] group by type order by events desc LIMIT 1000

/* How many events per actor */

SELECT actor_attributes_login, count(type) AS events
FROM  [githubarchive:github.timeline]
group by actor_attributes_login
order by events desc

/*the top repository names by event count */
SELECT repository_name, count(repository_name) as count FROM [githubarchive:github.timeline] 
group by repository_name
order by count desc
LIMIT 1000

/*Stu's query on repositories: how often repos are used
------------------------------------------------ */
SELECT RepoEvents, COUNT(*) AS Freq
FROM
(
    SELECT repository_name, COUNT(repository_name) AS RepoEvents
    FROM [githubarchive:github.timeline]
    GROUP BY repository_name
) MyTable
GROUP BY RepoEvents
ORDER BY Freq DESC

/*  Top 100 Repos by number of events */

SELECT repository_name, RepoEvents
FROM
(
    SELECT repository_name, COUNT(repository_name) AS RepoEvents
    FROM [githubarchive:github.timeline]
    GROUP BY repository_name
) MyTable
GROUP BY RepoEvents, repository_name
ORDER BY RepoEvents DESC
limit 100;


/*fork - pull requests
- only 1 month time window to deal with size of data
- 3
*/
SELECT
    ForkTable.repository_url,
    COUNT(DISTINCT ForkTable.url) AS f2p_number,
    AVG(PARSE_UTC_USEC(PullTable.created_at)-PARSE_UTC_USEC(ForkTable.created_at))/3600000000 AS f2p_interval_hour
FROM
    (SELECT
    url,
    repository_url,
    MIN(created_at) AS created_at
    FROM
    [githubarchive:github.timeline]
    WHERE type='ForkEvent'
    AND PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-04-01 00:00:00')
    AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2012-05-01 00:00:00')
    GROUP BY
    repository_url,
    url)
AS ForkTable
INNER JOIN
    (SELECT
    repository_url,
    payload_pull_request_head_repo_html_url,
    MIN(created_at) AS created_at
    FROM
    [githubarchive:github.timeline]
    WHERE type='PullRequestEvent'
    AND PARSE_UTC_USEC(created_at) >= PARSE_UTC_USEC('2012-04-01 00:00:00')
    AND PARSE_UTC_USEC(created_at) < PARSE_UTC_USEC('2012-05-01 00:00:00')
    GROUP BY
    repository_url,
    payload_pull_request_head_repo_html_url)
AS PullTable
ON
    ForkTable.repository_url=PullTable.repository_url AND
    ForkTable.url=PullTable.payload_pull_request_head_repo_html_url
GROUP BY
ForkTable.repository_url
ORDER BY
f2p_number DESC



/* Pull request events, discrete pull requests, and merged pull requests - per repo
*/

SELECT payload_pull_request_base_repo_url, 
count(payload_pull_request_base_repo_url) as PullRequestEvents, 
count(distinct(payload_pull_request_id)) as PullRequests,
sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
FROM [publicdata:samples.github_timeline]
WHERE type = 'PullRequestEvent' 
GROUP BY payload_pull_request_base_repo_url
ORDER BY PullRequests DESC
limit 1000;


/* attempting to construct the fork-pull request table*
the join method is clunky/

SELECT pulltable.repository_url,forktable.fork as forks, count(type) as pullrequests
FROM
//left join is all the pullrequest events
    (SELECT repository_url, type FROM
    [githubarchive:github.timeline]
    WHERE type='PullRequestEvent') as pulltable
JOIN
//right join is just the repos with > 1000 forks
//this limit can be changed by using JOIN EACH
    (SELECT repository_url, count(type) as fork
    FROM [githubarchive:github.timeline]
    WHERE (type='ForkEvent')
    GROUP BY repository_url
    having fork > 1000
    order by fork desc) as forktable
//the inner join is just repository_url
on pulltable.repository_url = forktable.repository_url
GROUP BY pulltable.repository_url, forks
order by forks
limit 100;


/* much simpler way to do fork-pullrequest table
using the sum(if ...) approach*/

select repository_url, SUM(IF(type='ForkEvent', 1,0)) as fork,
SUM(IF(type='PullRequestEvent', 1,0)) as pullrequest
from [githubarchive:github.timeline]
where (type='ForkEvent') or (type='PullRequestEvent')
group by repository_url
order by fork desc
limit 100;

/* trying to version of the Pull requests, merged pull request per repo with the fork events
Why doesn't it seem to work properly?*/

SELECT repository_url, payload_pull_request_base_repo_url, 
sum(if(type='ForkEvent', 1,0)) as ForkEvents,
count(payload_pull_request_base_repo_url) as PullRequestEvents, 
count(distinct(payload_pull_request_id)) as PullRequests,
sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
FROM [githubarchive:github.timeline]
WHERE (type = 'PullRequestEvent') or
(type = 'ForkEvent')
GROUP EACH BY repository_url, payload_pull_request_base_repo_url
ORDER BY PullRequests DESC, ForkEvents DESC
limit 100;

/* Richard's latest wide pull request table
Really good one!
*/

SELECT payload_pull_request_base_repo_url, 
count(payload_pull_request_base_repo_url) as PullRequestEvents, 
count(distinct(payload_pull_request_id)) as DistinctPullRequests,
count(distinct(payload_pull_request_head_repo_url)) as DistinctHeadRepos,
sum(IF(payload_action = 'opened', 1, 0)) AS PullRequestOpenEvents,
sum(IF(payload_action = 'closed', 1, 0)) AS PullRequestCloseEvents,
sum(IF(payload_pull_request_head_repo_url == payload_pull_request_base_repo_url AND payload_action = 'opened', 1, 0)) AS IntraRepoPullRequestOpenEvents,
sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
count(distinct(payload_pull_request_merged_by_login)) AS UsersWhoMerge,
sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0)) AS PullRequestMergedBySameUser,
FROM [github_explore.timeline]
WHERE type = 'PullRequestEvent' 
GROUP EACH BY payload_pull_request_base_repo_url
ORDER BY PullRequestEvents DESC
limit 1000;

/* Looking for forks which have supplanted their parents
Start with finding the 200k fork repos which have the most PushEvents
This query excludes those created before 2012-03-12 
because we need their ForkEvent to be included in the data or we can't ascertain their parent.
Results have been saved as 200k_active_forks
*/

SELECT repository_url,
count(repository_url) AS PushEvents,
count(distinct(actor_attributes_login)) AS Pushers,
sum(IF(actor_attributes_login = repository_owner, 1, 0)) AS PushesByOwner,
min(repository_watchers) AS minWatchers,
max(repository_watchers) as maxWatchers,
min(repository_size) AS minSize,
max(repository_size) AS maxSize,
min(repository_forks) AS minForks,
max(repository_forks) AS maxForks,
min(repository_created_at) AS created_at,
max(created_at) AS last_push,
FROM [github_explore.timeline]
WHERE type = 'PushEvent' AND repository_fork = 'true' 
AND PARSE_UTC_USEC(repository_created_at) >= PARSE_UTC_USEC('2012-03-12 00:00:00') 
GROUP EACH BY repository_url
ORDER BY PushEvents Desc
LIMIT 200000

/*
Get table of pushers for fork repos
*/
SELECT repository_url AS fork_url,
actor_attributes_login AS pusher,
count(repository_url) AS PushEvents,
min(created_at) AS first_push,
max(created_at) AS last_push,
FROM [github_explore.timeline]
WHERE type = 'PushEvent' AND repository_fork = 'true' 
AND PARSE_UTC_USEC(repository_created_at) >= PARSE_UTC_USEC('2012-03-12 00:00:00') 
GROUP EACH BY fork_url, pusher
ORDER BY PushEvents Desc
LIMIT 200000



/*
This creates a table linking the active fork repos to their parent repos
Saved as active_forks_parents
*/

SELECT
ForkTable.fork_url, ParentTable.repository_url
FROM
 (SELECT
   repository_url AS fork_url,
  FROM [github_explore.200k_active_forks]
  GROUP EACH BY
   fork_url
   )
 AS ForkTable
 INNER JOIN EACH
 (SELECT
   repository_url, url
  FROM
   [githubarchive:github.timeline]
  WHERE type='ForkEvent'
  GROUP EACH BY
   repository_url, url)
 AS ParentTable
 ON
  ForkTable.fork_url=ParentTable.url 

/* This one uses the table linking forks to their parents
and produces a table of values for the parent repos
Saved as 200k_active_forks_parentdata
*/
SELECT Parent.repo AS parent_repo,
Parent.PushEvents,
Parent.Pushers,
Parent.PushesByOwner,
Parent.minWatchers,
Parent.maxWatchers,
Parent.minSize,
Parent.maxSize,
Parent.minForks,
Parent.maxForks,
Parent.created_at,
Parent.last_push,
FROM
	(SELECT repository_url AS repo,
	count(repository_url) AS PushEvents,
	count(distinct(actor_attributes_login)) AS Pushers,
	sum(IF(actor_attributes_login = repository_owner, 1, 0)) AS PushesByOwner,
	min(repository_watchers) AS minWatchers,
	max(repository_watchers) as maxWatchers,
	min(repository_size) AS minSize,
	max(repository_size) AS maxSize,
	min(repository_forks) AS minForks,
	max(repository_forks) AS maxForks,
	min(repository_created_at) AS created_at,
	max(created_at) AS last_push,
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY repo)
AS Parent
INNER JOIN EACH 
	(SELECT ParentTable_repository_url AS parent
	FROM [github_explore.200k_fork_parent_relations]
	GROUP EACH BY parent)
AS parentstable
ON Parent.repo = parentstable.parent

/* Same as above but just want names of pushers
Extracted to ipython
*/
SELECT Parent.repo AS parent_repo,
Parent.PushEvents,
Parent.Pusher,
Parent.first_push,
Parent.last_push,
FROM
	(SELECT repository_url AS repo,
	actor_attributes_login AS pusher,
	count(repository_url) AS PushEvents,
	min(created_at) AS first_push,
	max(created_at) AS last_push,
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY repo, pusher)
AS Parent
INNER JOIN EACH 
	(SELECT ParentTable_repository_url AS parent
	FROM [github_explore.200k_fork_parent_relations]
	GROUP EACH BY parent)
AS parentstable
ON Parent.repo = parentstable.parent


/* This query is to add information on pull requests made/received in relation to the forked repos (with the forked repo as head)
*/ 
SELECT PR.headurl AS HeadURL,
PR.baseurl AS BaseURL,
PR.PRUser AS PRUser,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr,
FROM
	(SELECT payload_pull_request_head_repo_url AS headurl,
	payload_pull_request_base_repo_url AS baseurl,
	payload_pull_request_user_login AS PRUser, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent'
	GROUP EACH BY headurl, baseurl, PRUser)
AS PR
INNER JOIN EACH 
	(SELECT REGEXP_REPLACE(ForkTable_fork_url, 'https://github.com/', 'https://api.github.com/repos/') AS head
	FROM [github_explore.200k_fork_parent_relations]
	GROUP EACH BY head)
AS headtable
ON PR.headurl = headtable.head
ORDER BY HeadURL

/* This query is to add information on pull requests made/received in relation to the forked repos (with the forked repo as base)
saved as: 200k_active_forks_PRbase 
*/ 
SELECT PR.baseurl AS BaseURL,
PR.headurl AS HeadURL,
PR.PRUser AS PRUser,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr,
FROM
	(SELECT payload_pull_request_head_repo_url AS headurl,
	payload_pull_request_base_repo_url AS baseurl,
	payload_pull_request_user_login AS PRUser, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent'
	GROUP EACH BY baseurl, headurl, PRUser)
AS PR
INNER JOIN EACH 
	(SELECT REGEXP_REPLACE(ForkTable_fork_url, 'https://github.com/', 'https://api.github.com/repos/') AS fork
	FROM [github_explore.200k_fork_parent_relations]
	GROUP EACH BY fork)
AS forktable
ON PR.baseurl = forktable.fork
ORDER BY BaseURL

/* This query is to add information on pull requests made/received in relation to the parent repos (with the parent repo as base)
saved as: 200k_active_parents_PRbase 
*/ 
SELECT PR.baseurl AS BaseURL,
PR.headurl AS HeadURL,
PR.PRUser AS PRUser,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr,
FROM
	(SELECT payload_pull_request_head_repo_url AS headurl,
	payload_pull_request_base_repo_url AS baseurl,
	payload_pull_request_user_login AS PRUser, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent'
	GROUP EACH BY baseurl, headurl, PRUser)
AS PR
INNER JOIN EACH 
	(SELECT REGEXP_REPLACE(ParentTable_repository_url, 'https://github.com/', 'https://api.github.com/repos/') AS parent
	FROM [github_explore.200k_fork_parent_relations]
	GROUP EACH BY parent)
AS parenttable
ON PR.baseurl = parenttable.parent
ORDER BY BaseURL

/* This query is to add information on pull requests made/received in relation to the parent repos (with the parent repo as head)
saved as: 200k_active_parents_PRheads
*/ 
SELECT PR.headurl AS HeadURL,
PR.baseurl AS BaseURL,
PR.PRUser AS PRUser,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr,
FROM
	(SELECT payload_pull_request_base_repo_url AS baseurl,
	payload_pull_request_head_repo_url AS headurl,
	payload_pull_request_user_login AS PRUser, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent'
	GROUP EACH BY headurl, baseurl, PRUser)
AS PR
INNER JOIN EACH 
	(SELECT REGEXP_REPLACE(ParentTable_repository_url, 'https://github.com/', 'https://api.github.com/repos/') AS parent
	FROM [github_explore.200k_fork_parent_relations]
	GROUP EACH BY parent)
AS parenttable
ON PR.headurl = parenttable.parent
ORDER BY BaseURL







/* This query is for the repo census and produces mostly counts of the number of events
Because there are so many repos it needs to be done in stages through the python API, which is slow...
*/
SELECT repository_url,
count(repository_url) AS Events,
count(distinct(actor_attributes_login)) AS Actors,
sum(if(type = 'PushEvent', 1, 0)) AS PushEvents,
sum(if(type = 'CreateEvent', 1, 0)) AS CreateEvents,
sum(if(type = 'CreateEvent' AND payload_ref_type = 'branch', 1, 0)) AS CreateBranchEvents,
sum(if(type = 'WatchEvent', 1, 0)) AS WatchEvents,
sum(if(type = 'IssueCommentEvent', 1, 0)) AS IssueCommentEvents,
sum(if(type = 'IssuesEvent', 1, 0)) AS IssuesEvents,
sum(if(type = 'ForkEvent', 1, 0)) AS ForkEvents,
sum(if(type = 'GistEvent', 1, 0)) AS GistEvents,
sum(if(type = 'PullRequestEvent', 1, 0)) AS PullRequestEvents,
sum(if(type = 'FollowEvent', 1, 0)) AS FollowEvents,
sum(if(type = 'GollumEvent', 1, 0)) AS GollumEvents,
sum(if(type = 'CommitCommentEvent', 1, 0)) AS CommitCommentEvents,
sum(if(type = 'PullRequestReviewCommentEvent', 1, 0)) AS PullRequestReviewCommentEvents,
sum(if(type = 'DeleteEvent', 1, 0)) AS DeleteEvents,
sum(if(type = 'MemberEvent', 1, 0)) AS MemberEvents,
sum(if(type = 'DownloadEvent', 1, 0)) AS DownloadEvents,
sum(if(type = 'PublicEvent', 1, 0)) AS PublicEvents,
sum(if(type = 'ForkApplyEvent', 1, 0)) AS ForkApplyEvents,
min(repository_created_at) AS repo_created,
max(repository_pushed_at) AS repo_pushed_at,
min(repository_watchers) AS minWatchers,
max(repository_watchers) as maxWatchers,
min(repository_size) AS minSize,
max(repository_size) AS maxSize,
min(repository_forks) AS minForks,
max(repository_forks) AS maxForks,
max(repository_language) AS language,
IF(max(repository_fork) = 'true', 1, 0) AS fork
FROM [github_explore.timeline]
GROUP EACH BY repository_url
ORDER BY Events Desc


/* The following queries are for looking at ongoing relationships between base and head repos through pull requests
I've saved most or all of the results as tables, because getting at the data I wanted involved layers of custom-made tables
The first one gets base/head pairs which are not intra-repo - cutting it off at 200k and ordering by pull request events 
means that we are left with pairs that have a minimum 4 events 
Saved as: PR_Base_Head_Pairs_NoIntra
*/
SELECT payload_pull_request_base_repo_url, payload_pull_request_head_repo_url, count(payload_pull_request_head_repo_url) AS pullrequestevents, min(created_at) AS firstPR, max(created_at) as lastPR, count(distinct(payload_pull_request_id)) AS DistinctPullRequests, 
FROM [githubarchive:github.timeline]
WHERE type = "PullRequestEvent"  AND payload_pull_request_head_repo_url != payload_pull_request_base_repo_url
GROUP EACH BY  payload_pull_request_head_repo_url, payload_pull_request_base_repo_url
ORDER BY pullrequestevents DESC
LIMIT 200000

/* table of users who pushed to base repo of pair
saved as: PR_Base_repo_Push_By_User
*/
SELECT Base.baseurl AS BaseURL,
Base.actor AS BasePusher,
Base.PushEvents,
Base.first_push,
Base.last_push,
FROM
	(SELECT REGEXP_REPLACE(repository_url, 'https://github.com/', 'https://api.github.com/repos/' ) AS baseurl,
	actor, 
	count(repository_url) AS PushEvents,
	max(created_at) AS last_push,
	min(created_at) AS first_push,
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY baseurl, actor)
AS Base
INNER JOIN EACH 
	(SELECT payload_pull_request_base_repo_url AS base
	FROM [github_explore.Base_Head_Pairs_NoIntra]
	GROUP EACH BY base)
AS basetable
ON Base.baseurl = basetable.base
ORDER BY BaseURL

/* table of users who pushed to head repo of pair
saved as: PR_Head_repo_Push_By_User
*/
SELECT Head.headurl AS HeadURL,
Head.actor AS HeadPusher,
Head.PushEvents,
Head.first_push,
Head.last_push,
FROM
	(SELECT REGEXP_REPLACE(repository_url, 'https://github.com/', 'https://api.github.com/repos/' ) AS headurl,
	actor, 
	count(repository_url) AS PushEvents,
	max(created_at) AS last_push,
	min(created_at) AS first_push,
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY headurl, actor)
AS Head
INNER JOIN EACH 
	(SELECT payload_pull_request_head_repo_url AS head
	FROM [github_explore.Base_Head_Pairs_NoIntra]
	GROUP EACH BY head)
AS headtable
ON Head.headurl = headtable.head
ORDER BY HeadURL

/* table of pull requests (opens, closes, distincts) grouped by user and repo and whether they were merged plus more counts (self-merges) and times 
saved as: PR_Users_NoIntra
*/
SELECT PR.headurl AS HeadURL,
PR.baseurl AS BaseURL,
PR.PRUser AS PRUser,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr,
FROM
	(SELECT payload_pull_request_head_repo_url AS headurl,
	payload_pull_request_base_repo_url AS baseurl,
	payload_pull_request_user_login AS PRUser, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent'
	GROUP EACH BY headurl, baseurl, PRUser)
AS PR
INNER JOIN EACH 
	(SELECT payload_pull_request_head_repo_url AS head
	FROM [github_explore.Base_Head_Pairs_NoIntra]
	GROUP EACH BY head)
AS headtable
ON PR.headurl = headtable.head
ORDER BY HeadURL

/*Looking at table of memberevents to see if users were added to base repo and when
saved as: PR_AddedUsers_NoIntra
*/
SELECT Base.baseurl AS BaseURL,
Base.AddedUser AS AddedUser,
Base.AddedAt AS AddedAt
FROM
	(SELECT REGEXP_REPLACE(repository_url, 'https://github.com/', 'https://api.github.com/repos/' ) AS baseurl,
	payload_member_login AS AddedUser, 
	min(created_at) AS AddedAt,
	FROM [github_explore.timeline]
	WHERE type = 'MemberEvent'
	GROUP EACH BY baseurl, AddedUser)
AS Base
INNER JOIN EACH 
	(SELECT payload_pull_request_base_repo_url AS base
	FROM [github_explore.Base_Head_Pairs_NoIntra]
	GROUP EACH BY base)
AS basetable
ON Base.baseurl = basetable.base
ORDER BY BaseURL

/*GHTorrent query - looking at name duplications and whether they are forks
*/
SELECT name, 
count(name) AS numprojects, 
sum(IF(forked_from > 0, 1, 0)) AS forks
FROM projects 
GROUP BY name 
ORDER BY numprojects desc

/*The $1800 query - iterate on payload_pull_request_base_repo_url until bank account is empty*/

    SELECT payload_pull_request_head_repo_url, 
	    count(payload_pull_request_head_repo_url) as PullRequestEvents, 
	    count(distinct(payload_pull_request_id)) as DistinctPullRequests,
	    count(distinct(payload_pull_request_head_repo_url)) as DistinctHeadRepos,
	    sum(IF(payload_action = 'opened', 1, 0)) AS PullRequestOpenEvents,
	    sum(IF(payload_action = 'closed', 1, 0)) AS PullRequestCloseEvents,
	    sum(IF(payload_pull_request_head_repo_url == payload_pull_request_base_repo_url AND payload_action = 'opened', 1, 0)) AS IntraRepoPullRequestOpenEvents,
	    sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
	    count(distinct(payload_pull_request_merged_by_login)) AS UsersWhoMerge,
	    sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0)) AS PullRequestMergedBySameUser,
	    min(created_at) AS FirstPullRequest,
	    max(created_at) AS LastPullRequest,
	    min(payload_pull_request_head_repo_created_at) AS HeadRepoCreated,
	    max(payload_pull_request_head_repo_fork) AS Fork,
	    max(payload_pull_request_base_repo_url) AS payload_pull_request_base_repo_url,
    FROM [github_explore.timeline]
    WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_url = 'https://api.github.com/repos/zznate/intravert-ug'
    GROUP EACH BY payload_pull_request_head_repo_url
    ORDER BY PullRequestEvents DESC 
        LIMIT 5000000;

/* Null Language repos */
SELECT repository_url, count(repository_url) AS PushEvents, count(distinct(actor_attributes_login)) AS Pushers, max(repository_size) AS maxSize
FROM [githubarchive:github.tcount(payload_pull_request_head_repo_url) as PullRequestEvents, 
	    count(distinct(payload_pull_request_id)) as DistinctPullRequests,
	    count(distinct(payload_pull_request_head_repo_url)) as DistinctHeadRepos,
	    sum(IF(payload_action = 'opened', 1, 0)) AS PullRequestOpenEvents,
	    sum(IF(payload_action = 'closed', 1, 0)) AS PullRequestCloseEvents,
	    sum(IF(payload_pull_request_head_repo_url == payload_pull_request_base_repo_url AND payload_action = 'opened', 1, 0)) AS IntraRepoPullRequestOpenEvents,
	    sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
	    count(distinct(payload_pull_request_merged_by_login)) AS UsersWhoMerge,
	    sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0)) AS PullRequestMergedBySameUser,
	    min(created_at) AS FirstPullRequest,
	    max(created_at) AS LastPullRequest,
	    min(payload_pull_request_head_repo_created_at) AS HeadRepoCreated,
	    max(payload_pull_request_head_repo_fork) AS Fork,
	    max(payload_pull_request_base_repo_url) AS payload_pull_request_base_repo_url,count(payload_pull_request_head_repo_url) as PullRequestEvents, 
	    count(distinct(payload_pull_request_id)) as DistinctPullRequests,
	    count(distinct(payload_pull_request_head_repo_url)) as DistinctHeadRepos,
	    sum(IF(payload_action = 'opened', 1, 0)) AS PullRequestOpenEvents,
	    sum(IF(payload_action = 'closed', 1, 0)) AS PullRequestCloseEvents,
	    sum(IF(payload_pull_request_head_repo_url == payload_pull_request_base_repo_url AND payload_action = 'opened', 1, 0)) AS IntraRepoPullRequestOpenEvents,
	    sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
	    count(distinct(payload_pull_request_merged_by_login)) AS UsersWhoMerge,
	    sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0)) AS PullRequestMergedBySameUser,
	    min(created_at) AS FirstPullRequest,
	    max(created_at) AS LastPullRequest,
	    min(payload_pull_request_head_repo_created_at) AS HeadRepoCreated,
	    max(payload_pull_request_head_repo_fork) AS Fork,
	    max(payload_pull_request_base_repo_url) AS payload_pull_request_base_repo_url,count(payload_pull_request_head_repo_url) as PullRequestEvents, 
	    count(distinct(payload_pull_request_id)) as DistinctPullRequests,
	    count(distinct(payload_pull_request_head_repo_url)) as DistinctHeadRepos,
	    sum(IF(payload_action = 'opened', 1, 0)) AS PullRequestOpenEvents,
	    sum(IF(payload_action = 'closed', 1, 0)) AS PullRequestCloseEvents,
	    sum(IF(payload_pull_request_head_repo_url == payload_pull_request_base_repo_url AND payload_action = 'opened', 1, 0)) AS IntraRepoPullRequestOpenEvents,
	    sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
	    count(distinct(payload_pull_request_merged_by_login)) AS UsersWhoMerge,
	    sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0)) AS PullRequestMergedBySameUser,
	    min(created_at) AS FirstPullRequest,
	    max(created_at) AS LastPullRequest,
	    min(payload_pull_request_head_repo_created_at) AS HeadRepoCreated,
	    max(payload_pull_request_head_repo_fork) AS Fork,
	    max(payload_pull_request_base_repo_url) AS payload_pull_request_base_repo_url,imeline]
WHERE repository_language IS NULL AND type = 'PushEvent'
GROUP EACH BY repository_url
#HAVING PushEvents > 1 AND maxSize > 0
ORDER BY PushEvents DESC


/* Organisations */
SELECT repository_organization, count(distinct(repository_name)) AS Repos, count(repository_organization) AS PushEvents, count(distinct(actor)) AS Pushers
FROM [githubarchive:github.timeline]
WHERE type = 'PushEvent'
GROUP EACH BY repository_organization
ORDER BY Repos DESC


/* 1% sample of timeline pushevents - to look at organisation prevalence over time */
SELECT repository_organization, type, created_at 
FROM [githubarchive:github.timeline]
WHERE (HASH(created_at)%100 == 0) AND type = 'PushEvent'


/* Want a table which shows all forkevents BY repos which have an organisation 
For a forkevent: repository_url is the repo WHICH WAS FORKED, url is the NEWLY CREATED REPO, repository_organization relates to the base repo
*/
/*Events where a fork is created FROM a repository owned by an organisation 
forks_made_from_orgs*/
SELECT repository_organization AS parent_organization, 
min(repository_url) AS parent_url, 
url AS fork_url, 
min(created_at) AS creation_date
FROM [githubarchive:github.timeline]
WHERE type = 'ForkEvent' AND repository_organization IS NOT NULL
GROUP BY parent_organization, fork_url
ORDER BY parent_organization ASC

/* Table of organizations and their repos 
orgs_and_their_repos
*/

SELECT repository_organization, 
	repository_url, 
	max(SUBSTR(repository_url, 19, 500)) AS repo,
	count(repository_organization) AS Events, 
	sum(if(type = 'PushEvent', 1, 0)) AS Pushes,
	max(repository_homepage) AS repository_homepage,
	max(repository_fork) AS is_fork,
	max(repository_description) AS repository_description,
	max(domain(repository_homepage)) AS repository_homepage_domain
FROM [githubarchive:github.timeline]
WHERE repository_organization IS NOT NULL
GROUP EACH BY repository_organization, repository_url
ORDER BY repository_organization ASC


/* Joins on above to produce a list of forks MADE BY ORGANISATIONS
SELECT parenttable.fork AS fork_url,
parenttable.ParentUrl AS parent_url,
parenttable.created_at AS creation_date,
forktable.repository_organization AS fork_organization
FROM
	(SELECT url AS fork,
	min(repository_url) AS ParentUrl,
	min(created_at) AS created_at
	FROM [githubarchive:github.timeline]
	WHERE type = 'ForkEvent'
	GROUP EACH BY fork)
AS parenttable
INNER JOIN EACH 
	(SELECT repository_url AS ForkURL,
	repository_organization
	FROM [github_explore.orgs_and_their_repos])
AS forktable
ON parenttable.fork = forktable.ForkURL
ORDER BY parent_url ASC






/* How many repos have a repository_homepage */
SELECT repository_url, count(repository_url) AS pushes, max(repository_homepage) AS website
FROM [githubarchive:github.timeline] 
WHERE repository_homepage IS NOT NULL AND repository_homepage != '' AND type = 'PushEvent'
GROUP EACH BY repository_url
ORDER BY Pushes Desc

/* Add variables to the forks_made_by_orgs (and opposite) table: number of pull requests each way, number accepted, etc.
First table has rows only where the "fork_made_by_org" made a pull request as the head repo 
forks_made_by_orgs_with_pullrequests_forkashead
*/
SELECT forktable.fork_organization AS fork_organization,
forktable.fork_url AS fork_url,
forktable.parent_url AS parent_url,
forktable.creation_date AS fork_creation,
PR.headurl AS HeadURL,
PR.baseurl AS BaseURL,
PR.DistinctPRUsers AS DistinctPRUsers,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr
FROM
	(SELECT payload_pull_request_head_repo_html_url AS headurl,
	payload_pull_request_base_repo_html_url AS baseurl,
	count(distinct(payload_pull_request_user_login)) AS DistinctPRUsers, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_head_repo_html_url != payload_pull_request_base_repo_html_url
	GROUP EACH BY headurl, baseurl)
AS PR
INNER JOIN EACH 
	(SELECT fork_organization,
	fork_url,
	parent_url,
	creation_date
	FROM [github_explore.forks_made_by_orgs])
AS forktable
ON PR.headurl = forktable.fork_url
ORDER BY parent_url ASC

/* This one is the reverse, looking for pull requests with the org-forks as BASE 
forks_made_by_orgs_with_pullrequests_forkasbase
*/
SELECT forktable.fork_organization AS fork_organization,
forktable.fork_url AS fork_url,
forktable.parent_url AS parent_url,
forktable.creation_date AS fork_creation,
PR.headurl AS HeadURL,
PR.baseurl AS BaseURL,
PR.DistinctPRUsers AS DistinctPRUsers,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr
FROM
	(SELECT payload_pull_request_head_repo_html_url AS headurl,
	payload_pull_request_base_repo_html_url AS baseurl,
	count(distinct(payload_pull_request_user_login)) AS DistinctPRUsers, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_head_repo_html_url != payload_pull_request_base_repo_html_url
	GROUP EACH BY headurl, baseurl)
AS PR
INNER JOIN EACH 
	(SELECT fork_organization,
	fork_url,
	parent_url,
	creation_date
	FROM [github_explore.forks_made_by_orgs])
AS forktable
ON PR.baseurl = forktable.fork_url
ORDER BY parent_url ASC


/* When others fork an organisation's repo do they tend to pull request back?
Table has rows only where the "fork_made_from_org" made a pull request as the head repo 
forks_made_from_orgs_with_pullrequests_forkashead
To analyse this a key filter is whether BaseURL == parent_url
*/
SELECT forktable.parent_organization AS parent_organization,
forktable.fork_url AS fork_url,
forktable.parent_url AS parent_url,
forktable.creation_date AS fork_creation,
PR.headurl AS HeadURL,
PR.baseurl AS BaseURL,
PR.DistinctPRUsers AS DistinctPRUsers,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr
FROM
	(SELECT payload_pull_request_head_repo_html_url AS headurl,
	payload_pull_request_base_repo_html_url AS baseurl,
	count(distinct(payload_pull_request_user_login)) AS DistinctPRUsers, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_head_repo_html_url != payload_pull_request_base_repo_html_url
	GROUP EACH BY headurl, baseurl)
AS PR
INNER JOIN EACH 
	(SELECT parent_organization,
	fork_url,
	parent_url,
	creation_date
	FROM [github_explore.forks_made_from_orgs])
AS forktable
ON PR.headurl = forktable.fork_url
ORDER BY parent_url ASC

/* When others fork an organisation's repo does that organisation ever pull request to the fork?
Table has rows only where the "fork_made_from_org" received a pull request as the base repo 
forks_made_from_orgs_with_pullrequests_forkasbase
To analyse this a key filter is whether BaseURL == parent_url
*/
SELECT forktable.parent_organization AS parent_organization,
forktable.fork_url AS fork_url,
forktable.parent_url AS parent_url,
forktable.creation_date AS fork_creation,
PR.headurl AS HeadURL,
PR.baseurl AS BaseURL,
PR.DistinctPRUsers AS DistinctPRUsers,
PR.Events,
PR.OpenEvents,
PR.CloseEvents,
PR.DistinctPullRequests,
PR.Merged,
PR.SelfMerges,
PR.first_pr,
PR.last_pr
FROM
	(SELECT payload_pull_request_head_repo_html_url AS headurl,
	payload_pull_request_base_repo_html_url AS baseurl,
	count(distinct(payload_pull_request_user_login)) AS DistinctPRUsers, 
	count(payload_pull_request_head_repo_url) AS Events,
	sum(IF(payload_action = 'opened', 1, 0)) AS OpenEvents,
	sum(IF(payload_action = 'closed', 1, 0)) AS CloseEvents,
	count(DISTINCT(payload_pull_request_id)) AS DistinctPullRequests,
	sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS Merged,
	sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0 )) AS SelfMerges,
	max(created_at) AS last_PR,
	min(created_at) AS first_PR,
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_head_repo_html_url != payload_pull_request_base_repo_html_url
	GROUP EACH BY headurl, baseurl)
AS PR
INNER JOIN EACH 
	(SELECT parent_organization,
	fork_url,
	parent_url,
	creation_date
	FROM [github_explore.forks_made_from_orgs])
AS forktable
ON PR.baseurl = forktable.fork_url
ORDER BY parent_url ASC

/* want to tack number of pushevents onto the forks in the above tables - to filter out no-activity repos*/
SELECT PR.parent_organization AS parent_organization,
PR.fork_url AS fork_url,
PR.parent_url AS parent_url,
PR.fork_creation AS fork_creation,
PR.HeadURL AS HeadURL,
PR.BaseURL AS BaseURL,
PR.DistinctPRUsers AS DistinctPRUsers,
PR.PR_Events AS PR_Events,
PR.PR_OpenEvents,
PR.PR_CloseEvents,
PR.PR_DistinctPullRequests,
PR.PR_Merged,
PR.PR_SelfMerges,
PR.PR_first_pr,
PR.PR_last_pr,
pushtable.Pushevents AS PushEvents,
pushtable.Pushers AS Pushers
FROM
	(SELECT parent_organization,
	fork_url,
	parent_url,
	fork_creation,
	HeadURL,
	BaseURL,
	DistinctPRUsers,
	PR_Events,
	PR_OpenEvents,
	PR_CloseEvents,
	PR_DistinctPullRequests,
	PR_Merged,
	PR_SelfMerges,
	PR_first_pr,
	PR_last_pr
	FROM [metacommunities:github_explore.forks_made_from_orgs_with_pullrequests_forkashead]
	)
AS PR
INNER JOIN EACH 
	(SELECT repository_url,
	count(repository_url) AS PushEvents,
	count(distinct(actor)) AS Pushers
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY repository_url)
AS pushtable
ON PR.HeadURL = pushtable.repository_url



/* add push info to forks_made_from_orgs */
SELECT tab.parent_organization AS parent_organization,
tab.fork_url AS fork_url,
tab.parent_url AS parent_url,
tab.creation_date AS creation_date,
pushtable.PushEvents AS ForkPushEvents,
pushtable.Pushers AS ForkPushers
FROM
	(SELECT parent_organization,
	fork_url,
	parent_url,
	creation_date
	FROM [metacommunities:github_explore.forks_made_from_orgs]
	)
AS tab
LEFT JOIN EACH 
	(SELECT repository_url,
	count(repository_url) AS PushEvents,
	count(distinct(actor)) AS Pushers
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY repository_url)
AS pushtable
ON tab.fork_url = pushtable.repository_url



/* add push info to forks_made_by_orgs */
SELECT tab.fork_organization AS fork_organization,
tab.fork_url AS fork_url,
tab.parent_url AS parent_url,
tab.creation_date AS creation_date,
pushtable.PushEvents AS ForkPushEvents,
pushtable.Pushers AS ForkPushers
FROM
	(SELECT fork_organization,
	fork_url,
	parent_url,
	creation_date
	FROM [metacommunities:github_explore.forks_made_by_orgs]
	)
AS tab
LEFT JOIN EACH 
	(SELECT repository_url,
	count(repository_url) AS PushEvents,
	count(distinct(actor)) AS Pushers
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY repository_url)
AS pushtable
ON tab.fork_url = pushtable.repository_url


/*Table which groups pushevents by user/repo/organisation */
SELECT actor, repository_url, repository_organization, count(actor) as Pushes, min(created_at) AS FirstPush, max(created_at) AS LastPush
FROM [github_explore.timeline]
WHERE repository_organization IS NOT NULL AND type = 'PushEvent'
GROUP EACH BY repository_organization, repository_url, actor
ORDER BY repository_organization


/* Summary of actors involvement (number of orgs, repos)  */
SELECT actor, count(distinct(repository_organization)) AS number_of_orgs, count(distinct(repository_url)) AS number_of_repos
FROM [metacommunities:github_explore.organizations_repos_pushers]
GROUP EACH BY actor
ORDER BY number_of_orgs DESC


/* Organisations mega-table
Base table*/
SELECT repository_organization, 
count(distinct(repository_name)) AS Repos, 
count(repository_organization) AS PushEvents, 
count(distinct(actor)) AS Pushers,
min(created_at) AS FirstPush,
max(created_at) AS LastPush,
count(distinct(repository_homepage)) AS repository_homepages,
count(distinct(repository_owner)) AS repository_owners,
count(distinct(repository_language)) AS repository_languages
FROM [githubarchive:github.timeline]
WHERE type = 'PushEvent'
GROUP EACH BY repository_organization
ORDER BY Repos DESC


/* Add WatchEvents */
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
new.WatchEvents AS WatchEvents
FROM
	(SELECT repository_organization,
	Repos,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	repository_homepages,
	repository_owners,
	repository_languages
	FROM [github_explore.organizations_1])
AS old
LEFT JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS WatchEvents 
	FROM [github_explore.timeline]
	WHERE type = 'WatchEvent' 
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC

/* Add ForkEvents */
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
new.ForkEvents AS ForkEvents
FROM
	(SELECT repository_organization,
	Repos,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents
	FROM [github_explore.organizations_2])
AS old
LEFT JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS ForkEvents
	FROM [github_explore.timeline]
	WHERE type = 'ForkEvent' 
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC


/* Add IssuesEvents */
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
new.IssuesEvents AS IssuesEvents
FROM
	(SELECT repository_organization,
	Repos,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents
	FROM [github_explore.organizations_3])
AS old
LEFT JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS IssuesEvents
	FROM [github_explore.timeline]
	WHERE type = 'IssuesEvent' 
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC

/* Add DownloadEvents */
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
old.IssuesEvents AS IssuesEvents,
new.DownloadEvents AS DownloadEvents
FROM
	(SELECT repository_organization,
	Repos,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents,
	IssuesEvents
	FROM [github_explore.organizations_4])
AS old
LEFT JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS DownloadEvents
	FROM [github_explore.timeline]
	WHERE type = 'DownloadEvent' 
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC

/* Add IssueCommentevents */
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
old.IssuesEvents AS IssuesEvents,
new.IssueCommentEvents AS IssueCommentEvents,
old.DownloadEvents AS DownloadEvents
FROM
	(SELECT repository_organization,
	Repos,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents,
	IssuesEvents,
	DownloadEvents
	FROM [github_explore.organizations_5])
AS old
LEFT JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS IssueCommentEvents
	FROM [github_explore.timeline]
	WHERE type = 'IssueCommentEvent' 
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC

/*Add PullRequests */
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
old.IssuesEvents AS IssuesEvents,
old.IssueCommentEvents AS IssueCommentEvents,
old.DownloadEvents AS DownloadEvents,
new.PullRequestsClosed AS PullRequestsClosed
FROM
	(SELECT repository_organization,
	Repos,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents,
	IssuesEvents,
	IssueCommentEvents,
	DownloadEvents
	FROM [github_explore.organizations_6])
AS old
LEFT JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS PullRequestsClosed
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_state = 'closed'
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC


/*Add duration */
SELECT repository_organization,
	Repos, 
	PushEvents, 
	Pushers, 
	FirstPush, 
	LastPush, 
	ceil((PARSE_UTC_USEC(LastPush) - PARSE_UTC_USEC(FirstPush))/86400000000) AS PushDurationDays, 
	repository_homepages, 
	repository_owners, 
	repository_languages, 
	WatchEvents, 
	ForkEvents, 
	IssuesEvents, 
	IssueCommentEvents, 
	DownloadEvents, 
	PullRequestsClosed 
	FROM [github_explore.organizations_megatable]

/*Add variables related to the organisation's repos being linked to from SO posts 
organizations_megatable3*/
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PushDurationDays AS PushDurationDays,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
old.IssuesEvents AS IssuesEvents,
old.IssueCommentEvents AS IssueCommentEvents,
old.DownloadEvents AS DownloadEvents,
old.PullRequestsClosed AS PullRequestsClosed,
new.ReposLinkedTo AS repos_linked_to,
new.posts_linking_to_orgs_repos AS posts_linking_to_orgs_repos,
new.answers_linking_to_orgs_repos AS answers_linking_to_orgs_repos
FROM
	(SELECT repository_organization,
	Repos,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	PushDurationDays,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents,
	IssuesEvents,
	IssueCommentEvents,
	DownloadEvents,
	PullRequestsClosed
	FROM [github_explore.organizations_megatable2])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_organization, 
	sum(if(repolink_Posts IS NOT NULL, 1, 0)) AS ReposLinkedTo,
	sum(repolink_Posts) AS posts_linking_to_orgs_repos,
	sum(repolink_answers) AS answers_linking_to_orgs_repos
	FROM [github_explore.orgs_repos_links_from_SO]
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC
	
	
/* Add a single repository_homepage_domain for each org
Problematic because it just picks the longest domain, and some orgs have several */




/* Add a column which joins on org domain and gets the number of post referencing it on Stackoverflow */
#this is on hold because "domains" are problematic



/* Add a column which sums the references to an organisation's repos on Stackoverflow and counts the number of distinct repos which are referenced */
#joins orgs_and_their_repos and github_repo_links, THEN join on the organisations megatable
#orgs_repos_links_from_SO
SELECT old.repository_organization AS repository_organization,
old.repo AS repo,
old.Events AS Events,
old.Pushes AS Pushes,
new.Pushers AS Pushers,
old.repository_homepage AS repository_homepage,
old.repository_homepage_domain AS repository_homepage_domain,
new.MaxWatchers AS MaxWatchers,
new.MaxForks AS MaxForks,
new.repolinkPosts AS repolink_Posts,
new.repolinkPosters AS repolink_Posters,
new.repolinkAnswers AS repolink_answers,
new.repolinkDistinctQuestions AS repolink_DistinctQuestions
FROM
	(SELECT repository_organization,
	repository_url,
	repo,
	Events,
	Pushes,
	repository_homepage,
	repository_homepage_domain
	FROM [github_explore.orgs_and_their_repos])
AS old
LEFT JOIN EACH 
	(SELECT repo,
	Pushers,
	MaxWatchers,
	MaxForks,
	repolinkPosts,
	repolinkPosters,
	repolinkAnswers,
	repolinkDistinctQuestions
	FROM [github_explore.repos_linked_to_from_SO])
AS new
ON new.repo = old.repo
ORDER BY repolink_Posts DESC




/* Add number of repos owned which are forks 
organizations_megatable4*/
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
new.ReposWhichAreForks AS ReposWhichAreForks,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PushDurationDays AS PushDurationDays,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
old.IssuesEvents AS IssuesEvents,
old.IssueCommentEvents AS IssueCommentEvents,
old.DownloadEvents AS DownloadEvents,
old.PullRequestsClosed AS PullRequestsClosed,
old.repos_linked_to AS repos_linked_to,
old.posts_linking_to_orgs_repos AS posts_linking_to_orgs_repos,
old.answers_linking_to_orgs_repos AS answers_linking_to_orgs_repos
FROM
	(SELECT repository_organization,
	Repos,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	PushDurationDays,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents,
	IssuesEvents,
	IssueCommentEvents,
	DownloadEvents,
	PullRequestsClosed,
	repos_linked_to,
	posts_linking_to_orgs_repos,
	answers_linking_to_orgs_repos
	FROM [github_explore.organizations_megatable3])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_organization, 
	sum(if(is_fork = 'true', 1, 0)) AS ReposWhichAreForks,
	FROM [github_explore.orgs_and_their_repos]
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC
	
	
/* Add Pullrequests merged 
organizations_megatable5 */	
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.ReposWhichAreForks AS ReposWhichAreForks,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PushDurationDays AS PushDurationDays,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
old.IssuesEvents AS IssuesEvents,
old.IssueCommentEvents AS IssueCommentEvents,
old.DownloadEvents AS DownloadEvents,
old.PullRequestsClosed AS PullRequestsClosed,
new.pullrequestsmerged AS PullRequestsMerged,
old.repos_linked_to AS repos_linked_to,
old.posts_linking_to_orgs_repos AS posts_linking_to_orgs_repos,
old.answers_linking_to_orgs_repos AS answers_linking_to_orgs_repos
FROM
	(SELECT repository_organization,
	Repos,
	ReposWhichAreForks,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	PushDurationDays,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents,
	IssuesEvents,
	IssueCommentEvents,
	DownloadEvents,
	PullRequestsClosed,
	repos_linked_to,
	posts_linking_to_orgs_repos,
	answers_linking_to_orgs_repos
	FROM [github_explore.organizations_megatable4])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS PullRequestsMerged
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_state = 'closed' AND payload_pull_request_merged = 'true'
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC
	
/* Query which generates the orgs sample for manual coding */
SELECT repository_organization, CONCAT('http://www.github.com/', repository_organization) FROM [github_explore.organizations_megatable4] WHERE (Pushers > 1 OR PushDurationDays > 30 OR WatchEvents > 0 OR ForkEvents > 0 OR PullRequestsClosed > 0 OR repos_linked_to > 0) AND PushDurationDays > 5 AND (HASH(repository_organization)%100 == 0) ORDER BY repository_organization ASC



/* Query which builds a table of events for the repos which have been featured in STackoverflow posts at least 100 times
stacked_repos_events
*/
SELECT repos.repo AS repo,
events.type as type,
events.created_at as created_at
FROM
	(SELECT SUBSTR(repository_url, 19, 500) AS repo,
	created_at,
	type
	FROM [github_explore.timeline])
AS events
INNER JOIN EACH 
	(SELECT repo
	FROM [github_explore.repos_linked_to_from_SO]
	WHERE repolinkPosts > 100)
AS repos
ON repos.repo = events.repo
ORDER BY created_at DESC


/*Similar table which picks out the relevant STackoverflow posts and their timestamps
stacked_repos_posts */
SELECT repos.repo AS repo,
events.CreationDate as created_at,
events.PostTypeId as PostType
FROM
	(SELECT REGEXP_EXTRACT(Body, "://github.com(/[^/\"]*/[^/^\"^\'^#^ ^<^)]*)") as repo,
	CreationDate,
	PostTypeId
	FROM [stack_overflow.Posts])
AS events
INNER JOIN EACH 
	(SELECT repo
	FROM [github_explore.repos_linked_to_from_SO]
	WHERE repolinkPosts > 100)
AS repos
ON repos.repo = events.repo
ORDER BY created_at DESC


/* The following is all work in progress, that doesn't work.
It concerns trying to pick out early events for organisations */

/* Add creation date for org to megatable - how?
No - get events for all orgs and sort out the creation dates locally with API data
Getting the first X events is not easy with group by... http://www.xaprb.com/blog/2006/12/07/how-to-select-the-firstleastmax-row-per-group-in-sql/
But its possible to do it by time maybe...
What about an OVER clause? Don't want to aggregate, but could use the DENSE_RANK
Can i do this in 2 steps... label all org events with an order variable, then select the relevant rows from that table? The first step exceeds resource limit on full timeline, but works on public sample
Can i trim the timeline down enough to make this manageable? 
*/

/* This is an attempt to build a smaller table to work with, but the smaller table is itself too large to return

It would work in chunks, can chunk by repository_created_at, save several tables, apply dense-rank to those tables then chop them down, then download everything locally and figure out which chunk to look at for each org

orgevents_temp1
*/
SELECT repository_organization, repository_url, type, created_at, repository_size, repository_created_at,
DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC) dense_rank,
FROM
   [github_explore.timeline]
WHERE
   repository_organization IS NOT NULL  AND repository_created_at > '2013-07-01 00:00:01'
   
   
/*orgevents_temp2 */
SELECT repository_organization, repository_url, type, created_at, repository_size, repository_created_at,
DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC) dense_rank,
FROM
   [github_explore.timeline]
WHERE
   repository_organization IS NOT NULL  AND repository_created_at <= '2013-07-01 00:00:01' AND repository_created_at > '2013-04-01 00:00:01' AND created_at <= '2013-08-01 00:00:01'
   
  /*orgevents_temp3 */
SELECT repository_organization, repository_url, type, created_at, repository_size, repository_created_at,
DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC) dense_rank,
FROM
   [github_explore.timeline]
WHERE
   repository_organization IS NOT NULL  AND repository_created_at <= '2013-04-01 00:00:01' AND repository_created_at > '2013-01-01 00:00:01' AND created_at <= '2013-05-01 00:00:01' 
   
  /*orgevents_temp4 */
SELECT repository_organization, repository_url, type, created_at, repository_size, repository_created_at,
DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC) dense_rank,
FROM
   [github_explore.timeline]
WHERE
   repository_organization IS NOT NULL  AND repository_created_at <= '2013-01-01 00:00:01' AND repository_created_at > '2012-08-01 00:00:01' AND created_at <= '2013-01-01 00:00:01'    
   
  /*orgevents_temp5 */
SELECT repository_organization, repository_url, type, created_at, repository_size, repository_created_at,
DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC) dense_rank,
FROM
   [github_explore.timeline]
WHERE
   repository_organization IS NOT NULL  AND repository_created_at <= '2012-08-01 00:00:01' AND repository_created_at > '2012-04-01 00:00:01' AND created_at <= '2012-09-01 00:00:01'   

/*orgevents_temp1_20 */
SELECT * from [github_explore.orgevents_temp1] WHERE dense_rank <= 20   

/*orgevents_temp2_20 */
SELECT * from [github_explore.orgevents_temp2] WHERE dense_rank <= 20   

/*orgevents_temp3_20 */
SELECT * from [github_explore.orgevents_temp3] WHERE dense_rank <= 20   

/*orgevents_temp4_20 */
SELECT * from [github_explore.orgevents_temp4] WHERE dense_rank <= 20   

/*orgevents_temp5_20 */
SELECT * from [github_explore.orgevents_temp5] WHERE dense_rank <= 20   

/*above misses out forks which were made BY the org - so when a repo's creation was a fork event this is excluded - can do all of the above tables in 1 for this, cut it off wherever the other tables are cut off
refer to url as repository_url because this will make it compatible with other tables
This needs to be done with a join on url and all urls from orgs_and_their_repos

orgforkevents_temp  */  
SELECT repos.repository_url AS repository_url,
repos.repository_organization as repository_organization,
forkevents.created_at AS created_at,
forkevents.forked_from AS forked_from,
forkevents.repository_owner AS repository_owner
FROM
	(SELECT repository_url,
	repository_organization
	FROM [github_explore.orgs_and_their_repos])
AS repos
INNER JOIN EACH 
	(SELECT url,
	created_at,
	repository_url AS forked_from,
	repository_owner,
	FROM [github_explore.timeline]
	WHERE type = "ForkEvent")
AS forkevents
ON forkevents.url = repos.repository_url
ORDER BY repository_organization DESC


/*this attempt is broken because its still based on repository_organization */
 SELECT repository_organization, url AS repository_url, type, created_at, repository_size, repository_created_at,
DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC) dense_rank,
FROM
   [github_explore.timeline]
WHERE
   repository_organization IS NOT NULL AND type = 'ForkEvent' AND repository_created_at > '2012-04-01 00:00:01'
   
   
 
  /*orgevents_temp2ranks */
SELECT
   repository_organization,
   repository_url,
   type,
   repository_size,
   created_at,
   DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC) dense_rank,
FROM
   [github_explore.orgevents_temp2] 
   
 
/*this works on the sample table but exceeds resource limit on proper table */ 
SELECT
   repository_organization,
   repository_url,
   type,
   payload_id,
   created_at,
   DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC) dense_rank,
FROM
   [publicdata:samples.github_timeline]
WHERE
   repository_organization IS NOT NULL  





/*this doesnt work because the limit applies too broadly */
SELECT old.repository_organization AS repository_organization,
new.created_at AS created_at,
new.type AS type
FROM
	(SELECT repository_organization
	FROM [github_explore.organizations_megatable5])
AS old
INNER JOIN EACH 
	(SELECT repository_organization, 
	created_at,
	type
	FROM [github_explore.timeline]
/*	ORDER BY repository_organization ASC, created_at DESC */
	LIMIT 20
)
AS new
ON new.repository_organization = old.repository_organization



SELECT repository_organization, 
	created_at,
	type
	FROM [github_explore.timeline]
	WHERE created_at > min(created_at)  
	GROUP EACH BY repository_organization


SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.ReposWhichAreForks AS ReposWhichAreForks,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PushDurationDays AS PushDurationDays,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
old.IssuesEvents AS IssuesEvents,
old.IssueCommentEvents AS IssueCommentEvents,
old.DownloadEvents AS DownloadEvents,
old.PullRequestsClosed AS PullRequestsClosed,
old.pullrequestsmerged AS PullRequestsMerged,
old.repos_linked_to AS repos_linked_to,
old.posts_linking_to_orgs_repos AS posts_linking_to_orgs_repos,
old.answers_linking_to_orgs_repos AS answers_linking_to_orgs_repos
FROM
	(SELECT repository_organization,
	Repos,
	ReposWhichAreForks,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	PushDurationDays,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents,
	IssuesEvents,
	IssueCommentEvents,
	DownloadEvents,
	PullRequestsClosed,
	PullRequestsMerged,
	repos_linked_to,
	posts_linking_to_orgs_repos,
	answers_linking_to_orgs_repos
	FROM [github_explore.organizations_megatable5])
AS old
INNER JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS Events24hr,
	min(created_at) AS FirstEvent,
	FROM [github_explore.timeline]
	WHERE (DENSE_RANK() OVER (PARTITION BY repository_organization ORDER BY created_at ASC)) <= 20 )
AS new
ON new.repository_organization = old.repository_organization
ORDER BY Repos DESC



SELECT repository_url, actor, count(*) as pushes FROM [github_explore.timeline] 
WHERE type = 'PushEvent'
GROUP EACH BY repository_url, actor
ORDER BY pushes desc




/*creating a repo typology table - will involve joining several tables...
start with the maximum possible table, group by repo_url and include all events with sum(if) to get specific counts, then add in the pullrequests information
Can't return all repos, needs to be done in chunks
all_repos_1
*/
SELECT repository_url, max(repository_owner) AS owner, max(repository_organization) AS organization, max(repository_language) AS language, min(repository_created_at) AS repo_created,
max(repository_fork) AS Fork,
max(repository_watchers) AS Watchers,
max(repository_forks) AS Forks,
count(repository_url) AS Pushes,
count(distinct(actor)) AS Pushers,
min(created_at) AS FirstPush,
max(created_at) AS LastPush
FROM [github_explore.timeline] 
WHERE repository_created_at > '2013-06-01 00:00:01' AND type = 'PushEvent'
GROUP EACH BY repository_url
ORDER BY owner ASC



/*join with pullrequest info
all_repos_1_1
*/

SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
new.PR_Received AS PR_Received,
new.FirstPR AS FirstPR,
new.LastPR AS LastPR
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush
	FROM [github_explore.all_repos_1])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_base_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_received, min(created_at) AS FirstPR, max(created_at) AS LastPR
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url != payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_base_repo_html_url)
AS new
ON new.payload_pull_request_base_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/*join with pullrequest info - made
all_repos_1_2
*/
SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PR_Received AS PR_Received,
old.FirstPR AS FirstPR,
old.LastPR AS LastPR,
new.PR_issued AS PR_Issued,
new.FirstPRissued AS FirstPRissued,
new.LastPRissued AS LastPRissued
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush,
	PR_Received,
	FirstPR,
	LastPR
	FROM [github_explore.all_repos_1_1])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_head_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_issued, min(created_at) AS FirstPRissued, max(created_at) AS LastPRissued
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url != payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_head_repo_html_url)
AS new
ON new.payload_pull_request_head_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/* add intra repo pull requests
all_repos_1_3*/
SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PR_Received AS PR_Received,
old.FirstPR AS FirstPR,
old.LastPR AS LastPR,
old.PR_issued AS PR_Issued,
old.FirstPRissued AS FirstPRissued,
old.LastPRissued AS LastPRissued,
new.PR_intra AS PR_intra
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush,
	PR_Received,
	FirstPR,
	LastPR,
	PR_Issued,
	FirstPRissued,
	LastPRissued
	FROM [github_explore.all_repos_1_2])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_head_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_intra
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url = payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_head_repo_html_url)
AS new
ON new.payload_pull_request_head_repo_html_url = old.repository_url
ORDER BY Pushes DESC


/* all_repos_2 */
SELECT repository_url, max(repository_owner) AS owner, max(repository_organization) AS organization, max(repository_language) AS language, min(repository_created_at) AS repo_created,
max(repository_fork) AS Fork,
max(repository_watchers) AS Watchers,
max(repository_forks) AS Forks,
count(repository_url) AS Pushes,
count(distinct(actor)) AS Pushers,
min(created_at) AS FirstPush,
max(created_at) AS LastPush
FROM [github_explore.timeline] 
WHERE repository_created_at > '2013-01-01 00:00:01' AND repository_created_at <= '2013-06-01 00:00:01' AND type = 'PushEvent'
GROUP EACH BY repository_url
ORDER BY owner ASC



/*join with pullrequest info
all_repos_2_1
*/

SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
new.PR_Received AS PR_Received,
new.FirstPR AS FirstPR,
new.LastPR AS LastPR
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush
	FROM [github_explore.all_repos_2])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_base_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_received, min(created_at) AS FirstPR, max(created_at) AS LastPR
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url != payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_base_repo_html_url)
AS new
ON new.payload_pull_request_base_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/*join with pullrequest info - made
all_repos_2_2
*/
SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PR_Received AS PR_Received,
old.FirstPR AS FirstPR,
old.LastPR AS LastPR,
new.PR_issued AS PR_Issued,
new.FirstPRissued AS FirstPRissued,
new.LastPRissued AS LastPRissued
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush,
	PR_Received,
	FirstPR,
	LastPR
	FROM [github_explore.all_repos_2_1])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_head_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_issued, min(created_at) AS FirstPRissued, max(created_at) AS LastPRissued
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url != payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_head_repo_html_url)
AS new
ON new.payload_pull_request_head_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/* add intra repo pull requests
all_repos_2_3*/
SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PR_Received AS PR_Received,
old.FirstPR AS FirstPR,
old.LastPR AS LastPR,
old.PR_issued AS PR_Issued,
old.FirstPRissued AS FirstPRissued,
old.LastPRissued AS LastPRissued,
new.PR_intra AS PR_intra
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush,
	PR_Received,
	FirstPR,
	LastPR,
	PR_Issued,
	FirstPRissued,
	LastPRissued
	FROM [github_explore.all_repos_2_2])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_head_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_intra
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url = payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_head_repo_html_url)
AS new
ON new.payload_pull_request_head_repo_html_url = old.repository_url
ORDER BY Pushes DESC



/* all_repos_3 */
SELECT repository_url, max(repository_owner) AS owner, max(repository_organization) AS organization, max(repository_language) AS language, min(repository_created_at) AS repo_created,
max(repository_fork) AS Fork,
max(repository_watchers) AS Watchers,
max(repository_forks) AS Forks,
count(repository_url) AS Pushes,
count(distinct(actor)) AS Pushers,
min(created_at) AS FirstPush,
max(created_at) AS LastPush
FROM [github_explore.timeline] 
WHERE repository_created_at > '2012-06-01 00:00:01' AND repository_created_at <= '2013-01-01 00:00:01' AND type = 'PushEvent'
GROUP EACH BY repository_url
ORDER BY owner ASC



/*join with pullrequest info
all_repos_3_1
*/

SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
new.PR_Received AS PR_Received,
new.FirstPR AS FirstPR,
new.LastPR AS LastPR
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush
	FROM [github_explore.all_repos_3])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_base_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_received, min(created_at) AS FirstPR, max(created_at) AS LastPR
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url != payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_base_repo_html_url)
AS new
ON new.payload_pull_request_base_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/*join with pullrequest info - made
all_repos_3_2
*/
SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PR_Received AS PR_Received,
old.FirstPR AS FirstPR,
old.LastPR AS LastPR,
new.PR_issued AS PR_Issued,
new.FirstPRissued AS FirstPRissued,
new.LastPRissued AS LastPRissued
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush,
	PR_Received,
	FirstPR,
	LastPR
	FROM [github_explore.all_repos_3_1])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_head_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_issued, min(created_at) AS FirstPRissued, max(created_at) AS LastPRissued
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url != payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_head_repo_html_url)
AS new
ON new.payload_pull_request_head_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/* add intra repo pull requests
all_repos_3_3*/
SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PR_Received AS PR_Received,
old.FirstPR AS FirstPR,
old.LastPR AS LastPR,
old.PR_issued AS PR_Issued,
old.FirstPRissued AS FirstPRissued,
old.LastPRissued AS LastPRissued,
new.PR_intra AS PR_intra
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush,
	PR_Received,
	FirstPR,
	LastPR,
	PR_Issued,
	FirstPRissued,
	LastPRissued
	FROM [github_explore.all_repos_3_2])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_head_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_intra
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url = payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_head_repo_html_url)
AS new
ON new.payload_pull_request_head_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/* this one is for the power time graph, it gets repos created before timeline or early timeline
all_repos_4
*/
SELECT repository_url, max(repository_owner) AS owner, max(repository_organization) AS organization, max(repository_language) AS language, min(repository_created_at) AS repo_created,
max(repository_fork) AS Fork,
max(repository_watchers) AS Watchers,
max(repository_forks) AS Forks,
count(repository_url) AS Pushes,
count(distinct(actor)) AS Pushers,
min(created_at) AS FirstPush,
max(created_at) AS LastPush
FROM [github_explore.timeline] 
WHERE repository_created_at <= '2012-06-01 00:00:01' AND type = 'PushEvent'
GROUP EACH BY repository_url
ORDER BY Pushes DESC

/*join with pullrequest info
all_repos_4_1
*/

SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
new.PR_Received AS PR_Received,
new.FirstPR AS FirstPR,
new.LastPR AS LastPR
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush
	FROM [github_explore.all_repos_4])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_base_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_received, min(created_at) AS FirstPR, max(created_at) AS LastPR
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url != payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_base_repo_html_url)
AS new
ON new.payload_pull_request_base_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/*join with pullrequest info - made
all_repos_4_2
*/
SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PR_Received AS PR_Received,
old.FirstPR AS FirstPR,
old.LastPR AS LastPR,
new.PR_issued AS PR_Issued,
new.FirstPRissued AS FirstPRissued,
new.LastPRissued AS LastPRissued
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush,
	PR_Received,
	FirstPR,
	LastPR
	FROM [github_explore.all_repos_4_1])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_head_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_issued, min(created_at) AS FirstPRissued, max(created_at) AS LastPRissued
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url != payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_head_repo_html_url)
AS new
ON new.payload_pull_request_head_repo_html_url = old.repository_url
ORDER BY Pushes DESC

/* add intra repo pull requests
all_repos_4_3*/
SELECT old.repository_url AS repository_url,
old.owner AS owner,
old.organization AS organization,
old.language AS language,
old.repo_created AS repo_created,
old.Fork AS Fork,
old.Watchers AS Watchers,
old.Forks AS Forks,
old.Pushes AS Pushes,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PR_Received AS PR_Received,
old.FirstPR AS FirstPR,
old.LastPR AS LastPR,
old.PR_issued AS PR_Issued,
old.FirstPRissued AS FirstPRissued,
old.LastPRissued AS LastPRissued,
new.PR_intra AS PR_intra
FROM
	(SELECT repository_url,
	owner,
	organization,
	language,
	repo_created,
	Fork,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	FirstPush,
	LastPush,
	PR_Received,
	FirstPR,
	LastPR,
	PR_Issued,
	FirstPRissued,
	LastPRissued
	FROM [github_explore.all_repos_4_2])
AS old
OUTER LEFT JOIN EACH 
	(SELECT payload_pull_request_head_repo_html_url, count(distinct(payload_pull_request_id)) AS PR_intra
	FROM [github_explore.timeline]
	WHERE type = 'PullRequestEvent' AND payload_pull_request_base_repo_html_url = payload_pull_request_head_repo_html_url
	GROUP EACH BY payload_pull_request_head_repo_html_url)
AS new
ON new.payload_pull_request_head_repo_html_url = old.repository_url
ORDER BY Pushes DESC


/* find orphaned repos 
first find repo create events
repo_creations_1*/
SELECT repository_url, max(repository_created_at) AS repository_created_at
FROM [github_explore.timeline] WHERE type = 'CreateEvent' AND payload_ref_type = 'repository' AND created_at > '2013-03-01 00:00:01'
GROUP BY repository_url


/* repo_creations_2 */
SELECT repository_url, max(repository_created_at) AS repository_created_at
FROM [github_explore.timeline] WHERE type = 'CreateEvent' AND payload_ref_type = 'repository' AND created_at <= '2013-03-01 00:00:01'
GROUP BY repository_url


/* join on pushevents to see if they have pushes 
repo_creations_1_1*/
SELECT old.repository_url AS repository_url,
old.repository_created_at AS repository_created_at,
new.Pushes AS Pushes
FROM
	(SELECT repository_url,
	repository_created_at
	FROM [github_explore.repo_creations_1])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, count(repository_url) AS Pushes
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY repository_url)
AS new
ON new.repository_url = old.repository_url
ORDER BY Pushes DESC

/* join on events to see if they have events
repo_creations_1_events*/
SELECT old.repository_url AS repository_url,
old.repository_created_at AS repository_created_at,
new.Events AS Events
FROM
	(SELECT repository_url,
	repository_created_at
	FROM [github_explore.repo_creations_1])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, count(repository_url) AS Events
	FROM [github_explore.timeline]
	WHERE type != 'CreateEvent'
	GROUP EACH BY repository_url)
AS new
ON new.repository_url = old.repository_url
ORDER BY Events DESC

/* join on pushevents to see if they have pushes 
repo_creations_2_1*/
SELECT old.repository_url AS repository_url,
old.repository_created_at AS repository_created_at,
new.Pushes AS Pushes
FROM
	(SELECT repository_url,
	repository_created_at
	FROM [github_explore.repo_creations_2])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, count(repository_url) AS Pushes
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY repository_url)
AS new
ON new.repository_url = old.repository_url
ORDER BY Pushes DESC

/* join on events to see if they have events
repo_creations_2_events*/
SELECT old.repository_url AS repository_url,
old.repository_created_at AS repository_created_at,
new.Events AS Events
FROM
	(SELECT repository_url,
	repository_created_at
	FROM [github_explore.repo_creations_2])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, count(repository_url) AS Events
	FROM [github_explore.timeline]
	WHERE type != 'CreateEvent'
	GROUP EACH BY repository_url)
AS new
ON new.repository_url = old.repository_url
ORDER BY Events DESC

/* Same as above but for forks 
fork_creations*/
SELECT url AS fork_url, max(created_at) AS created_at
FROM [github_explore.timeline] WHERE type = 'ForkEvent' 
GROUP BY fork_url

/* Join to get pushes */
SELECT old.fork_url AS fork_url,
old.created_at AS created_at,
new.Pushes AS Pushes
FROM
	(SELECT fork_url,
	created_at
	FROM [github_explore.fork_creations])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, count(repository_url) AS Pushes
	FROM [github_explore.timeline]
	WHERE type = 'PushEvent'
	GROUP EACH BY repository_url)
AS new
ON new.repository_url = old.fork_url
ORDER BY Pushes DESC


/* Join to get all other event types (potentially problematic) */
SELECT old.fork_url AS fork_url,
old.created_at AS created_at,
new.Events AS Events
FROM
	(SELECT fork_url,
	created_at
	FROM [github_explore.fork_creations])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, count(repository_url) AS Events
	FROM [github_explore.timeline]
	GROUP EACH BY repository_url)
AS new
ON new.repository_url = old.fork_url
ORDER BY Events DESC



/*check pushevent rows against unique hashes 
distinctpushes_2012
in the 2012 set around half of rows are duplicates, in 2013 set there's no clear issue (although something weird is going on with the number of distinct hashes being greater than the number of rows)
*/
SELECT repository_url, count(repository_url) AS Pushes, count(distinct(payload_commit_id)) AS DistinctPushes 
FROM [github_explore.timeline] 
WHERE created_at > '2012-06-01 00:00:01' AND created_at <= '2012-10-01 00:00:01' AND type = 'PushEvent'
GROUP EACH BY repository_url
ORDER BY Pushes DESC

SELECT repository_url, count(repository_url) AS Pushes, count(distinct(payload_commit_id)) AS DistinctPushes 
FROM [github_explore.timeline] 
WHERE created_at > '2013-06-01 00:00:01' AND created_at <= '2013-10-01 00:00:01' AND type = 'PushEvent'
GROUP EACH BY repository_url
ORDER BY Pushes DESC


/*trying to investigate the "event overload" further 
when was it happening? push rows and distinct hashes by day*/
SELECT date(created_at) AS date, count(created_at) AS Pushes, count(distinct(payload_commit_id)) AS DistinctPushes
FROM [github_explore.timeline] 
WHERE type = 'PushEvent'
GROUP BY date
ORDER BY date






SELECT repository_url, max(repository_owner) AS owner, max(repository_organization) AS organization, max(repository_language) AS language, min(repository_created_at) AS repo_created,
max(repository_fork) AS Fork,
max(repository_watchers) AS Watchers,
max(repository_forks) AS Forks,
count(repository_url) AS Pushes,
count(distinct(actor)) AS Pushers,
min(created_at) AS FirstPush,
max(created_at) AS LastPush
FROM [github_explore.timeline] 
WHERE repository_created_at > '2012-06-01 00:00:01' AND repository_created_at <= '2013-01-01 00:00:01' AND type = 'PushEvent'
GROUP EACH BY repository_url
ORDER BY owner ASC




/* Finding significant events through accumulation of Watchers
Base this on the Social Repo type - create a new table with monthly or weekly watcher counts for these repos
allrepos_1_social
*/
SELECT * FROM [github_explore.all_repos_1_3] WHERE Watchers > 50 OR Forks > 50;


/* run this in R to get new Watches by day for repos */
SELECT old.repository_url AS repository_url,
old.repo_created AS repo_created,
new.date AS date,
new.Watches AS Watches
FROM
	(SELECT repository_url,
	repo_created
	FROM [github_explore.allrepos_1_social])
AS old
INNER JOIN EACH 
	(SELECT repository_url, 
	date(created_at) AS date,
	count(repository_url) AS Watches
	FROM [github_explore.timeline]
	WHERE type = 'WatchEvent'
	GROUP EACH BY repository_url, date)
AS new
ON new.repository_url = old.repository_url
ORDER BY repository_url DESC



/*going back to pull requests 
PR_relationships_all*/
SELECT payload_pull_request_base_repo_url, payload_pull_request_head_repo_url, count(payload_pull_request_head_repo_url) AS pullrequestevents, 
min(created_at) AS firstPR, max(created_at) as lastPR, count(distinct(payload_pull_request_id)) AS DistinctPullRequests, 
sum(if(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
(max(PARSE_UTC_USEC(created_at)) - min(PARSE_UTC_USEC(created_at)))/86400000000 AS PRDurationDays,
FROM [githubarchive:github.timeline]
WHERE type = "PullRequestEvent"  AND payload_pull_request_head_repo_url != payload_pull_request_base_repo_url
GROUP EACH BY  payload_pull_request_head_repo_url, payload_pull_request_base_repo_url
ORDER BY pullrequestevents DESC



/* Add Number of Releases to orgs megatable
org_ultimate_1
*/
SELECT old.repository_organization AS repository_organization,
old.Repos AS Repos,
old.ReposWhichAreForks AS ReposWhichAreForks,
old.PushEvents AS PushEvents,
old.Pushers AS Pushers,
old.FirstPush AS FirstPush,
old.LastPush AS LastPush,
old.PushDurationDays AS PushDurationDays,
old.repository_homepages AS repository_homepages,
old.repository_owners AS repository_owners,
old.repository_languages AS repository_languages,
old.WatchEvents AS WatchEvents,
old.ForkEvents AS ForkEvents,
old.IssuesEvents AS IssuesEvents,
old.IssueCommentEvents AS IssueCommentEvents,
new.ReleaseEvents AS ReleaseEvents,
old.DownloadEvents AS DownloadEvents,
old.PullRequestsClosed AS PullRequestsClosed,
old.pullrequestsmerged AS PullRequestsMerged,
old.SO_repos_linked_to AS SO_repos_linked_to,
old.SO_posts_linking_to_orgs_repos AS SO_posts_linking_to_orgs_repos,
old.SO_answers_linking_to_orgs_repos AS SO_answers_linking_to_orgs_repos,
old.org_created AS org_created,
old.blog AS blog,
old.FirstEvent AS FirstEvent,
old.EarlyEvents AS EarlyEvents,
old.MinsTo20Events AS MinsTo20Events,
old.First20_Creates AS First20_Creates,
old.First20_Forks AS First20_Forks,
old.First20_Pushes AS First20_Pushes,
old.First20_WatchEvents AS First20_WatchEvents,
old.First20_IssueEvents AS First20_IssueEvents,
old.First20_PullRequests AS First20_PullREquests,
old.First20_DistinctRepos AS First20_DistinctRepos,
old.First20_OtherEvents AS First20_OtherEvents,
old.Event20Time AS Event20Time
FROM
	(SELECT repository_organization,
	Repos,
	ReposWhichAreForks,
	PushEvents,
	Pushers,
	FirstPush,
	LastPush,
	PushDurationDays,
	repository_homepages,
	repository_owners,
	repository_languages,
	WatchEvents,
	ForkEvents,
	IssuesEvents,
	IssueCommentEvents,
	DownloadEvents,
	PullRequestsClosed,
	PullRequestsMerged,
	SO_repos_linked_to,
	SO_posts_linking_to_orgs_repos,
	SO_answers_linking_to_orgs_repos,
	org_created,
	blog,
	FirstEvent,
	EarlyEvents,
	MinsTo20Events,
	First20_Creates,
	First20_Forks,
	First20_Pushes,
	First20_WatchEvents,
	First20_IssueEvents,
	First20_PullRequests,
	First20_DistinctRepos,
	First20_OtherEvents,
	Event20Time
	FROM [github_proper.org_ultimate])
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_organization, 
	count(repository_organization) AS ReleaseEvents
	FROM [github_explore.timeline]
	WHERE type = 'ReleaseEvent'
	GROUP EACH BY repository_organization)
AS new
ON new.repository_organization = old.repository_organization
ORDER BY repository_organization ASC


/* table for looking at repo ownership profiles 
repo_ownership
*/
SELECT owner, type, count(type) AS owned FROM [github_proper.repo_type] GROUP BY owner, type ORDER BY owner ASC, type ASC


/* table for looking at watcher growth profiles */
SELECT
old.repository_url AS repository_url,
new.date AS date,
new.Watches AS watches
FROM
	(SELECT repository_url
	FROM [github_proper.repo_type] WHERE Watchers > 200)
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, 
	date(created_at) AS date,
	count(repository_url) AS Watches
	FROM [githubarchive:github.timeline]
	WHERE type = 'WatchEvent' AND created_at > '2012-09-17 00:00:00'	
	GROUP EACH BY repository_url, date)
AS new
ON new.repository_url = old.repository_url
ORDER BY repository_url ASC, date ASC



SELECT repository_url, 
	date(created_at) AS date,
	count(repository_url) AS Watches
	FROM [githubarchive:github.timeline]
	WHERE type = 'WatchEvent' AND repository_url = '", r, "' AND created_at > '2012-09-17 00:00:00'
	GROUP EACH BY repository_url, date", sep = "")

	
/* facebook_forks */
SELECT url FROM [github_explore.timeline] WHERE repository_owner = 'facebook' AND type = 'ForkEvent' GROUP BY url

/* link to repo_types */

SELECT
old.url AS repository_url,
new.organization AS organization,
new.repo_created AS repo_created,
new.Watchers AS Watchers,
new.Forks AS Forks,
new.Pushes AS Pushes,
new.Pushers AS Pushers,
new.LastPush AS LastPush,
new.PR_Received AS PR_Received,
new.PR_Issued AS PR_Issued,
new.PushDuration AS PushDuration,
new.type AS type
FROM
	(SELECT url
	FROM [github_explore.facebook_forks] )
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, 
	organization,
	repo_created,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	LastPush,
	PR_Received,
	PR_Issued,
	PushDuration,
	type
	FROM [github_proper.repo_type] 
	)
AS new
ON new.repository_url = old.url
ORDER BY repo_created ASC



/* twitter_forks */
SELECT url FROM [github_explore.timeline] WHERE repository_owner = 'twitter' AND type = 'ForkEvent' GROUP BY url;


SELECT
old.url AS repository_url,
new.organization AS organization,
new.repo_created AS repo_created,
new.Watchers AS Watchers,
new.Forks AS Forks,
new.Pushes AS Pushes,
new.Pushers AS Pushers,
new.LastPush AS LastPush,
new.PR_Received AS PR_Received,
new.PR_Issued AS PR_Issued,
new.PushDuration AS PushDuration,
new.type AS type
FROM
	(SELECT url
	FROM [github.twitter_forks] )
AS old
OUTER LEFT JOIN EACH 
	(SELECT repository_url, 
	organization,
	repo_created,
	Watchers,
	Forks,
	Pushes,
	Pushers,
	LastPush,
	PR_Received,
	PR_Issued,
	PushDuration,
	type
	FROM [github_proper.repo_type] 
	)
AS new
ON new.repository_url = old.url
ORDER BY repo_created ASC
	

/* how many repos are owned by orgsnisations */
SELECT
count(new.owner)
FROM
	(SELECT repository_organization
	FROM [github_proper.org_ultimate_1] )
AS old
INNER JOIN EACH 
	(SELECT owner
	FROM [github_proper.repo_list] 
	)
AS new
ON new.owner = old.repository_organization

	
-- test of virtualization comments
SELECT repository_name, type, created_at, payload_commit, payload_commit_msg FROM [githubarchive:github.timeline] 
where payload_commit_msg != "null" and regexp_match(payload_commit_msg, 'virtualiz') limit 10


/* how many distinct actors and repositories are on gh */

SELECT  count(distinct(actor)) as number_of_actors, count(distinct(repository_url)) AS number_of_repos
FROM  [githubarchive:github.timeline]

/* to find all the copies of bootstrap, not just forks -- but imitations
that use the name */

SELECT repository_url, repository_name, created_at
FROM [githubarchive:github.timeline] \nwhere type='ForkEvent' and
lower(repository_name) contains 'bootstrap'\norder by created_at asc LIMIT 20000
