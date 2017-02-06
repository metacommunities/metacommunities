# data analysis ideas    

## Tue Feb 16 16:50:43 UTC 2016

- could see Github  as UGC on speed -- hardly any consumption there, just making. Where would that sit with the other range of activities?
- is there any way just to check for things like timestamps, or particular operations of calculation (Callon style) or particular styles of platform usage (Cloud, virtualisation)?
- wrote query for GoogleBigQuery to test this:
    SELECT repository_name, type, created_at, payload_commit, payload_commit_msg FROM [githubarchive:github.timeline] 
    where payload_commit_msg != "null" and regexp_match(payload_commit_msg, 'virtualiz') limit 10

## Wed Feb 17 10:01:29 UTC 2016
    - added this to sql list
    - could also extend it to include repo name and org name
    - would need to craft search queries for different topics  -- 'docker or chef or etc.'

## Mon Feb 22 14:48:22 UTC 2016
- how would you analyse who is leaving Github? http://agateau.com/2016/github-lock-in/

## Tue Mar  8 22:05:30 GMT 2016

- having Stirling piece on  'general framework for analyzing diversity' -- could redo the metacommunity argument using that ... 

## Wed Mar  9 11:27:01 GMT 2016

### Github diversity -- how would we think of diversity in code-sharing commons? Is this a mono-culture? 
 - played a bit with MastodonC NESTA github thing -- and started a new branch on repo-languages  to see if it could implement the 'diversity' idea. What would software diversity be? Languages? organisational-associative structures? variety- the number of categories; balance- the pattern of apportionment of elements across categories; disparity - manner and degree to which elements may be distinguished; how different from each other are they? 
 - no way to aggregate, accommodate or articulate full variety, balance and disparity, all of which can be quantified ... 


## Wed Mar  9 13:17:20 GMT 2016
 - reading zach holman on deployment -- https://zachholman.com/posts/deploying-software -- useful in describing some of the experiments, containers, etc of contemporary infrastrustructures -- versions, branches, etc

## Fri Mar 11 09:35:28 GMT 2016
- going through old fork-pullrequest queries -- could use these to engage with the problems of centralisation on Github
- also looking at null language repositories on gh -- 10M repos have no language -- that is a major fraction -- what is going on in them. That would be worth looking into. Might make a new mini-analysis branch on that.  
- ok, did do that -- but put stuff in analysis/repo_language branch
- also thinking about posting on gh as too centralized -- that's what I've thought for a while. But how to analyse it? What is the centring effect? Are there places that the centring breaks down and in what ways? This connects to wider debates about platforms and hubs on the internet. Is Github a good case study of this?

## Wed Mar 16 18:52:50 GMT 2016

- people leaving Github  -- there is a posting about that on some blog -- how could I look at that?
- the API -- are there any controversies about the API? Could use Bucher to talk about that a bit. 

## Thu Mar 24 14:32:05 GMT 2016

- just submitted sss manuscript and looking at how to 'release' it. But found this 'integrations' page https://github.com/integrations. Could perhaps use that to track how some code moves through infrastructures. Many different forms of integrations shown there, but so what? Can anything of this be gleaned from event data?

## Tue Mar 29 17:19:33 BST 2016

- playing around a lot with torch and nn and names. Have run ltstm  models on 1M github names. Not sure how to use the deeplearning stuff. Could either - 
    - find ways of exploring what the nodes of the network are seeing. Given the low validation error, the LTSTM model is pretty capable of developing a generative model of repo names. 
    - develop a training set and use the classifiers, as documents in the torch tutorials to extract all the names from github repositories. 

## Thu Mar 31 10:31:02 BST 2016

- The Sense of Dissonance: Accounts of Worth in Economic Life, David Stark, has really interesting stuff about work and organizations. If we did a paper on github as a kind of work, as immaterial labour, etc, this would be a good reference


## Mon Jun 13 21:38:50 BST 2016

- returning to nn stuff and names. Looking at allamanis' work (see zotero libraries) on source code -- mainly on summarization of source code -- could perhaps adapt that to Github names but in combination with some other features, like programming language, etc. 

## Tue Jul 26 09:52:42 BST 2016

- did proofs for infrastructures handbook and looked quite a bit at heroku-travis-ci and various other entities -- could try to do something more with those in relation to infrastructure and its contemporary transformation; especially in the light of 'stack'; 
- also found some new literature on data mining Github -- added some to zotero and archive  -- reasonable attempts to understand popularity of projects on Github, albeit with little sense of software culture; Weber's focus  on Python is quite good; the brazilian piece has useful stuff on 'node'; also has a guide to some other recent literature. 
- such a study would include docker, travis, jenkins, chef, puppet, vm, PaaS, IaaS, SaaS, etc. What would it try to explain?  
- would be good to contrast all of these with node and javascript, and all that happens around that. 

