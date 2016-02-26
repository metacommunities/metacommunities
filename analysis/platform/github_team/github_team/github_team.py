
url = 'https://github.com/about/team'
from bs4 import BeautifulSoup
soup = BeautifulSoup(resp.read(), from_encoding=resp.info().getparam('charset'))
for link in soup.find_all('a', href=True):
        links.append(link['href'])
    
links
len(links)
links[0:10]
links[10:30]
team = links[12:]
team
len(team)
team[:235]
team[:233]
team = team[:233]
team
pre = 'https://github.com/'
[pre+t for t in team]
team_urls = [pre+t for t in team]
pre = 'https://github.com'
team_urls = [pre+t for t in team]
team_urls
import GitHub
import Github
import github
import github as gh
gh.Github?
github = gh.Github('rian39', 'inc14ives')
github.get_user(team_urls[0])
github.get_user(team[0])
team[0]
[t[1:] for t in team]
team = [t[1:] for t in team]
github.get_user(team[0])
user = github.get_user(team[0])
user.company
user.location
cd ~/Documents/google_analytics/publications/dublin_cities_code/
%notebook -e github_team
user.type
user.disk_usage
user.get_repos()
user.plan
user.public_repos
user.total_private_repos
user
user.bio
user.blog
user.name
user.login
user.url
user.raw_data
import pandas as pd
pd.DataFrame(user.raw_data)
pd.DataFrame([user.raw_data])
df = pd.DataFrame([user.raw_data])
df.columns
github.get_user(team[1]).raw_data
team_df = pd.DataFrame([github.get_user(t).raw_data for t in team])
team_df.shape
team_df.location
team_df.location.value_counts()
team_df.location.str.replace(', C[aA]', '')
team_df.location.str.replace(', C[aA]', '').value_counts()
team_df.location.str.replace(', (C[aA]|US)', '').value_counts()
locs = team_df.location.str.replace(', (C[aA]|US)', '').value_counts()
%notebook -e github_team.ipynb
team_df.columns
team_df.created_at
team_df.created_at.sort()
team_df.created_at.order()
team_df['login'][team_df.created_at.order()]
team_df['name'][team_df.created_at.order()]
team_df.name
team_df.to_csv('github_team.csv')
team_df.to_csv?
team_df.to_csv('github_team.csv', encoding='utf-8')
team_df.to_csv('github_team.csv', encoding='utf-8', sep='\t')
mojombo = github.get_user('mojombo')
mojombo.raw_data
team_df.type
team_df.type.value_counts()
team_df.public_repos
team_df.followers.order()
team_df[0]
team_df.ix[0]
team_df.public_repos.order()
team_df.following
team_df.followers
team_df.followers.sum()
%matplotlib
team_df.followers.plot(kind='bar')
team_df.sort(['created_at', 'followers'])
team_df[['created_at', 'followers']].sort(['created_at', 'followers'])
team_df[['name', 'created_at', 'followers']].sort(['created_at', 'followers'])
%notebook -e github_team.ipynb
team_df[['name', 'login', 'created_at', 'followers']].sort(['created_at', 'followers'])
%notebook -e github_team.ipynb
team_df[['name', 'login', 'id', 'created_at', 'followers']].sort(['created_at', 'followers'])
mojombo.id
team_df[['name', 'login', 'id', 'created_at', 'followers']].sort(['created_at', 'followers']).head()
team_df[['name', 'login', 'id', 'created_at', 'followers', 'location']].sort(['created_at', 'followers']).head()
team_df.followers.mean()
team_df.followers.sd()
team_df.followers.std()
team_df.followers.hist()
team_df.followers.hist()
team_df.followers.hist(bins=100)
import seaborn
team_df.followers.hist(bins=100)
team_df.followers.hist(bins=100)
%notebook -e github_team.ipynb
mojombo.raw_data()
mojombo.raw_data
mj_repos = mojombo.get_repos()
mj_repos.totalCount
mj_repos.totalCount()
p1 = mj_repos.get_page()
p1 = mj_repos.get_page(1)
p1
p1[0]
r1 = p1[0]
r1.raw_data
r1 = p1[1]
r1.raw_data
r2 = p1[2]
r2.raw_data
r2 = p1[3]
r2.raw_data
team_df.location
pd.read_csv('github_team.csv', sep='\t')
team_df = pd.read_csv('github_team.csv', sep='\t')
team_df.name
team_df.login
team_df.country.value_counts()
len(team_df.country.value_counts())
'|'.join(team_df.login.values())
'|'.join(team_df.login.values)
all_names = '|'.join(team_df.login.values)
all_names = '|'.join(team_df.login.values) + '|mojombo'
all_names
team_df.sort('name')
team_df['name'].sort('name')
query = """SELECT actor, repository_url, type, count(type) as event_count FROM [githubarchive:github.timeline] 
where  actor = 'defunkt'
group each by actor, repository_url, type
order by event_count desc
LIMIT 1000"""
query
query = """SELECT actor, repository_url, type, count(type) as event_count FROM [githubarchive:github.timeline] 
where  actor = 'defunkt'
group each by actor, repository_url, type
order by event_count desc
LIMIT 1000""





@@@
"""
query = "SELECT actor, repository_url, type, count(type) as event_count FROM [githubarchive:github.timeline] where  actor = 'defunkt' group each by actor, repository_url, type order by event_count desc LIMIT 1000"
query
pd.io.gbq.DataFrame?
pd.io.gbq.read_gbq?
repo_df = pd.io.gbq.read_gbq(query)
repo_df.shape
repo_df.head()
%notebook -e github_team.ipynb
all_team_repos = pd.DataFrame()
for t in team_df.login:
    print t
    
for t in team_df.login:
   

    
    
    asfasdf
    
query
query = "SELECT actor, repository_url, type, count(type) as event_count FROM [githubarchive:github.timeline] where  actor = '{}' group each by actor, repository_url, type order by event_count desc LIMIT 1000"
query.format('hello')
for t in team_df.login:
    team_query = query.format(t)
    df = pd.io.gbq.read_gbq(query)
    all_team_repos = all_team_repos.append(df)
    
all_team_repos.shape
df
for t in team_df.login:
    team_query = query.format(t)
    df = pd.io.gbq.read_gbq(query)
    all_team_repos = all_team_repos.append(df)
    
query
%paste
%paste
%paste
%paste
%paste
all_team_repos.shape
all_team_repos.head()
%paste
all_team_repos.shape
all_team_repos.to_csv('github_team_repos.csv', sep='\t')
all_team_repos.repository_url.value_counts()
all_team_repos.columns
%notebook - github_team.ipynb
%notebook -e github_team.ipynb
pd.crosstab?
ct = pd.crosstab(all_team_repos.actor, all_team_repos.repository_url)
ct.shape
all_team_repos.repository_url.unique()
all_team_repos.repository_url.unique().shape
ct.head()
ct.dot(ct.transpose())
all_team_repos.columns
all_team_repos.head()
all_team_repos.groupby('type')['event_count'].sum()
all_team_repos.groupby('type')['event_count'].sum().sort()
all_team_repos.groupby('type')['event_count'].sum()
evts = all_team_repos.groupby('type')['event_count'].sum()
type(evts)
evts.sort()
evts.order()
evts.order(ascending=False)
evts.order()
evts.order(ascending=False)
%notebook?

