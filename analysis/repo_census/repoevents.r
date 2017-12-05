library(ggplot2)
library(dplyr)
library(bigrquery)


ev = read.csv('data/repo_event_counts_top1000.csv')
evf = read.csv('data/repo_event_counts_top1000_fork_repos.csv')
ev$CumFreq = cumsum(ev$Freq)
evf$CumFreq = cumsum(evf$Freq)
evf$Fork = TRUE
ev$Fork=FALSE

#assuming that forks are included in the repo count, we can subtract them
ev$Freq = ev$Freq - evf$Freq
evdf = rbind(ev, evf)


g = ggplot(evdf, aes(x=RepoEvents, y=Freq, group=Fork, color=Fork)) + geom_point() + scale_y_log10() + scale_x_log10()
g + geom_hline(yintercept=c(10,100,1000,10000, 100000)) + geom_vline(xintercept=100)
g + ggtitle('Repo events, contrasting forks and non-forks')
ggsave('figures/repos_events_fork_not_fork_fixed.svg')
g2 = ggplot(evdf, aes(x=RepoEvents, y=Freq, group=Fork, fill=Fork)) + geom_area() + scale_y_log10() + scale_x_log10()
g2

#to retrieve more results
fq = 'SELECT RepoEvents, COUNT(*) AS Freq FROM (
    SELECT repository_url, COUNT(repository_url)  AS RepoEvents
        FROM [githubarchive:github.timeline]
        where repository_fork = "true"
            GROUP each BY repository_url
        ) MyTable
    WHERE RepoEvents > 1000
GROUP each BY RepoEvents ORDER BY Freq DESC limit 10000'

q = 'SELECT RepoEvents, COUNT(*) AS Freq FROM (
    SELECT repository_url, COUNT(repository_url)  AS RepoEvents
        FROM [githubarchive:github.timeline]
        where repository_fork = "false"
            GROUP each BY repository_url
        ) MyTable
    WHERE RepoEvents > 1000
GROUP each BY RepoEvents ORDER BY Freq DESC limit 10000'
1
evf = query_exec(query=fq, project='metacommunities')
ev = query_exec(query=q, project='metacommunities')

head(evf)
head(ev)
fivenum(ev$RepoEvents)
fivenum(evf$RepoEvents)

ev$CumFreq = cumsum(ev$Freq)
evf$CumFreq = cumsum(evf$Freq)
evf$Fork = TRUE
ev$Fork=FALSE

#assuming that forks are included in the repo count, we can subtract them
evdf = rbind(ev, evf)
g2 = ggplot(evdf, aes(x=RepoEvents, y=Freq, group=Fork, fill=Fork)) + geom_point(size=1) +  scale_x_log10()
g2
