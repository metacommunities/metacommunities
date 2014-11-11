library(bigrquery)
library(Rook)
library(tools)
library(brew)
library(rjson)
library(ggplot2)
library(scales)
library(igraph)


#government showcase
sql = "SELECT repository_url, actor, type, count(actor) AS events
FROM [github_explore.timeline]
WHERE (type = 'PushEvent' OR type = 'WatchEvent' OR type = 'ForkEvent') AND (repository_url = 'https://github.com/alphagov/whitehall' OR repository_url = 'https://github.com/WhiteHouse/petitions' OR repository_url = 'https://github.com/opengovplatform/opengovplatform-beta' OR repository_url = 'https://github.com/nasa/mct'
 OR repository_url = 'https://github.com/visionworkbench/visionworkbench' OR repository_url = 'https://github.com/codeforamerica/adopt-a-hydrant' OR repository_url = 'https://github.com/avoinministerio/avoinministerio' OR repository_url = 'https://github.com/nysenate/NYSenateMobileApp' OR repository_url = 'https://github.com/project-open-data/project-open-data.github.io'
  OR repository_url = 'https://github.com/Chicago/osd-bike-routes' OR repository_url = 'https://github.com/opengovfoundation/madison' )
GROUP BY repository_url, actor, type
"

sql = "SELECT repository_url, actor, type, count(actor) AS events
FROM [github_explore.timeline]
WHERE (type = 'PushEvent' OR type = 'WatchEvent' OR type = 'ForkEvent' OR (type = 'PullRequestEvent' AND payload_action = 'opened')) AND (repository_url = 'https://github.com/alphagov/whitehall' OR repository_url = 'https://github.com/WhiteHouse/petitions' OR repository_url = 'https://github.com/opengovplatform/opengovplatform-beta' OR repository_url = 'https://github.com/nasa/mct'
 OR repository_url = 'https://github.com/visionworkbench/visionworkbench' OR repository_url = 'https://github.com/codeforamerica/adopt-a-hydrant' OR repository_url = 'https://github.com/avoinministerio/avoinministerio' OR repository_url = 'https://github.com/nysenate/NYSenateMobileApp' OR repository_url = 'https://github.com/project-open-data/project-open-data.github.io'
  OR repository_url = 'https://github.com/Chicago/osd-bike-routes' OR repository_url = 'https://github.com/opengovfoundation/madison' )
GROUP BY repository_url, actor, type
"

gov_actors = query_exec("metacommunities", "github_explore", sql,
  billing=billing_project) 


#add pullrequests  
  
  
gov_actors$repository_url = substr(gov_actors$repository_url, 19, 100)
  
 
users = unique(gov_actors$actor)
repos = seq(1:length(users))

udf = data.frame(users, repos)
udf$repos = 0

for(u in udf$users)
	{
	udf$repos[udf$users == u] = length(unique(gov_actors$repository_url[gov_actors$actor == u]))
	}

incusers = as.character(udf$users[udf$repos > 1])

gov_actors_sub = gov_actors[gov_actors$actor %in% incusers,]
gov_actors_sub_all = gov_actors_sub

#clean out multiple rows in a hierarchical fashion
for(u in incusers)
{

	#where user has forked repo remove watchevent row
	forkrepos = unique(gov_actors_sub$repository_url[gov_actors_sub$actor == u & gov_actors_sub$type == 'ForkEvent'])
	for(r in forkrepos)
		{
		gov_actors_sub = gov_actors_sub[!(gov_actors_sub$actor == u & gov_actors_sub$type == 'WatchEvent' & gov_actors_sub$repository_url == r),]
		
		
		
		}
}

nodes = unique(c(gov_actors_sub$repository_url, gov_actors_sub$actor ))
nodetype = seq(1:length(nodes))

ndf = data.frame(nodes, nodetype)
ndf$nodetype = "user"
ndf$nodetype[ndf$nodes %in% gov_actors_sub$repository_url] = "repo"

ndf$name = ndf$nodes


g <- graph.data.frame(gov_actors_sub, directed=FALSE, vertices = ndf)
print(g, e=TRUE, v=TRUE)

setwd("C:\\Dropbox\\rmills\\Postdoc\\gephi")

write.graph(g, format="graphml", file = "gov-test.graphml")






#data visualisation

sql = "SELECT repository_url, actor, type, count(actor) AS events
FROM [github_explore.timeline]
WHERE (type = 'PushEvent' OR type = 'WatchEvent' OR type = 'ForkEvent' OR (type = 'PullRequestEvent' AND payload_action = 'opened')) AND (repository_url = 'https://github.com/mbostock/d3' OR repository_url = 'https://github.com/benpickles/peity' OR repository_url = 'https://github.com/gka/chroma.js' OR repository_url = 'https://github.com/okfn/recline'
 OR repository_url = 'https://github.com/jacomyal/sigma.js' OR repository_url = 'https://github.com/samizdatco/arbor' OR repository_url = 'https://github.com/HumbleSoftware/envisionjs' OR repository_url = 'https://github.com/kartograph/kartograph.js' OR repository_url = 'https://github.com/square/cubism'
  OR repository_url = 'https://github.com/michael/dance' OR repository_url = 'https://github.com/trifacta/vega' OR repository_url = 'https://github.com/stamen/modestmaps-js'
OR repository_url = 'https://github.com/Leaflet/Leaflet' OR repository_url = 'https://github.com/matplotlib/matplotlib' OR repository_url = 'https://github.com/Kozea/pygal' OR repository_url = 'https://github.com/dc-js/dc.js' )
GROUP BY repository_url, actor, type
"