## Mon Aug 22 12:25:45 BST 2016

 - been doing slides for barcelona, and see that _configuration_ is actually a good way to talk about a whole slew of things to do with  Github.  
 - looked at a few notes on config -- ranging Suchman, Woolgar, Arendt to Badiou -- quite a few views on configuration -- all suggesting what a strange entity configuration is. 
- would be worth doing a proper search on 'configuration' in STS, theory, and perhaps computer science?

## Thu 25 Aug 11:14:51 BST 2016

- did the search on `configuration` -- there is not much there. The research on configuration is curiously marginal, even though the term is used quite often (as in 'spatial configuration'). Would be good to look at the STS literature -- Akrich, Suchman, Woolgar -- again with contemporary configurations in mind.  

## Fri Sep  2 11:16:57 CEST 2016

- hand-eye configuration: use Steve Jackson's idea of the hand to work on config and dotfiles; then use the keystrokes to highlight the digitality of abstraction  
- would be worth doing a proper search on 'configuration' in STS, theory, and perhaps computer science? DONE -- see below

## Sat Sep  3 12:38:03 CEST 2016

- need to extend the notion of configuration in order to range across scales, and in order to oppose scale. This is Sarah Kember's phrase -- 'oppose scale' -- and maybe a focus on configuration ranging from hand to data centre, from text editor to container, would help do that. It would be good to see how Docker, the most active repository in Github deals with configuration. 
- problem: how to write a bq that shows for any given month the 10 most active repositories. It would be an event count broken down by month? It would include clones? Or perhaps only as a point of comparison. 
    select repository_name, count(type) as events, extract_month_year(date) as month_year from GithubArchive Group
    by repository_name order by month_year, events desc limit 10


## Mon Sep  5 14:19:09 BST 2016

- really got back into bigqueries over weekend. Added a couple to sql file. Also starting some code to analyse them -- just a few lines of dplyr really ... 
- wrote script to filter top results per month; easy to change event type in the query. Could then compare different events -- fork, pullrequest, issue, member, watch, public, release, etc.
- added script to analysis/social_practices/
- would it be possible to classify repos by topic and category? and could that be predicted?

## Fri Sep  9 09:45:11 BST 2016

- pfaffing a lot with docker containers -- trying again to see if that gives a significant handle on 'configuration.' Could imagine looking at CI, containerisation, vms, cloud platforms
- could use a list of their names to track down configuration-related developments 
- here's the query:

       > SELECT repo.url, count(*) cnt, year(created_at) yr, month(created_at) wk
        FROM 
            [githubarchive:year.2011],
            [githubarchive:year.2012],
            [githubarchive:year.2013],
            [githubarchive:year.2014],
            [githubarchive:year.2015]
        where repo.url contains('docker')
        group by repo.url,yr,wk
        having cnt>100
        order by yr, wk, cnt desc 
        limit 200

- would also be able to engage with Bratton's idea of **'stack'** -- look at Docker, Travis, OpenStack, Jenkins, kubernetes, etc.


## Thu Sep 15 15:08:53 BST 2016

- stack idea keeps coming back at the moment -- could use Leigh Star account of layers to intervene in this. Show how layers are done today in the 'stack,' the main layered entity of contemporary infrastructures. She has really good analysis of how 'layers' work in vlsi chip design.  


## Fri Sep 16 10:21:16 BST 2016

- just had really good idea that might totally change how I count -- the _series_ of event ids in the api are consecutive. That means I can measure the gaps in those ids to impute the presence of private repos, and perhaps also get a sense of how the capital number, the surplus value form, of Github takes shape. 
- tried to write a lag query on bquery, but didn't work ... 
- played a bit with repo.ids -- they may have the same property -- they seem to be consecutive but with gaps in the numbers. Excellent opportunity to use Whitehead on this. 
- also had the Gödelian idea of constructing an event number that uniquely expresses each repoid, actorid, eventid, and UTCdate and then putting them in order. But would be the point of that? To create a super-searchable list of everything that happens? To look for patterns in those numbers? Not sure. Probably better to just focus on getting a good set of event.ids, and the seeing what can be done with those. Even just the basic proportion of events that are private would a useful find.  
- that aside:found typical problem -- event ids are only in GoogleBigQuery for some years (2011, 2012, 2015, some of 2014). Are they in GithubArchive? Need to check that  - perhaps by grepping in gz tarballs. ... 


## Tue Sep 20 22:45:56 BST 2016
- starting to play with jobs from GoogleBigQuery as a way of looking at how much data have been through and what that means in terms of configuration, and its materialization


