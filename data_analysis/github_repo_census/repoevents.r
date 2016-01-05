library(ggplot2)
ev = read.csv('data/repo_event_counts_top1000.csv')
ggplot(ev, aes(x=RepoEvents, y=Freq))+geom_point() + scale_y_log10() + scale_x_log10()
ev$CumFreq = cumsum(ev$Freq)
evf = read.csv('data/repo_event_counts_top1000_fork_repos.csv')
evf$CumFreq = cumsum(evf$Freq)
evf$Fork = TRUE
ev$Fork=FALSE
evdf = rbind(ev, evf)
g = ggplot(evdf, aes(x=RepoEvents, y=Freq, group=Fork, color=Fork)) + geom_point() + scale_y_log10() + scale_x_log10()
g + geom_hline(yintercept=c(10,100,1000,10000, 100000)) + geom_vline(xintercept=100)
g + ggtitle('Repo events, contrasting forks and non-forks')
ggsave('figures/repos_events_fork_not_fork.svg')