datavis_actors = query_exec("metacommunities", "github_explore", sql,
  billing=billing_project) 

datavis_actors$repository_url = substr(datavis_actors$repository_url, 19, 100)
  
 
users = unique(datavis_actors$actor)
repos = seq(1:length(users))

udf = data.frame(users, repos)
udf$repos = 0

for(u in udf$users)
	{
	udf$repos[udf$users == u] = length(unique(datavis_actors$repository_url[datavis_actors$actor == u]))
	}

incusers = as.character(udf$users[udf$repos > 1])

datavis_actors_sub = datavis_actors[datavis_actors$actor %in% incusers,]
datavis_actors_sub_all = datavis_actors_sub

#clean out multiple rows in a hierarchical fashion
for(u in incusers)
{
	pushrepos = unique(datavis_actors_sub$repository_url[datavis_actors_sub$actor == u & datavis_actors_sub$type == 'PushEvent'])
	for(p in pushrepos)
		{
		datavis_actors_sub = datavis_actors_sub[!(datavis_actors_sub$actor == u & datavis_actors_sub$type != 'PushEvent' & datavis_actors_sub$repository_url == p),]
		}
	prrepos = unique(datavis_actors_sub$repository_url[datavis_actors_sub$actor == u & datavis_actors_sub$type == 'PullRequestEvent'])
	for(pr in prrepos)
		{
		datavis_actors_sub = datavis_actors_sub[!(datavis_actors_sub$actor == u & (datavis_actors_sub$type == 'ForkEvent' | datavis_actors_sub$type == 'WatchEvent') & datavis_actors_sub$repository_url == pr),]
		}
	#where user has forked repo remove watchevent row
	forkrepos = unique(datavis_actors_sub$repository_url[datavis_actors_sub$actor == u & datavis_actors_sub$type == 'ForkEvent'])
	for(r in forkrepos)
		{
		datavis_actors_sub = datavis_actors_sub[!(datavis_actors_sub$actor == u & datavis_actors_sub$type == 'WatchEvent' & datavis_actors_sub$repository_url == r),]
		}
}

nodes = unique(c(datavis_actors_sub$repository_url, datavis_actors_sub$actor ))
nodetype = seq(1:length(nodes))

ndf = data.frame(nodes, nodetype)
ndf$nodetype = "user"
ndf$nodetype[ndf$nodes %in% datavis_actors_sub$repository_url] = "repo"

ndf$name = ndf$nodes


g <- graph.data.frame(datavis_actors_sub, directed=FALSE, vertices = ndf)
print(g, e=TRUE, v=TRUE)

setwd("C:\\Dropbox\\rmills\\Postdoc\\gephi")

write.graph(g, format="graphml", file = "datavis-test.graphml")










#github for windows

sql = "SELECT repository_url, actor, type, count(actor) AS events
FROM [github_explore.timeline]
WHERE (type = 'PushEvent' OR type = 'WatchEvent' OR type = 'ForkEvent' OR (type = 'PullRequestEvent' AND payload_action = 'opened')) AND (repository_url = 'https://github.com/BlueSpire/Caliburn.Micro' OR repository_url = 'https://github.com/JamesNK/Newtonsoft.Json' OR repository_url = 'https://github.com/msysgit/msysgit' OR repository_url = 'https://github.com/NLog/NLog'
 OR repository_url = 'https://github.com/dahlbyk/posh-git' OR repository_url = 'https://github.com/Reactive-Extensions/Rx.NET' OR repository_url = 'https://github.com/akavache/Akavache' OR repository_url = 'https://github.com/paulcbetts/splat' OR repository_url = 'https://github.com/octokit/octokit.net'
  OR repository_url = 'https://github.com/reactiveui/ReactiveUI' OR repository_url = 'https://github.com/icsharpcode/SharpDevelop' OR repository_url = 'https://github.com/libgit2/libgit2'
OR repository_url = 'https://github.com/libgit2/libgit2sharp' OR repository_url = 'https://github.com/nsubstitute/NSubstitute')
GROUP BY repository_url, actor, type
"

billing_project <- "237471208995"

gitwindows_actors = query_exec("metacommunities", "github_explore", sql,
  billing=billing_project) 

gitwindows_actors$repository_url = substr(gitwindows_actors$repository_url, 19, 100)
  
 
users = unique(gitwindows_actors$actor)
repos = seq(1:length(users))

