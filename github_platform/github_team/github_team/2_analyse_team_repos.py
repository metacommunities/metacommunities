import pandas as pd
import seaborn
import github as gh

# I added the countries in manually, so load this to see team members (including )
team_df = pd.read_csv('data/github_team_with_countries.csv', sep='\t')
team_df.country.value_counts()
print 'There are {} different countries in the team'.format(len(team_df.country.value_counts()))


team_df.followers.plot(kind='bar')
team_df[['name', 'login', 'id', 'created_at', 'followers', 'location']].sort(['created_at', 'followers']).head()
team_df.followers.hist(bins=100)


# to weight the events 
all_team_repos = pd.read_csv('data/github_team_repos.csv', sep='\t')
evts = all_team_repos.groupby('type')['event_count'].sum()
print("The repo events in descending order")
print evts.order(ascending=False)
ct = pd.crosstab(all_team_repos.actor, all_team_repos.repository_url)
