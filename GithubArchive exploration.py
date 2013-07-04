# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Repositories by event histories: top 100
# 
# A simple way to gauge the importance of github repositories is just by counting sheer number of events. (There is a 'mistake' in this approach, but potentially an interesting one.)

# <codecell>

import google_bigquery_access as gbq
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# <codecell>

query  = """SELECT repository_name, RepoEvents
FROM
(
    SELECT repository_name, COUNT(repository_name) AS RepoEvents
    FROM [githubarchive:github.timeline]
    GROUP BY repository_name
) MyTable
GROUP BY RepoEvents, repository_name
ORDER BY RepoEvents DESC
limit 100;"""

 
results_df = gbq.query_table(query, max_rows=5000)

# <codecell>

results_df

# <markdowncell>

# Some interesting entries in this list. Quite a few of the top repos are just test repos (try-git, test, Test). Some are major projects like the Eclipse software development environment, Mozilla, Moodle, linux, or rails, a Ruby web framework. Others are a bit more surprising, like the [Khan Academy](https://www.khanacademy.org/) Exercises or TrinityCore, a game server, or Euro2012. Or number 33: 'pulWifi shows the default password of some wireless networks'.  Can this repo really be more active than mozilla-central or do we need to distinguish what kinds of events are occurring in it? 
# 
# ## Repository importance judged by push events
# 
# Running a similar query but now just looking at PushEvents. Maybe these give a different idea of repo activity?

# <codecell>

query = """
SELECT repository_name, RepoEvents
FROM
(
    SELECT repository_name, COUNT(repository_name) AS RepoEvents
    FROM [githubarchive:github.timeline]
    WHERE type = 'PushEvent'
    GROUP BY repository_name
) MyTable
GROUP BY RepoEvents, repository_name
ORDER BY RepoEvents DESC
limit 100;

"""
push_results_df = gbq.query_table(query, max_rows=5000)

# <codecell>

push_results_df

# <markdowncell>

# The ordering changes here, although many of the same repo names appear. But that's an important point. There is no single test repository, but quite a few repositories called 'test' or 'thesis' or 'scripts' or 'android' or 'rails'. Obviously repos can have the same name. 

# <markdowncell>

# ## Repos without the same name
# 
# The problem with querying by repository name is the duplication of names. We can avoid the duplicates by using the repository_url instead of the repository name. The query for that is shown below (still just looking at PushEvents).

# <codecell>

query2  = """SELECT repository_name, repository_url, count(repository_name) as RepoEvents
FROM [githubarchive:github.timeline]
WHERE type = 'PushEvent' OR type = 'ForkEvent'
GROUP BY repository_name, repository_url
ORDER BY RepoEvents DESC
limit 100;"""

repos_dedup_df = gbq.query_table(query2, max_rows=5000)

# <codecell>

repos_dedup_df

# <markdowncell>

# This does clear out all the 'test', 'core' or 'android' sites, and also leaves some surprising results. The top two repos by pushes and forks are 'websites' and 'euro2012.' Both repositories do not currently exist on github. What happened to them? (It could be worth looking at the delete repo events?) 
# 
# The first proper repo is 'llvm', a highly recognised compiler-virtual machine project that was awarded the 2012 ACM Software System Award.

# <markdowncell>

# ## Repos with the same name
# 
# But maybe the copying of repo names would be a useful lead for us in tracking metacommunity dynamics. This is similar to tracking the fork/pull-request dynamics, but via a looser coupling. Commonly used repo names might designate _prototypes_ for repositories more generally. For instance, one of the top repo names in the PushEvents query shown above was 'dotfiles.' An exploration of 'dotfile(s)' repos might tell us something about code editing practices. 

# <codecell>

query4  = """SELECT repository_name, repository_url, count(repository_name) as RepoEvents
FROM [githubarchive:github.timeline]
WHERE type = 'PushEvent' AND REGEXP_MATCH(repository_name, 'dotfile(s?)')
GROUP BY repository_name, repository_url
ORDER BY RepoEvents DESC;"""

dotfiles_df = gbq.query_table(query4, 100)


# <codecell>

query5  = """ SELECT count(repository_url) from [githubarchive:github.timeline]
where type = 'CreateEvent' AND REGEXP_MATCH(repository_name, 'dotfiles?')"""

dotfile_repo_count = gbq.query_table(query5)

# <codecell>

print dotfile_repo_count.f0_

# <markdowncell>

# This suggests that around 55,000 repositories are concerned with 'dotfile(s)' for code editors such as vim, emacs, etc. Many other versions of 'dotfiles' can be found. Repo names that begin with '.' are often configuration files for code editors or command line shells (bash, zsh, etc). A more sophisticated search might just track repositories that concern coding practices. This would perhaps give some lead on how _practices_ of coding move around in the code commons. 

# <codecell>

dotfiles_df

# <markdowncell>

# Similar 'prototype' repos might also be found with names like 'website(s)' or 'android'.
# 
# It might also be worth looking at the 'forkiness' of these generically named repos. 
# Are they more commonly forked than more specific repositories?

# <markdowncell>

# # Repositories by forks and pull requests
# 

# <codecell>

query5 = """SELECT payload_pull_request_base_repo_url, repository_name,
count(payload_pull_request_base_repo_url) as PullRequestEvents, 
count(distinct(payload_pull_request_id)) as DistinctPullRequests,
sum(IF(payload_action = 'opened', 1, 0)) AS PullRequestOpenEvents,
sum(IF(payload_pull_request_head_repo_url == payload_pull_request_base_repo_url AND payload_action = 'opened', 1, 0)) AS IntraRepoPullRequestOpenEvents,
sum(IF(payload_pull_request_merged == 'true', 1, 0)) AS MergedPullRequests,
count(distinct(payload_pull_request_merged_by_login)) AS UsersWhoMerge,
sum(IF(payload_pull_request_merged_by_login == payload_pull_request_user_login, 1, 0)) AS PullRequestMergedBySameUser,
FROM [github_explore.timeline]
WHERE type = 'PullRequestEvent' 
GROUP BY payload_pull_request_base_repo_url, repository_name
ORDER BY PullRequestEvents DESC"""

fork_pull_df = gbq.query_table(query5, 400)

# <codecell>

fork_pull_df.repository_name

