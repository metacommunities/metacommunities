# what is stored in the redis db
contribution = evttype in ["IssuesEvent", "PullRequestEvent",
                                           "PushEvent"]

osrc:total -- count all events - set

osrc:day - hashset for days of week, number 1 - 7
osrc:hour - hashset for hours of the day, number 1 - 24

osrc:user rian39  - sorted set by user name and number of events
osrc:event  zrevrange  -- number of events, broken down by kind
osrc:event:IssueEvent:day weekday eventcount -- HGETALL osrc:event:IssuesEvent:day
osrc:event:IssueEvent:hour hour  eventcount -- HGETALL osrc:event:IssuesEvent:hour

osrc:user:NAME:day 1 eventcount      - hashset of event totals for that user by day of week
osrc:user:NAME:hour 23 eventcount      - hashset
                
osrc:user:NAME:event IssuesEvent 2 -- sorted set of eventcounty for that kind of event
osrc:user:NAME:event:PullRequestEvent:day 2 23  - hashset for days
osrc:user:NAME:event:PullRequestEvent:hour 2 23  - hashset for hours

osrc:repo OWNER/REPO nevents -- the ranking of all repos by event counts -- zrevrange osrc:repo 0 50 gives top 50

osrc:social:user:NAME repo event_count -- a sorted set of repo names and their event counts
	e.g.  Zrevrange osrc:social:user:torvalds 0 100

osrc:social:repo:OWNER/REPO NAME -- sorted set of repos with their contributors counts - zcard osrc:social:repo:torvalds/linux

## languages
osrc.lang  - sorted set of languages by number of events
osrc.pushes.lang LANG -- sorted set of languages by push  e.g. ZREVRANGE osrc:pushes:lang 0 10
osrc:user:NAME:lang LANG - sorted set of languages by events e.g ZREVRANGE osrc:user:rian39:lang 0 20
osrc:lang:LANG:user NAME nevents -- sorted set of languages by user importance e.g. zrevrange osrc:lang:Python:user  0 10
                       
                       