
# publication/bigdata_ethnography_2016

##TODO

- look at who cites Kelty 2005 and Coleman 2009, etc. 
- add global assemblage into general references for gh -- gh as platform, but one that cannot fully capture the flows that run across it ... 

## Thu Feb  4 12:13:59 GMT 2016
- drafting abstract for book chapter


## Wed Feb 10 15:47:01 GMT 2016
- starting to look at literature on ethnography and code
    This article investigates the social, technical, and legal affiliations among  'geeks' (hackers, lawyers, activists, and IT entrepreneurs) on the Internet. The mode of association specific to this group is that of 'recursive public sphere'' constituted by a shared imaginary of the technical and legal conditions of possibility for their own association. On the basis of fieldwork conducted in the United States, Europe, and India, I argue that geeks imagine their social existence and relations as much through technical practices (hacking, networking, and code writing) as through discursive argument (rights, identities, and relations). In addition, they consider a 'right to tinker' a form of free speech that takes the form of creating, implementing, modifying, or using specific kinds of software (especially Free Software) rather than verbal discourse.

    that's Kelty's abstract
- re-writing abstract to include some of the code literature. Got it down to 11 sentences, and removed much of the imitation argument (keep for large numbers paper). 


## Fri Feb 12 08:34:18 GMT 2016

- re-did abstract for a third time -- came up with a better title -- intersectional assemblages and analytic affiliations, etc. Should be more doable. And I don't need to worry about the big data work too much
- sending abstract off.


## Tue Sep  6 12:43:09 BST 2016

- started writing the chapter, mainly drawing on EASST paper approach -- big number as the site of encounter



## Wed  7 Sep 09:27:42 BST 2016
- not sure how to include in next part of paper -- for instance, the query ...  



## Thu Sep  8 16:52:30 BST 2016

- moved numbers barcelona doc across from other branch so that I can start this main document again. 
- got very distracted in tensorflow configuration work -- typical of  big data stuff


## Fri Sep  9 09:15:28 BST 2016

- is TensorFlow (now working with GPU on Docker image) such a distraction? Seems to me that Docker is probably the real interest at the moment since it seems to change configuration work 


## Tue Sep 13 11:38:36 BST 2016

- been putting many more of the queries into the text -- that's the real focus now -- working with these queries. Could put all the queries into Gists, and just link them all. Or could make the whole paper into a DockerContainer. ...  
- managed to write the rest of the events section, adding new queries to bolster it out. 





## Wed 14 Sep 17:20:04 BST 2016
-struggled quite a lot of with associative imitation graphs -- working on converting those from ipython,etc to ggplot format. But not sure if it is worth the effort. 
- does give some ideas of working with names as I try to do it ... 


## Thu Sep 15 13:19:06 BST 2016

- all morning working on 'streamgraphs' for forks -- this has been a huge effort, but now have functions that plot them for any repo. 
- seems to be some shift in the data at end of 2014 -- everything shifts in the counts. 
- put in the two stacked plots for android and bootstrap. Need to write a bit more commentary on what is going on here. 
- and perhaps think whether counting FOrks is the right thing to do ... 


## Fri Sep 16 10:17:26 BST 2016
 great morning working on chapter -- going back through early parts and fixing them up by adding in literature, some bits of code and a general focusing of the arguments.
- still have not put in the configuration material, but am around 5000 words at the moment.
- also realized something very obvious but important -- I can't count all the repos because I don't know how many are private. But I can see event id numbers - I saw them using the 'events' api. IF event ideas on the public api are consecutive for all events, then I can estimate home many private repos there are, and how private repos have grown by imputing them from events. See fuller discussion of this in ideas log. 
- almost ready to bring in the configuration -- the question for me is how to make it more reflexive ... 



## Mon 19 Sep 14:04:55 BST 2016

- brought in the configuration passage -- bring word coutn to 6100. Wrote and ran some queries, now included in the text to count events and top 0.1% of repositories contributing 25% of event count. 
- and introduced the topic of what we are doing with our own work.  need to write a bit more reflexively here. Should try to do that. 


## Tue Sep 20 16:23:37 BST 2016
- finding it hard to write reflexively about the work with the data; seem to stay firmly in the observational/critical mode. 
- started by trying to just list the number of files.  And then got into using bq ls -j etc to list all the queries and jobs on GoogleBigQuery, so that becomes a way of looking at configuration. 


## Thu Sep 22 12:00:06 BST 2016

- really got stuck in trying to download and analyse bq job data, but now finally working -- needed to use json stream_in, etc
- wrote bash script to get jobs, job ids, and then all the job details, and some R script to plot dates and bytes processed
- did some graphs in the text of the amount of data processed over the years
- added scripts to analysis


## Fri Sep 23 09:31:07 BST 2016

- still working on graphs; have the 22000 jobs on bigquery; have done cumulative data volume graphic -- now need to write commentary on it.   
- sent chapter off with preliminary conclusion; 150 pages long, so has massive amounts of printout ... 
- had another idea: that the attempt to deal with Github meant engaging with a lot of configuration work; and this configuration work is really important to  big data more generally. So all that repository stuff, all the data, is really an encounter with big data, not just Github. That point should go in the conclusion. TODO. 
- 

## Wed 22 Mar 2017 12:52:33 GMT
- have been working on edits on file sent back by df whole_number_in_partsDNedits.docx
- have done about 10 pages of edits so far. There are around 30 pages -- should be done for next Tuesday? 

## Thu 23 Mar 2017 09:17:42 GMT
- got through to end of p19 in edits; roughly 50 edits listed so far;   
- fixed some of the figure references in the article

## Wed 29 Mar 2017 09:31:37 BST
- finished paper edits; there are about 80 including references to go in.  
- reached edit 17
- some comments for eds:
    - found it quite hard to respond to main comment on page 2; problem for me is that I'm not a practising ethnographer, although keenly interested in it. I don't know the contemporary debates well. Could you point me to a couple of things to read for orientation? Could you be something of your own? I did read some George Marcus from JCultEcon, 2014, and added it

## Thu 30 Mar 2017 13:26:22 BST
- have only got 30 minutes today to work on this; hoping to get 10 edits done 
- got to about edit 25/80 

## Mon 24 Apr 2017 09:56:06 BST
- didn't do anything on this in Australia.  
