library(RMySQL)

drv = dbDriver("MySQL")
con = dbConnect(drv,host="localhost",dbname="git",user=USER,pass=PASSWORD)

orgs = dbGetQuery(con, "SELECT * FROM organizations_megatable3;")

orgs$WatchEvents[is.na(orgs$WatchEvents)] = 0
orgs$ForkEvents[is.na(orgs$ForkEvents)] = 0
orgs$IssuesEvents[is.na(orgs$IssuesEvents)] = 0
orgs$IssueCommentEvents[is.na(orgs$IssueCommentEvents)] = 0
orgs$DownloadEvents[is.na(orgs$DownloadEvents)] = 0
orgs$PullRequestsClosed[is.na(orgs$PullRequestsClosed)] = 0
orgs$repos_linked_to[is.na(orgs$repos_linked_to)] = 0
orgs$posts_linking_to_orgs_repos[is.na(orgs$posts_linking_to_orgs_repos)] = 0
orgs$answers_linking_to_orgs_repos[is.na(orgs$answers_linking_to_orgs_repos)] = 0

"""
1. totally internal, almost fictional organisation that individuals make 
for some benighted reason (e.g ours -- we have a research project)
2. internal but substantial organisations that make something that goes 
out into the world -- e.g. a software project/product
3. external organisation who move into github as a way of 
revamping/expanding etc what they do.
4. Junk
5. Short-term
"""
#temporary org type? things like cs371p-spring-2013, they have several for different times


#type1 - Very few social events (<10 of any one type excluding issue(comment)events), no mentions on stackoverflow, less than 10 pushers
#type2 - more than 10 pushers OR has social events (>= 10 Watches/Forks/PullRequests, I'm excluding issue events) OR has been mentioned on Stackoverflow
#type3 - tricky, maybe very high ratio of pushes to pushers and a relative lack of social events? Haven't worked out a way to find these yet.
#type4 - junk, active for less than a month, single pusher, no social events or mentions on stackoverflow
#type5 - short-term (<= 5 days) - only includes repos not classified as junk


orgs$type = 0

#also do binary variables

orgs$type1 = 0
orgs$type2 = 0
orgs$type3 = 0
orgs$type4 = 0
orgs$type5 = 0

#type 1 - practically, these are the orgs which don't fall into any of the other types, so set all to 1 first
orgs$type = 1


#type 2 - if its defined by a high level of activity, how many of those orgs have been referenced on SO?
orgs$type[orgs$Pushers >= 10 | orgs$WatchEvents >= 10 | orgs$ForkEvents >= 10 | orgs$DownloadEvents >= 10 | orgs$PullRequestsClosed >= 10 | orgs$repos_linked_to >=1] = 2
orgs$type2[orgs$Pushers >= 10 | orgs$WatchEvents >= 10 | orgs$ForkEvents >= 10 |  orgs$DownloadEvents >= 10 | orgs$PullRequestsClosed >= 10 | orgs$repos_linked_to >=1] = 1


#type 3 = has pushes and pushduration, very few social events and pushers


orgs$type[orgs$PushEvents > 10000 & orgs$Pushers <= 3 & orgs$PushDurationDays >= 100 & orgs$WatchEvents <= 10 & orgs$PullRequestsClosed ==0 & orgs$repos_linked_to == 0] = 3
orgs$type3[orgs$PushEvents > 10000 & orgs$Pushers <= 3 & orgs$PushDurationDays >= 100 & orgs$WatchEvents <= 10 & orgs$PullRequestsClosed ==0 & orgs$repos_linked_to == 0] = 1


#type5 - short term (where they also meet criteria for type 4 this takes precedence)
orgs$type[orgs$PushDurationDays <= 5] = 5
orgs$type5[orgs$PushDurationDays <= 5] = 1


#type4
orgs$type[orgs$Pushers == 1 & orgs$PushDurationDays <= 30 & orgs$repos_linked_to == 0 & orgs$WatchEvents == 0 & orgs$ForkEvents == 0] = 4
orgs$type4[orgs$Pushers == 1 & orgs$PushDurationDays <= 30 & orgs$repos_linked_to == 0 & orgs$WatchEvents == 0 & orgs$ForkEvents == 0] = 1



