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
