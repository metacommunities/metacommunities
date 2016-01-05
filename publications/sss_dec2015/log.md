
Fri Dec 18 13:51:56 GMT 2015

wrote abstract

Tue Jan  5 11:40:33 GMT 2016
playing with bigqueries to look at the repo census again. Tried
1. stus basic repo event count -- can use this to cut up repo count
2. started some work on durations using Richard's repo census query which makes a wide table of events, etc. 

Needed to modify queries as they were all using repo names not urls. 
Also saved repo event count top 1000  as csv to data in data_analysis. Can easily plot this to show power law distribution of the event counts. Could also fit distributions using poweRlaw package, but not sure what the point would be ... But the main thing is that the cumulative event counts show very quickly that most repos have few events. 
Could then add to that the number of repos that are forks. 