udf = data.frame(users, repos)
udf$repos = 0

for(u in udf$users)
	{
	udf$repos[udf$users == u] = length(unique(gitwindows_actors$repository_url[gitwindows_actors$actor == u]))
	}

incusers = as.character(udf$users[udf$repos > 1])

gitwindows_actors_sub = gitwindows_actors[gitwindows_actors$actor %in% incusers,]
gitwindows_actors_sub_all = gitwindows_actors_sub

#clean out multiple rows in a hierarchical fashion
for(u in incusers)
{
	pushrepos = unique(gitwindows_actors_sub$repository_url[gitwindows_actors_sub$actor == u & gitwindows_actors_sub$type == 'PushEvent'])
	for(p in pushrepos)
		{
		gitwindows_actors_sub = gitwindows_actors_sub[!(gitwindows_actors_sub$actor == u & gitwindows_actors_sub$type != 'PushEvent' & gitwindows_actors_sub$repository_url == p),]
		}
	prrepos = unique(gitwindows_actors_sub$repository_url[gitwindows_actors_sub$actor == u & gitwindows_actors_sub$type == 'PullRequestEvent'])
	for(pr in prrepos)
		{
		gitwindows_actors_sub = gitwindows_actors_sub[!(gitwindows_actors_sub$actor == u & (gitwindows_actors_sub$type == 'ForkEvent' | gitwindows_actors_sub$type == 'WatchEvent') & gitwindows_actors_sub$repository_url == pr),]
		}
	#where user has forked repo remove watchevent row
	forkrepos = unique(gitwindows_actors_sub$repository_url[gitwindows_actors_sub$actor == u & gitwindows_actors_sub$type == 'ForkEvent'])
	for(r in forkrepos)
		{
		gitwindows_actors_sub = gitwindows_actors_sub[!(gitwindows_actors_sub$actor == u & gitwindows_actors_sub$type == 'WatchEvent' & gitwindows_actors_sub$repository_url == r),]
		}
}

nodes = unique(c(gitwindows_actors_sub$repository_url, gitwindows_actors_sub$actor ))
nodetype = seq(1:length(nodes))

ndf = data.frame(nodes, nodetype)
ndf$nodetype = "user"
ndf$nodetype[ndf$nodes %in% gitwindows_actors_sub$repository_url] = "repo"

ndf$name = ndf$nodes


g <- graph.data.frame(gitwindows_actors_sub, directed=FALSE, vertices = ndf)
print(g, e=TRUE, v=TRUE)

setwd("C:\\Dropbox\\rmills\\Postdoc\\gephi")

setwd("E:\\Dropbox\\rmills\\Postdoc\\gephi")

write.graph(g, format="graphml", file = "gitwindows-test.graphml")







write.graph(g, format="graphml", file = "att-test.graphml")
	
	
	if(length(unique(gov_actors_sub$repository_url[gov_actors_sub$actor == u & gov_actors_sub$type == 'ForkEvent'])) > 0)
		{
		repos = 
		
		gov_actors_sub = gov_actors_sub[!(gov_actors_sub$actor == u & gov_actors_sub$type == 'WatchEvent'),]
		
		}


 
sql = "SELECT repository_url, actor, count(actor) AS events, max(type) AS type
FROM [github_explore.timeline]
WHERE type = 'WatchEvent' AND (repository_url = 'https://github.com/alphagov/whitehall' OR repository_url = 'https://github.com/WhiteHouse/petitions' OR repository_url = 'https://github.com/opengovplatform/opengovplatform-beta' OR repository_url = 'https://github.com/nasa/mct'
 OR repository_url = 'https://github.com/visionworkbench/visionworkbench' OR repository_url = 'https://github.com/codeforamerica/adopt-a-hydrant' OR repository_url = 'https://github.com/avoinministerio/avoinministerio' OR repository_url = 'https://github.com/nysenate/NYSenateMobileApp' OR repository_url = 'https://github.com/project-open-data/project-open-data.github.io'
  OR repository_url = 'https://github.com/Chicago/osd-bike-routes' OR repository_url = 'https://github.com/opengovfoundation/madison' )
GROUP BY repository_url, actor
"  


actors <- data.frame(name=c("Alice", "Bob", "Cecil", "David",
                            "Esmeralda"),
                     age=c(48,33,45,34,21),
                     gender=c("F","M","F","M","F"))
relations <- data.frame(from=c("Bob", "Cecil", "Cecil", "David",
                               "David", "Esmeralda"),
                        to=c("Alice", "Bob", "Alice", "Alice", "Bob", "Alice"),
                        same.dept=c(FALSE,FALSE,TRUE,FALSE,FALSE,TRUE),
                        friendship=c(4,5,5,2,1,1), advice=c(4,5,5,4,2,3))
g <- graph.data.frame(relations, directed=TRUE, vertices=actors)
print(g, e=TRUE, v=TRUE)


setwd("C:\\Dropbox\\rmills\\Postdoc\\gephi")

write.graph(g, format="graphml", file = "att-test.graphml")







