# Large numbers and many events: methods for imitative fluxes and the data-as-raw-material imaginary

Fri Nov 27 09:00:20 GMT 2015

## Overview

- the case study – a social media platform that hosts ~20 million code repositories; 
- diagrammatic cultures and data:  the political economies of counting and graphing
- code and field of devices: 'co-device analysis'
- obstacles to and potentials for count-based ethnographic sensibility


## case study in 2 senses:

- a study of coding as a practice, and the way that code links into government, media, science, business and civil society
- a study of working with data amidst the shifting methodological conditions of big data, and the like.

## the case study – a social media platform that hosts ~20 million code repositories; 

During 2013-2014, I was funded by the ESRC and also sponsored by Google Corporation. Along with 4-5 other funded projects, my project called 'metacommunities of code' sought to analyse how code was shared being shared across millions of software repositories.

### Some context here for code sharing:

1. We are used to hearing about the importance of code and programming. Here in the UK, the government mandated last year that all children will learn to code because coding is a vital economic activity. Such legislative moves suggest that software development is not one work practice amongst others, but a locus of power, agency, labour or value; 
2. Coding practices have changed over the last decade or so in fairly profound ways, which I won't detail here. The principal changes are a broad cultural shift in the organization of software development away from massively centralized software development (the kind epitomised by Microsoft or IBM) to a much more de-centralized process in which lines between production, distribution, and use have thoroughly blurred. Code flows in much more diverse ways. At the same time, it has become a much more *public* activity, and the *publicness of code* has become a major concern for business, government and science, for different reasons.

The social media site Github, started in in 2007, epitomises these changes:
1. it has grown tremendously in the last 7 years (like many social media platforms) to include around 29 million software projects. When I started the project, that number was around 13 million, but even in the last year it has grown tremendously. 
2. this growth flows from a tremendous variety of processes that are difficult to summarise or classify partly because the topics or domains of coding are so diverse and partly because much of what flows through Github is quite social but also technical. Whether we summarise or classify them or not matters less than the sheer fact of their existence.  

Like many contemporary assemblages, Github seeks to describe itself through large numbers.  In June 2014, Github showed a photo of a women working in an urban office location, with lights and professional camera focused on her work. It described '6.1 million people collaborating right now across 13.2 million repositories ... building amazing things together'. In November 2015, Github has a slightly more functional description, and the image seems to be a press conference in China:

>GitHub is how people build software. With a community of more than 11 million people, developers can discover, use, and contribute to over 29 million projects using a powerful collaborative development workflow. [Github/About](https://github.com/about)

 The numbers change over time, but that change itself, alongside the sometimes rather sublime scales of community (a community of 11 million people?) forms part of the description. Most importantly, large numbers feed back into  and strengthen the platforms that host them.[^3]

 [^3]: Neither image -- the woman at work in a funk urban office or the press conference in China -- is arbitrary. Github was rocked in 2012 by allegations of sexism and mismanagement, particularly associated with one of the co-founders, who subsequently resigned and left Github. In early 2015, Github itself was subject to a massive Denial oF Service attack, emanating from China. Reports alleged that the DoS attack targeted pro-democracy repositories on Github. Unlike many social media platforms, China does not block Chinese citizens' use of Github because it is seen as economically and commercially important for the software industry. 

## Diagrammatic cultures and data:  the data-as-raw-material imaginary

The power of large numbers brings us to the nexus of the ESRC and Google. Both of these bodies have a certain investment in data and digital technologies, and in what I'm calling the data-as-raw-material imaginary. While Google's interest in that will be well-known, the ESRC's might be less familiar. Here's the call for applications:

>The ESRC and Google are pleased to announce the Google Data Analytics Social Science Research Call. Data is the new raw material of the 21st century. It allows citizens to hold governments to account, drives improvements in public services by informing choice, and provides a feedstock for innovation and growth. As open-source data and data integration grows, it is a key time to better understand how it maps onto and possibly significantly strengthens, the ability of academics to understand society. 

>The ESRC spends between £15-20 million per year on the collection and curation of data, providing access to a wide variety of data resources and developing the methodological tools and techniques for building and exploiting data resources. This has helped to create a world-leading data infrastructure. Much of this funding has been focused on the creation and support of large scale surveys and other aggregate statistics provided by other major agencies like the ONS. However, as the volume of less structured online data resources become increasingly available the ESRC has recognised the potential of capturing and connecting huge data flows in new ways to support conceptual, methodological and empirical advances in social and economic research. 

> As a first step we are collaborating with Google to identify demand from the social science community in working with online data and to develop a suite of demonstrator projects which highlight its true value for better understanding society.


Much in this call for proposals will be familiar: 'data is the new raw material of the 21st century' points to newness, nowness, and economic potential of work. The following sentences invoke citizens, choice, public services, innovation, growth, and, last but not least, 'academics' understanding society. It then contrasts existing investments in data collection and curation, particularly surveys and statistical data, but contrasts this data with the 'new data,' the 'huge data flows.' Finally, 'as a first step,' the Google collaboration aims to identify 'demand,' as if social science researchers working with data are a kind of consumer, but a consumer who produces 'understanding.' 

## Working with large numbers

To all of this, we might simply respond with a degree of critical scepticism. Isn't this just all part of the economisation of data, another twist in what James Beniger called the 'control revolution' in which information and programs function as ways addressing problems of distribution, consumption, or communication?

STS approaches suggest a slightly messier but perhaps more challenging way of thinking about and responding to this situation.  From the work of Helen Verran, for instance, we can see that this work on 'raw materials' is bound to involve political differences, and that these differences will affect any understandings that depend on that data:

>In any practical going-on with numbers, what matters is that they can be made  to work, and making them work is  a politics. Yet is a politics that completely evades conventional foundationist analysis (Verran, 2001: 88)

Or as John Law would put it, if methods enact the social, what kind of social do data analytics and the like enact? [see @Law_2004] The data-as-raw-material imaginary nearly always includes large numbers. As we have already seen with Github, numbers such as 29 million or 11 million come up straight away. Given that the project was funded by the ESRC, how could we go on with large numbers? What kind of going-on with numbers would I,  as an STS researcher, engage in?  Is it possible to work with numbers in ways that 'make them work' politically?

## The Github data

The project was awarded to work on Github using data that the platform makes available through its Application Programmer Interfaces or APIs. In nearly all social media or web2.0 settings, this data embodies the traces of social practices of many different kinds criss-crossing digital devices today. The API data was not created as a data resource for social scientists, but for software developers working in convergence cultures [@Jenkins_2004] in which connecting different platforms, devices, sites and practices together using code has become standard practice. 

The data is generated as developers write code and store that code in repositories. Coding has a complex collaborative structure that I won't attempt to describe here. The collaboration or 'sharing' to use social media keywords includes both people and things. The format of the data that records this activity is anything but 'raw.' By convention, for instance, nearly all API data from social media sites has an 'event' structure, and Github is no exception to  this. SHOW SLIDE of event.

```
{
"id": "2111998059",
"type": "WatchEvent",
"actor": {
"id": 1459103,
"login": "mmemetea",
"gravatar_id": "4532d1e4885f579ca7d9aa8748418817",
"url": "https://api.github.com/users/mmemetea",
"avatar_url": "https://avatars.githubusercontent.com/u/1459103?"
},
"repo": {
"id": 14802742,
"name": "OpenSensorsIO/azondi",
"url": "https://api.github.com/repos/OpenSensorsIO/azondi"
},
"payload": {
"action": "started"
},
"public": true,
"created_at": "2014-05-23T08:40:56Z",
"org": {
"id": 5497318,
"login": "OpenSensorsIO",
"gravatar_id": "1e0218942846ec8ef59f5d679dbca782",
"url": "https://api.github.com/orgs/OpenSensorsIO",
"avatar_url": "https://avatars.githubusercontent.com/u/5497318?"
}
}
```

This is about as raw as Github data gets. This is a relatively simple 'social event', a `WatchEvent` on Github, recording the act of an `actor` calling themselves `mmemetea` interested in the repository called `azondi`, a software project coordinated by the 'organisation' calling itself `OpenSensorsIO`. This event has also has a datetime recording when the event occurred. Note that the event also has various status designations -- it is a `public` event, it has a 'payload' (often much more complicated than simply `started`) -- and includes various indexical references or `id`s that link the event to people, organisations, repositories and images (`gravatar_id`). The tricky syntax of all this data -- many brackets, inverted commas, colons, commas -- attests to an ontology which aligns all actors, actions, places and times in discrete events, and whose *nested* structure contains all variations within a formal hierarchy displayed via indentation.

## What can be done with event data?

Now that we have a grasp of the basic data format of a social media platform, what work can be done with it? What can be done with hundreds of millions of them? For that's how many we have: around 300 million public events can be retrieved from  Github.  

I should say that the actors in my research project included two social statisticians, two StS-aware media theorists, and myself, someone who stands somewhere between STS and media and cultural studies, with a strong interest in methods. As the PI, I had a vision of working with the data in ways that resonated with recent StS work on traceability, on device-specific methods in the growth of digital sociology, and with media and cultural studies work on platforms, algorithms and participation.

By traceability, I refer to recent ANT work, such as [@Latour_2012] - 'The Whole is Smaller than the Part: How Digital Navigation May Modify Social Theory.' Latour and Venturini argue that given tools that allow us to move between different scales and locations in social fields, we no longer need the long-standing structural oppositions between structure and agency, between macro and micro. We instead begin to inhabit a space of continuously transforming scales in which any particular standpoint stabilises scale for a particular actor. 

By 'device-specific research,' I mean principally the work of Noortje Marres and the Amsterdam 'Digital Methods Initiative.' Marres and Weltevrede  argue that when we make use of 'digital navigation,' we need also to countenance the fact that any knowledge we generate mixes in complicated ways features derived from the platform itself and from practices originating elsewhere [@Marres_2012a; @Marres_2015].  Marries highlights the ways in which the data is formatted by the social life of the devices and platforms that give rise to it; yet we need to look for the forms of practice, difference, change or becoming that cannot be fully formatted by the event-structures of the platform. That is, we need to look in and around the data for what **overflows the platform and its formatting of events**.

I found the media and cultural studies work on platforms, algorithms and data less directly useful at the level of methods, but important in terms of overall framings. For instance, one concern in much of that work has been to understand how immaterial or cognitive labour takes place in contemporary media environments [@Gill_2008] configured as cognitive capitalism. At the same time, from the StS standpoint, I was quite interested in giving a strong empirical account of immaterial labour epitomised by coding work. The basic idea here would be that the massively decentralized flows of code through Github co-constitute people and things in a 'field of devices.' While 'geeks shall inherit earth,' and coding work lacks the salient precarity of much immaterial labour (carework, art, call-centre operatives), the tremendous re-socialization of coding work over the last decade suggests something important happens to work, to property, and to community here. My own digital sociology could well operate in this vein.  

To summarise these perspectives, and their implications for the practical going on with Github data:
1. Traceability through event data should free up any pre-given opposition between macro and micro, structure and individual
2. Device-specific research should address the interplay between the purposive formatting of data and something that overflows or eludes that formatting
3. Immaterial labour and cognitive capital suggests a need to track transformations in work and value creation processes, to see how they are organised, controlled, asymmetrical or hierarchical despite their de-centralization.  

## Going on with the data: GithubArchive

When I wrote the proposal for the project, I did not know that an enormous wave of interest was gathering around the  Github data. Maybe in 2012 I should have anticipated that interest. More likey my interest was just one symptom of a broader investment in this data. Remember, ESRC call aimed in collaboration with Google to gauge demand amongst academics for online tools able to work with large, 'raw material' data, such as that generated at platform APIs. After the project was awarded, the RAs and I started to write code to gather and collate data from the  Github APIs. This was a relatively tedious process. While  Github delivers almost everything that happens on the platform through the  API, the history of these events has to be programmatically reconstructed and stored. APIs typically 'throttle' or rate-limit requests for data. This is in the interests of 'liveness.' Most operational uses of API data only need what happened recently not the several hundred million events that stretch back to early 2008. 

Why then in mid-2013, after the project has started, after much effort has been spent in gathering huge numbers of events, generating long list of code repository names, and reading some of the burgeoning research done by academic software engineers on Github do we suddenly become aware of GithubArchive? A 'Web Performance Engineer' at Google called Ilya Grigorik has launched both a Github repository and a website GithubArchive.org dedicated to amalgamating all this data in one place. 

Moreover, Grigorik, working at Google, had access to Google's infrastructure, and was able to not only publish all the data in an archive, but to transform that data, whose formatting we have discussed above, into the flat tabular forms familiar in much statistical work, and make it available through Google's newly launched cloud computing service, GoogleBigQuery.[^1] The Github was even listed, along with all the words in Shakespeare and all the US birth name records as one of three public datasets that people could use to learn about GoogleBigQuery. Like GithubArchive, the GoogleBigQuery datasets were updated hourly, and they went back to 2011. 

In some ways, this seemed too good to be true. All the data had been collected in one place, and access to that place was unrestricted. In addition, the data had been copied to an extremely powerful online analytics tool, a 'Big Data' system, that perfectly epitomised the tools that the ESRC wants social researchers to use in their 'capturing and connecting of the huge data flows.'

[^1]: GoogleBigQuery, it seems, is the commercialisation of an internal infrastructure called `Dremel`, that Google has since 2006 used in many different ways to manage its own platforms. 
    • Analysis of crawled web documents.
    • Tracking install data for applications on Android Market.
    • Crash reporting for Google products.
    • OCR results from Google Books.
    • Spam analysis.
    • Debugging of map tiles on Google Maps.
    • Tablet migrations in managed Bigtable instances.
    • Results of tests run on Google’s distributed build system.
    • Disk I/O statistics for hundreds of thousands of disks.
    • Resource monitoring for jobs run in Google’s data centers.
    • Symbols and dependencies in Google’s codebase. [@Melnik_2010]


The project budget had allocated funds for two laptops and some hard drives to store data. GoogleBigQuery, however, is a 'Platform as a Service' in which charges are made depending on how much data (measured in gigabtye and terabytes) a particular computation consumes. It was rather alarming to receive a bill for over \$USD2000 in early August 2013, only a few months into the project. One of the RAs had written a rogue  query that continued running all night, consuming almost 2 terabytes of data. Somewhere in a data centre, steam billowed out of the compute engines, as  our equipment budget dwindled to nothing in one query.  In later negotiations with Google, a credit of \$1500 didn't actually refund the charge on my credit card, but did give us computing resource. Our 'device-specific research' became device-specific in a specific way: we were more or less locked into the Google cloud services. 

## Diagrammatic imaginaries in data

This archiving, copying and transformation, on the other hand, also drew the attention many other people, including Github itself. A succession of 'Github Data Challenges' ensued in the next three years (2012-2014) The fact Github itself organises 'data challenges' (https://github.com/blog/1544-data-challenge-ii-results) suggests that  people doing things with this data is part and parcel of the public life and publicity of the platform or device. These data challenges are what AnneLise Riles calls 'momentary apprehensions of depth' showed that drawing networks has long been part of networks (Riles, 2001: 184). Whatever the reason for these data challenges (they are increasingly common in many places today in the form of hackathons, data competitions, etc), they bring to light practical imaginings of what is in data. 

In response to these challenges and availability of the public Github datastream, people do things like:

1. the OpenSource Report Card  (http://osrc.dfm.io/) by Dan Foreman-Mackay, is a prize-winning use of the timeline data. It ingests all the data from the Githubarchive, counting what developers do, when they do it, and using what programming languages. With this data stored, it then builds a predictive model that allows it to both characterise a given Github user, and to predict who that Github user might have affinities with. The admonition from Foreman-Mackay  – 'Dear recruiters: While you read this, make sure that you remember that GitHub is not your C.V. and that these stats only provide a biased and one-sided view. This is just a toy. Don't take it too seriously! ' – suggests that this is a playful application of the data, but one that is nevertheless quite typical of what is being done with data streams in social media, mobile communications, retail advertising and marketing, etc. OpenSource Report Card treats the data as a way of seeing similiarities and differences in individual software developers in terms of counting events by type and comparing how often and when an individual does something on Github. Here the massive datastream is brought to bear on finding similiarities between people. 
2. People often map datastreams by geographic location. An extraordinary proliferation of maps has occurred as a result. The  mapping of Github contributions by location performed by David Fischer (http://davidfischer.github.io/gdc2/#languages/C) is typical in that it too counts events, but this time puts the emphasis on places of work.
3. As is common today in sentiment analysis on social, people look for feelings in data. In 2012, software developers feelings were mined in terms of emotional words present in comments found in the Github events (http://geeksta.net/geeklog/exploring-expressions-emotions-github-commit-messages/), and the presence of words in these message can be cross-linked with programming languages in order to identify what programming language elicit most emotion. The emphasis here is on how software developers  feel in relation to particular kinds of work. 
4. Finally, people make live dashboards for Github. Octoboard (http://octoboard.com/) is a typical dashboard. Dashboards are becoming very common as a way to engage with the liveness of data. Data analysis is no longer something done in leisurely rhythms of analysis, but is increasingly framed as a realtime in the form of 'stream analytics.' That is, not also does the data stream, but the analysis is meant to stream as well in order to be timely, lively and responsive to change. Octoboard presents a summary of daily activity in major categories on Github – how many new repositories, how many issues, how repositories have been 'open sourced' today. Also it offers realtime analytics on emotions.
5. The familiar relation form of the network appears in many guises. In both academic work [@Cronin_2014] and data competitions, networks have often appeared as ways of tracing relations between people, between projects or sometimes between programming languages. These diagrams closely resemble what we see in [@Latour_2012]. 
6. For academic researchers in computer science and certain parts of management, Github has been a boon because they study software development in the wild much more easily.  Academic researchers in fields such as software engineering do social network analysis in order to gauge productivity, reuse, efficiency and other engineering and management concern [@Thung_2013]. 
7. Finally, and looking slightly more widely,  the Github data stream has quickly become a favourite training tool for data mining books. In his book *Mining the Social Web: Data Mining Facebook, Twitter, LinkedIn, Google+, GitHub, and More,* Matthew Russell makes use of the Github timeline to demonstrate ways of uses social network analysis to highlight the important nodes and links between repositories and users [@Russell_2013]. Again, the propensity to apply network analysis approaches is widespread and endemic to the data itself, given the way that the event format is already implicitly framed by a network or 'social media' understanding.

So, the actors in concert with the archives of the datastreams are already doing so much in the data streams. They identify individual behaviours and their similiarities, they analysis geographies, emotions, social networks, and they offer live summaries and so on. They often invent ways of working with the data using particular devices and platforms. The way in which the OpenSource Report Card models counts what developers do on Github and constructs a simple but vast encompassing database and model for millions of Github developers is quite fascinating. The visual forms of some of the projects are interesting too for the way in which they sometimes provide very simple summaries – bar chart, a some text, a network visualization – of highly entwined processes. 

It seems like 'the social' has been rapidly and heavily colonised here. The Data Challenges and the GoogleBigQuery encourage exploration of almost any conceivable question, pattern or practice through the data. As goings-on with number, they produce maps, tabulations, dashboards, graphs, networks and summaries are various scales ranging from affect to global geography, from individual developer's productivity to patterns of similarity between programming sub-cultures. 

## Overflow in the data

What would the methodological orientations of traceability, or of device-specific research do here? The speed of the work done on GithubArchive during the Data Challenges completely overtook the slow development that we had been planning. Secondly, many of the obvious empirical questions were quickly addressed, and analyzed. And, as is often the case with contemporary data analytics, the data here is quite social, so those analyses are already in our space, the space of the social. 

Or is it in the social in the same way? The long-standing Lancaster take on the social is that methods enact the social [see @Law_2004]. All of this going on with the numbers is very tangled, because as it shows the sociality of Github data -- the patterns of social networking, the ebb and flow of sentiment around particular practices, the geography of code work, etc. -- it also enacts the framing of the social that Google and ESRC advance. This version of the social replaces the demographic counting of populations and, as well, the mid-20th century version of the social associated with media, marketing and government, the public defined by opinions and attitudes elicited through polls [see @Osborne_1999], with a hybrid entity formed at the intersection of practices, their traces (event data) and some transformations in inscription devices that in this case take the form of GoogleBigQuery.

Tensions between different ways of doing the social began to play out in the project during 2013, even before we were fully aware of all the work being done on the GithubArchive data by data scientists and the like. My vision of device-specific researcher or digital sociologist began to encounter the ways of going on with numbers in contemporary applied statistics. With good justification, statisticians like to say 'no' to many of my desires to enact the social through the data.  

For instance, a basic question for me was: amidst 13 million code repositories, how many actually contain code? Around this time, many new organisations were setting up Github repos for all kinds of purposes -- to draft laws, to develop public policy, to post recipes. Was it possible to count how many repos actually contain code? And given they contain code, could then count those that contained something substantial? Or even a more seemingly basic question such as can we tell whether an actor is human or not? Or a perhaps a slightly more complicated question -- how many of the organisations on Github have any existence apart from their repos? -- would be answerable. I hoped also to address questions such as: of the repositories that contain code, how many work on different topics? Despite extensive work by the RAs and myself on these questions, using a variety of data exploration techniques, we didn't manage to answer any of these questions. We used a mixture of methods, including latent class analysis and  machine learning techniques. The flat abundance of the Github event data constantly reasserted itself. 

\begin{figure}
  \centering
      \includegraphics[width=0.9\textwidth]{figure/info1.pdf}
        \caption{Figure title}
  \label{fig:events_in_time}
\end{figure}

\begin{figure}
  \centering
      \includegraphics[width=0.9\textwidth]{figure/organisation_parent_community.pdf}
        \caption{Figure title}
  \label{fig:organisations_on_gh}
\end{figure}

We found ourselves at odds concerning what should be with the data. The contrast can be seen in the figures. Figure \ref{fig:events_in_time} on the left patiently examines patterns events across repositories over time, graphing how they are distributed in different ways. The main message here, as can be seen from the subplot 'Github Repo Events' is that very little happens in the vast majority of code repositories. (This is the infamous 'power-law' or 'long-tail' distribution of social media activity.) This figure, while soundly based in the GithubArchive event data, tells us very little about the heterogeneity and diversity of activity around coding. On the right hand side represents the work of the digital sociologist. The vast network graph of organisations and their relations on Github does evoke something of the crowdlike intensity of software cultures, but at the cost of losing legibility as well. The nodes in this graph represent 'organisations' and their repositories.  Their colour comes from a 'community detection' algorithm developed by physicists to explore social network structures in the same way they explore molecular forces [@REF_TBA].  

Which of these two diagrams is better? The first remains close to the discipline of statistics in its cautious attempt to diagram patterns of practice. Like that discipline, however, it remains somewhat detached from the values and differences that matter in particular domains. The second more or less *imitates* what is happening in the field of data-intensive re-enactments of the social, inadvertently reusing many of the same inscriptive devices, ranging from GoogleBigQuery to the network graphs shown in the figure. This inadvertent imitation might count as an example of how immaterial labour of the analytic/symbolic kind is often done amidst conditions of precarity: the imitation of data intensive enactments of the social by academics such as myself (but there are far worse cases to be found) attests to both shifts in the relations of production around cognitive surplus value and the precarity associated with these forms of constantly changing work. For instance, GoogleBigQuery almost immediately obliterated our first six months of data collation and gathering.  

## Taking the imitation seriously

Given a dilemma in which I constantly felt myself constrained by a justified and sceptical statistical reserve about what could be with the data (no matter we have a hundreds of Gb of it) and at same interpellated by the very same practices that had no doubt prompted the ESRC-Google funding programme, it was hard to find a space to play.[^2]

Despite working very hard on this problem of finding a different way of going on with numbers, I didn't find any simple solution. Almost by chance, our small research team become  itself de-centralized during this time. While we were using  Github to coordinate our own work, the de-centralized repositories attracted very different levels of commitment. Some members of the team, in which I include myself, saw using  Github itself for our project as part of an ethnographic participation we wanted to bring to these going on with numbers. But for others,  Github workflow was constrictive. They could be more productive alone, delivering mini-work packages  by other means (emailed documents, etc.).  

If I did find any relief from the problem of doing statistically weak and behind the cutting-edge data science in this project, that relief came mainly in the form of taking imitation seriously and seeing imitation as both productive, and possibly politically efficacious. After I left Lancaster in 2014 to spend a term of research leave in Copenhagen, one potential in the hundreds of millions of events in  GithubArchive seemed to remain: that even if we could not know about that general distribution of repo topics, or whether they contained code or not, or whether they mattered as repos or not, one thing in the event data was not fully formatted and homogenised in its formatting: the names of the repositories themselves, in all their trivial, superficial, often imitative yet quite countable entity. 

## Analysing imitation

\begin{figure}
  \centering
      \includegraphics[width=0.9\textwidth]{figure/powertime-wide.pdf}
        \caption{The power of events over time}
  \label{fig:power_time}
\end{figure}

The analysis of the event timeline continually suggested a great proportion of events in the data were trivial, and in particular, imitative. Millions of repositories were simply copies of other repositories. Millions of repositories flash into visibility on the timeline for a brief period before falling back into obscurity. The diagram shown in the Figure \ref{fig:power_time} encapsulates this imitative flux quite well. It comprises three graphs that count how many events are associated with repositories. On the left hand side, millions of repositories receive less than five events during the 18 months. On the right hand side, less than 50 repos receive more than a thousand events. 

But rather than see this empherality as a waste, noise or something to be discarded, maybe in terms of immaterial labour and the politics of large numbers, it matters quite a lot. Given that repositories are receptacles for the work of software developers and coders, and that they are the material expression of all the immaterial labour associated with code, it seems strange that the vast bulk of them are so ephemeral. When we start tracking the patterns of imitation, rather than looking for the events that define repositories as important, something different starts to appear.

Looking at the flow of names of repositories, and how they move in waves of imitation begins to show something of the dynamics that animate the growth of large numbers.  These take two forms in the event data. Firstly, almost one half of the repositories in Github are simply copies of other repositories. This is part of the 'sharing' practice of Github coding. People 'fork' other repositories frequently. 

\begin{figure}
  \centering
      \includegraphics[width=0.9\textwidth]{figure/bootstrap_repository_forks_plain_counts.pdf}
        \caption{Figure title}
  \label{fig:bootstrap_forks}
\end{figure}

\begin{figure}
  \centering
      \includegraphics[width=0.9\textwidth]{figure/android_stackplot_2014-07-03-22-40.pdf}
        \caption{Android forks}
  \label{fig:android_forks}
\end{figure}


The figures shown above show some versions of this counting of imitation. In both Figure \ref{fig:bootstrap_forks} and \ref{fig:android_forks}, the imitations appears in two different ways. The broad bands of color rippling across the figures graph the counts of copies being made each day on Github of important repos. But the much more dense striations seen in Figurew \ref{fig:android_forks} count copies of repositories whose names incorporate the important repository, but vary it in some way. These striations still imitate, and they generate large numbers of events, but less homogenously, and in greater variety. In this striations, new things sometimes appear. 

I see these figures as presenting a different way of working with large numbers. They sense the average everydayness of working with code as a form of work. In this work, important repositories act like brands, as points around which forms of identity take hold and multiply. A sensibility for imitation, therefore, in STS might benefit from media and cultural studies.  With certain exceptions like Donna Haraway, STS doesn't always play happily with the critical approaches developed in media and cultural studies. But media and cultural studies approaches to brands, commodities, imitation, identity and differences might help us here. Imitation saturates popular culture, and media and cultural studies has long grappled with what to make of imitation. 


## Conclusions

I have been describing the work needed to get contemporary digital data and associated large numbers to do something other feed back into the platform and its associated data-as-raw-material imaginary. I have been suggesting that STS research might develop its strong ethnographic sensibilities in relation to data event streams by sitting in an ambivalent space between formats and disfiguring elements, between the device-specific and its overflows. There are several different ways to understand what is at stake in this work.

One comes from Latour, Jensen, and Venturini, who ask:

>Is it possible to do justice to … common experience by shifting from prediction and simulation to description and data mining? … Let the agents produce a dynamics and collect the traces that their actions leave as they unfold so as to produce a rich data set’ (Latour et al., 2012)

I broadly agree with them but think there are hidden difficulties in their recommendation. What they call the 'rich data set' is pre-formatted for particular actors and agents (the platform usually). If we are interested in alternative agencies, we have to work against the traces in some ways. Helen Verran's observation about work on numbers might be a more productive starting point. As she says, 'in any practical going-on with numbers, what matters is that they can be made to work, and making them work is a politics' (Verran, 2001). Like Verran, I see the interplay between different kinds of numbering as generative. 

How do we re-animate and open up the large numbers that abound in contemporary sciences and technologies? To do this, we need to find ways of working on formatted data that goes against its pre-formatted counting relations and uses. The massive availability of data from online databases is power-laden number work. Its very openness allows a certain kind of capitalising and governing based on data to expand. The formatting of data streams tends to simply confirm and expand how the platform already advertises itself. By contrast, device-specific research that attends to the ways in which data is formatted, and how that formatting affects practices around the platform seems to me quite important in alternative to the much advertised (but actually often limited) opennness of data.

If our concern is to begin to explore the indeterminacy in the relations between what is specific to the devices or platforms and what is specific to the social practices that come to those platforms. I think ethnographic work on things like the flow of naming heads in a different direction to the formatting of data for purposes of platform services and enterprises. It cannot remain content with the familiar processes of reduction to social networks, or counting specific kinds of pre-formatted event types. In the case of Github, the names of repositories offer one way to begin to explore this ambiguity and indeterminacy.o

I have also been suggesting that STS work on numbers might help us understand better the transformations in work that concepts such as immaterial labour and cognitive capitalism often describe in quite abstract ways. If coding epitomises contemporary immaterial labour, the patterning of events on Github might indicate the imitative fluxes that organise that work, rendering it routine, ordering it and controlling it. 

[^2]: At a workshop with Google employers in their London offices in early 2015, all the funded projects described their experience. The other projects had used twitter data to identify changing brand loyalties,  classified mp3 tracks according to their musical genre, and build infrastructures to allow social researchers to collect lots of social network meidia and then analyse it using network analysis approaches. Given the audience of Google managers and ESRC officers in a crowded boardroom, with video links to other parts of Google Corporation around the world, there was little scope to articulate the complications that I describe here. I had the sense that, apart from our intensive use of GoogleBigQuery (and we were the only project to use Google's on data analytics and cloud computing services), these issues were simply over the horizon for that audience. 

## References
