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