## Sat Sep 24 11:40:54 BST 2016
- writing queries to look at pattern of event ids in GithubArchive. Seems like they were switched on in 1 Jan 2015 again. A billion events are shown for that year. So the public events show 212,174,067. But event ids are close to a billion. (Run the query to see this differences: 9.98E+008. That suggests that almost 80% of the events are private. Could that be right? And given that they might be less 'social', what then?
- started to repeat the same analysis using repo.ids. Quite interesting results and maybe more reliable --  
-wrote query to get 1st 100 repos by id and look at the their activity over the last 5 years -- most or all are infrastructural elements of Github itself. 
-wrote query to download 1st million repo.ids and then some R script in repo_census to look at how many ids are missing, and if there is any pattern in that. See **analysis/repo_census/repo_ids.r**
- wrote queries and some graphs to look at rates of repo creation over all years. Seems to be really uneven at times. Maybe spam or DDos stuff?
- plotted 10% sample of all ids again date -- seems like a smooth curve and interesting in terms of why there is a gap in the data in 2012. Downloaded some extra data to try to cover that gap. 
- used gsutil to download table from Google storage -- best to keep it compressed. Wanted to see if data had the same 2012 gap in it.  
- realized why the curve has so much stuff below -- the Fork and Create events I'm using to count with have the base repo.id in the repo.id field, not the new repo.id
- TODO: redo the repo.id queries to count the ids of the  forked repos by looking in the payload field and for the CreateEvent looking in the payload field for the ref_type = repository.
- But maybe I don't really need to do this. As long as a I have list of unique repo.ids and the first date in which they are mentioned, not for what event, then should be ok. Because a branch can only be created after a repository has been created. Will still need to check for Forkers tho, since many people just fork and do nothing else.   

## Mon Oct 10 15:35:27 BST 2016

- played quite a bit on weekend with gz archive on hpo to look at flows of events around important repos -- e.g. tensorflow with its 50k watchers. Also theano is big
 - had the idea of following the outflow of just repository across a whole range of places to see how a set of concerns are taken up .. 

## Mon Nov  7 12:24:20 GMT 2016

- started work on jcultecon, but also seen some new literature on commons -- the undercommons, etc. Also skeggs article ~/archive/Skeggs-2014-The_British_Journal_of_Sociology.pdf has some useful references on commons and value. Also stuff in UNSW thesis to look at. 

## Thu Nov 17 21:34:26 GMT 2016
- also on open, TODO: check onlineopen.org -- has Pasquinelli, etc.  

## Mon Nov 21 17:14:52 GMT 2016
- reading MEOT, had ideas about where the coder sits in relation to ensembles. It seems that they are not inventors, operators or any of those position. What is individuate through them? How do they become part of the associated milieu of the ensemble? Would be good to clarify some of these different positions by reference to different projects on  Github. This mean a different understanding of 'social coding.'   

## Wed 14 Dec 14:13:12 GMT 2016
- actually some of the MEOT ideas have gone into the number paper, but could develop them more fully.
- also been looking at git internals -- for instance from https://www.git-scm.com/book/en/v2/Git-Internals-Git-References -- this is really useful to understand how things are put together. Amazingly pervasive use of hash functions, and trees. They structure everything it seems. Could develop some digital materiality argument around the hash function perhaps. A low-level account of git would be very geeky ... 

## Mon 19 Dec 2016 11:28:46 GMT
- news accounts of  Github losing millions see [@Newcomer_2016] -- the de-centralised workforce is costing too much! Billboards going up in SF. Also the rise of the competitors -- gitlab, bitbucket -- more focused on corporate;   
- also GoogleComputer has announced all the stackoverflow data is now on GoogleBigQuery

## Mon 16 Jan 2017 12:11:18 GMT
- idea: would it be possible to look for all  Github sites that are using CI services? How would you do that? Is there an event for that? Something like WebHooks 
- looking at Github api, but it seems that DeployEvents do not appear in timeline data. So won't appear in any bigquery data. That means that may be many events that do not appear in the data.  
- so would probably need to use deployment statuses on a set of repos: e.g. https://developer.github.com/v3/repos/deployments/#list-deployment-statuses
- also started looking at travis-ci api, and what it offers (not much), and then got distracted into setting up ci for my own projects, which is not the point at the moment. So shutting down now!

## Fri 20 Jan 2017 15:42:53 GMT
- there is a posting about  Github growth and whether it is scale free, and why  http://perfdynamics.blogspot.co.uk/2017/01/github-growth-appears-scale-free.html Could be useful to work with. TODO: look at how it's done 


## Thu 02 Feb 2017 10:19:59 GMT
- read Straube on Git; 2016; bdas; also maybe go through bdas more generally for purposes of git 


## Mon 06 Feb 2017 15:24:04 GMT
- really interesting development:  Github has introduced machine-learned topics: https://github.com/blog/2309-introducing-topics; see also https://help.github.com/articles/about-topics/ 
