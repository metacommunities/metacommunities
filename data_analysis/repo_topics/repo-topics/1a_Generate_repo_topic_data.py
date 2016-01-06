# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import redis
import pandas as pd
import re

# <codecell>

repo_table = 'metacommunities:github_proper.repo_list'
red = redis.Redis(db='1')

# this loads around 10 million repo names, so its a bit slow
%timeit -r 1 repo_list = pd.read_pickle('data/repo_list.pyd')

# <codecell>

# only run this if the repo_list has been updated
pipe = red.pipeline()
step = 100000
for i in range(0, len(repo_list), step):
    pipe.sadd('repos:list', *repo_list[i:i+step])
    pipe.execute()

# <codecell>

def construct_repo_df_using_local(query):
    """ For a given query, return all the repo full names from the local
    copy of all the repo names.
    It uses regular expression   on a list to do this.
    
    @param: regular expression query
    """
    if repo_list is not None:
        full_df = pd.DataFrame(repo_list[repo_list.str.contains(query)], columns = ['full_name'])
        print(full_df.shape)
        return full_df
    else:
        return None

# <codecell>


def repo_query(query):
    """ Runs simple GLOB-style queries against the list of all repo fullnames
    in the Redis database"""
    
    query_formatted  = '*{}*'.format(query)
    more_results = True
    results = []
    c=0
    while more_results:
        c, res =  red.sscan('repos:list', cursor=c, match = query_formatted, count = 10000000)
        results.extend(res)
        if c is '0':
            more_results=False
    print ('Found {0} repositories for query {1}'.format(len(results), query))
    return results

# <codecell>

def construct_repo_df(query, description = False, local =True):
    """ For a given query, return all the repo names, full names and fork
    from the master list of reponames held on the githubarchive timeline.
    It uses regular expression to do this and queries the table: metacommunities:github_proper.repo_list.
    
    @param: description - if True, will use the 'description' field too
    @param: local - if True, will use the local copy of the repo names"""
    
    query = query.lower()
    #to deal with the way people name repositories, try various separator characters
    query = re.subn('[-_\s+]', '.?', query)[0]
    query = re.subn('[,\(\):]', '', query)[0]
    print query
    
    if local:
        return construct_repo_df_using_local(query)
    else:
        print('starting bigquery ... ')
    
        if description:
            full_query = 'SELECT name, full_name, fork FROM [github_proper.repo_list] where regexp_match(lower(name),"' + query +'") or regexp_match(description,"'+ query +'")'

        else:
            full_query = 'SELECT name, full_name, fork FROM [github_proper.repo_list] where regexp_match(lower(name),"' + query +'")'

        full_df = pd.io.gbq.read_gbq(full_query)
        print(full_df.shape)
        return full_df

# <codecell>

query = 'facebook'
%timeit repo_query(query)

# <codecell>

query = 'facebook|twitter'
%timeit construct_repo_df_using_local(query)

# <markdowncell>

# # Topics of github repos 
# 
# How far in classifying all the repositories can we get by using repo names? And also departing from the github showcases?
# I'm taking a fairly rough but encompassing approach by using lists of sofware from various sources.  I've cleaned the lists quite a bit in making them. 
# 
# ## List of topics/domains
# 
# There are three main sources of topics I'm drawing on here. 
# 
# 1. List of software, often found on wikipedia or specialist sites
# 2. A big list (several thousand) of file formats categorised by domain
# 3. A list of disciplines and fields
# 
# Combining these helps identify components of github repository names. 
# I've also got an idea that these components constitute an intensive time-space metacommunity. 

# <markdowncell>

# ## Possible domains:
# 
# 
# 
# 1. databases: -- use a list of them: see http://db-engines.com/en/ranking -- DONE
# 2. web frameworks: -- use a list of them -- apache, ruby on rails, asp.net, symphony, etc: see http://hotframeworks.com/ DONE
# 3. editing tools and code development tools: -- using a list of them -- wikipedia has one http://en.wikipedia.org/wiki/List_of_text_editors; and for ides: http://en.wikipedia.org/wiki/Comparison_of_integrated_development_environments
# 4. github and git components: -- need to use search on reponame for these; -- DONE
# 5. test repos for testing github use: -- query reponames for 'test|try|demo|hello' -- DONE
# 6. dot or config files for bash, zsh, tmux, csh, vim, emacs: , etc -- list for these including 'bash|zsh|tmux|csh|vim|emacs|dot?file' -- DONE
# 7. javascript libraries for web pages: - jquery, bootstrap  - http://en.wikipedia.org/wiki/List_of_JavaScript_libraries DONE
# 8. data visualization: d3.js, ggplot2, matplotlib, 'dashboard|infoviz|chart|plot'
# 9. machine learning: in title or in description -- the phrase, plus 'advanced analytics'; perhaps algorithms by name - vowpal, support vector machine, neural net, etc - http://en.wikipedia.org/wiki/List_of_machine_learning_algorithms and added a list of software from  http://en.wikipedia.org/wiki/Machine_learning -- DONE
# 10. icons and fonts and emojis: -- just search for these literals in the name -- DONE
# 11. css tools and libraries: -- css like bootstrap -- http://en.wikipedia.org/wiki/CSS_frameworks -- DONE
# 12. package and library management: -- rubygems, apt, cran, cpan, homebrew, etc - http://en.wikipedia.org/wiki/List_of_software_package_management_systems -- DONE
# 13. server administration, virtualization and infrastructural services: -- chef, including operating systems and cloud platforms like azure, etcsee http://newrelic.com/devops/toolset -- DONE
# 14. drawing and graphic design: -- gimp, inkscape, svg, png, illustrator, sketch, draw, cad, raytrace -- CHECK FILE FORMATS on this
# 15. video, sound and image processing: --  'video, youtube, image,  jpeg, mp3, mpeg, audio, sound, photograph' -- DONE
# 16. code cleaning: -- linters
# 17. policies: -- legal, political, data, 
# 18. books: -- mainly technical, but probably others too; tons of these, but many are code-based. Used manual query.  -- DONE
# 19. games: -- use 'game' in the reponames -- again, many just with this simple query, but also 'xbox, ps3, wii', '['game', 'xbox', 'playstation', 'wii', 'kinect', 'nintendo', 'minecraft', 'warcraft']. -- DONE
# 20. programming languages: -- development of the languages, but also as programming platforms against on which things are made
# 21. computational architectures and operating systems: -- linux, openwrt  -- DONE?
# 22. science and modelling: -- of what? molecules, populations, dynamic systems, etc -- huge list of disciplines http://en.wikipedia.org/wiki/List_of_academic_disciplines_and_sub-disciplines that I've downloaded and cleaned a bit.  -- DONE
# 23. hardware devices: -- arduino, raspberry pi, android, ios, blackberry - they bring many libraries to them; --'arduino|raspberry|android|ios|blackberry|armv|symbian'  DONE
# 24. data manipulation, statistics and calculation: -- pandas, numpy, but also spreadsheets -- hard to define this list -- I started with this http://en.wikipedia.org/wiki/List_of_statistical_packages  and then appended this http://en.wikipedia.org/wiki/List_of_numerical_analysis_software -- DONE
# 25. build and build management tools: -- compilers, but also continuous systems like Jenkins -- http://en.wikipedia.org/wiki/List_of_compilers; http://en.wikipedia.org/wiki/Continuous_integration#Software -- DONE
# 26. maps and gis: -- libraries, tools and maps -- search for gps, geo, gis - http://en.wikipedia.org/wiki/List_of_geographic_information_systems_software - DONE
# 27. business software: -- accounting, finance, personal or business including spreadsheets (xls) 
# 28. data processing architectures: -- Hadoop
# 30. Social media platforms: -- how could I forget -- http://en.wikipedia.org/wiki/List_of_social_networking_websites -- DONE
# 31. internet protocols and services: - ftp, smtp, etc, etc -- used http://en.wikipedia.org/wiki/Lists_of_network_protocols  DONE -- might need to add more to the list of 18 -- DONE
# 32. document processing: -- wordprocessing, desktop publishing, presentations, docx, markdown, latex, etc; then just 'document|presentation|' -- DONE
# 32. Github as a blog or webpage: -- search for 'github.com|github.io' -- DONE
# 33. cracks and downloads: -- 'crack|download' -- DONE
# 34. filehandling tools: -- archives, compression, etc -- use fileformats? -- no, put them into packages -- DONE
# 35. educational platforms: -- list form wikipedia@ -  DONE
# 36. apis and sdks: -- this a really wide ranging query -- DONE

# <markdowncell>

# Each of these domains -- and there are probably more to be added -- is populated by a range of different pieces of software, implemented in different languages, and with different relations to each other. Even assembling a fully list of the main pieces of software would be a significant achievement, and useful in making sense of why Github looks like it does. There would also be many overlaps between them. 
# 
# The aim would be to process all of the 12 million repo names in the list and try to classify them using a mixture of rules. Given the name of a repo, what it groups does it belong to. The mapping that results would be like a treemap, with some blurry edges. 

# <markdowncell>

# #  File formats
# 
# This is a huge list. They provide pointers to different domains and connect between them (e.g. xml, json vs svg, etc). See http://en.wikipedia.org/wiki/List_of_file_formats; could be interesting to use this as a lens overall; or as a way to augment any of the list givens above all.  

# <markdowncell>

# # Repo domains

# <codecell>

file_formats = pd.read_csv('topic_lists/file_formats.csv', sep='\t', header=None, names = ['domain', 'filetype', 'description'])
file_formats = file_formats.apply(lambda x: x.str.strip().str.lower())
file_formats['domain'].value_counts()

# <codecell>

file_formats.ix[file_formats['domain'] == 'graphics']

# <markdowncell>

# This list of file types suggests some things I haven't looked at properly. 

# <markdowncell>

# ## Spam and download repositories
# 
# Many events on the github timeline might be produced by botnets or spammers. There are many repositories that appear and disappear from the timeline. Yet they add to the overall repository count. 

# <codecell>

spam_query = 'crack|download|free.*mp3'
spam_df = construct_repo_df(spam_query, description = False)

# <codecell>

long_title_query = 'SELECT name, full_name, fork FROM [github_proper.repo_list] where length(name) > 40'
long_title_df = pd.io.gbq.read_gbq(long_title_query)
print(long_title_df.shape)

# <codecell>

# keep all the Bayesian probability programming books
long_title_df = long_title_df.ix[-long_title_df.name.str.contains('Bayesian')]
long_title_df.shape

# <codecell>

spam_df = pd.concat([spam_df, long_title_df])
spam_df = spam_df.drop_duplicates()
print spam_df.shape
red.sadd('spam', *spam_df.full_name)

# <markdowncell>

# ## Test/try/demo repos
# 
# Many people just play a bit with git or github

# <codecell>

test_query = 'test|try|demo|hello|getting started|starting|beginning|train|learn|sample|spoon-knife'
test_df = construct_repo_df(test_query, description=False,local=True)

# <codecell>

test_df.head()

# <codecell>

red.sadd('tests', *test_df.full_name)

# <markdowncell>

# As expected, this is quite a big number of repos -- 0.8M. 

# <markdowncell>

# ## Code editors and IDEs
# 
# These have to be a basic part of the Github world, since nearly everything we find there has been written in some kind of text editor. There are around 120 editors and 133 IDes in the Wikipedia list.
# 
# Matching problems occur around some editor names -- 'ee', and 'ed' for instance are text editors on Unix and BSD platforms. It's hard to get good matches on those. 

# <codecell>

editors = pd.read_csv('topic_lists/editors.csv', header = None, names = ['name'])

ides = pd.read_csv('topic_lists/ide_list.csv', header=None, names = ['name']).drop_duplicates()

# <codecell>

print(ides.head())
editors.sort(inplace=True, columns =['name'])
editors.drop_duplicates(inplace=True, cols = ['name'])

print(editors['name'].head())

# <codecell>

ed_query_1 = 'editor|' + '|'.join(editors['name'][:50].str.strip()).lower().replace('++', '\\\+\\\+')

ed_query_2 = '|'.join(editors['name'][50:].str.strip()).lower().replace('++', '\\\+\\\+')

ide_query = '|'.join(ides['name'].str.strip()).lower().replace('++', '\\\+\\\+')

# <codecell>

ide_df = construct_repo_df(ide_query, description=False,local=True)

# <codecell>

red.sadd('ides', *ide_df.full_name)

# <codecell>

ide_df.head()

# <codecell>

editor_df = construct_repo_df(ed_query_1,local=True, description=False)

# <codecell>

editor_df2 = construct_repo_df(ed_query_2, local=True)

# <markdowncell>

# This is still way too noisy, but I'll work with it for the moment. 

# <codecell>

editor_df.head()

# <codecell>

editor_df = editor_df.append(editor_df2)
editor_df.drop_duplicates(inplace=True)
editor_df.shape

# <codecell>

delete = False

# <codecell>

pipe = red.pipeline()

if delete:
    pipe.delete('editors')

for i in range(0, editor_df.shape[0], 100000):
    pipe.sadd('editors', *editor_df.full_name[i: i+100000])
res =pipe.execute()

# <markdowncell>

# ## Compilers
# 
# There are huge number of these.

# <codecell>

compilers = pd.read_csv('topic_lists/compilers.csv', header=None, names = ['name'])
compilers.dropna(inplace=True)
compilers.drop_duplicates(inplace=True)
compiler_query = '|'.join(compilers.name.str.strip()).lower().replace('++', '\\\+\\\+')

# <codecell>

compiler_df = construct_repo_df(compiler_query, description=False)

# <codecell>

red.sadd('compilers', *compiler_df.full_name)

# <markdowncell>

# This is pretty huge. 0.5M Possible the biggest category I've seen. Is this really noise? 

# <markdowncell>

# ## Continuous integration build

# <codecell>

integration_list = pd.read_csv('topic_lists/integration.csv', header =None, names = ['name'])
integration_query = '|'.join(integration_list.name.str.strip()).lower()

# <codecell>

integration_df = construct_repo_df(integration_query, description = True)

# <codecell>

red.sadd('integration', *integration_df.full_name)

# <codecell>

integration_df.head()

# <markdowncell>

# ## Programming languages

# <codecell>

programming_query = '\\bC\\b|java|php|javascript|perl|ruby|python|scala|pig'
programming_df = construct_repo_df(programming_query, description=True)

# <codecell>

programming_query2 = 'clojure|fortran|lisp|actionscript|objective-c|\\bSQL\\b|lua|visual basic'
programming_df2 = construct_repo_df(programming_query2, description=True)

# <codecell>

programming_df = pd.concat([programming_df, programming_df2])

# <codecell>

red.sadd('programming_language', *programming_df.full_name)

# <markdowncell>

# ## Package manager software
# 
# There are around 100 different package managers in use. 

# <codecell>

packagelist = pd.read_csv('topic_lists/package_manager.csv', header=None, names = ['name'])
packagelist.shape
package_query = 'zip|tar|gz|'+ '|'.join(packagelist['name'].str.strip()).lower()

# <codecell>

package_df = construct_repo_df(package_query)

# <codecell>

package_df.head()
red.sadd('packages', *package_df.full_name)

# <markdowncell>

# Another quite important category -- 0.2M repos here. 

# <markdowncell>

# ## Databases
# 
# Several hundred databases are in use. The point of looking for them in repo names or descriptions is to highlight work on the databases themselves. 

# <codecell>

# list of databases came from db-engine.com. I just copied the ranking table there. There are around 200 there.
dblist = pd.read_csv('topic_lists/db_list.csv', header=None)
dblist.columns = ['name', 'type']
print(dblist.shape)

# <codecell>

dblist['type'].value_counts()

# <markdowncell>

# The idea with such lists is to construct queries that look for all the top db names in names of repos, and then see how that divides up

# <codecell>

dbquery = '|'.join(dblist['name']).lower()

# <codecell>

db_df = construct_repo_df(dbquery, description=False)

# <codecell>

print(db_df.shape)
print db_df.head()
red.sadd('databases', *db_df.full_name)

# <markdowncell>

# This is not a huge number -- around 0.125 M, but still quite significant. 

# <markdowncell>

# ## Web frameworks
# 
# These are important infrastructural components. Most websites rely on them today. So there are quite a few of them. 

# <codecell>

#  http://hotframeworks.com/ has a ranked list

wflist_df = pd.read_csv('topic_lists/webframe_list.csv', header=None, names=['name'])

# <codecell>

print(wflist_df.shape)
wflist_df.head()

# <codecell>

wfquery = '|'.join(wflist_df['name'][:30]).lower()
wfquery

# <codecell>

wf_df = construct_repo_df(wfquery)

# <codecell>

red.sadd('webframeworks', *wf_df.full_name)

# <markdowncell>

# 0.1M Are there really that many projects working on webframeworks. Or is that these frameworks are widely used, but not actually under development. 

# <markdowncell>

# # Javascript frontend libraries
# 
# Some of these are hard to differentiate, because javascript is now becoming a server technology, and an application framework. There are 50 libraries in use.

# <codecell>

javascript_list = pd.read_csv('topic_lists/javascript_front.csv', header=None, names=['name'])
javascript_query = 'widget|'+'|'.join(javascript_list.name.str.strip()).lower()

# <codecell>

javascript_query

# <codecell>

javascript_df = construct_repo_df(javascript_query)

# <codecell>

red.sadd('web_frontend_javascript', *javascript_df.full_name)

# <markdowncell>

# A small list of libraries, but a lot of repos -- 0.2M

# <markdowncell>

# ## CSS processors
# 
# Again, these are widely used components for structuring the content of webpages. A couple of dozen are in use. 

# <codecell>

csslist = pd.read_csv('topic_lists/css_list.csv', header=None, names = ['name'])
csslist.head()

# <codecell>

cssquery = 'css|'+'|'.join(csslist['name'][:30]).lower()
cssquery

# <codecell>

css_df = construct_repo_df(cssquery)

# <codecell>

red.sadd('css', *css_df.full_name)

# <codecell>

css_df.head(10)

# <markdowncell>

# Quite a lot here -- around 0.2 M

# <markdowncell>

# ## Git and github related tools

# <codecell>

git_query = 'git|(github)'
git_df = construct_repo_df(git_query, description=False)

# <codecell>

git_df.head(20)
red.sadd('git', *git_df.full_name)

# <markdowncell>

# Ok, as expected, quite a few here. I haven't worked out a way to exclude all the 

# <markdowncell>

# ## Editor and command configs - dot files
# 
# I'm thinking these are really important to programmers work. They are commonly known as 'dotfiles.' The query here is very loose. There might be additional terms needed. 

# <codecell>

dotquery = 'bash|zsh|tmux|csh|vim|emacs|dot?file'
dot_df = construct_repo_df(dotquery)
red.sadd('dot_files', *dot_df.full_name)

# <markdowncell>

# Again, quite a few here - around 0.15 M.

# <markdowncell>

# ## Server admin, virtualization and infrastructures
# 
# These are quite large low level bodies of software, including cloud, virtualization, application servers, etc. This list is from newrelic.com. Again, around 120 exist. 

# <codecell>

server = pd.read_csv('topic_lists/opsadmin.csv', header=None, names = ['name', 'type'], na_filter=True, sep='\t')
print server.shape
server.dropna(inplace=True)
server.head()

# <codecell>

serverquery   = '|'.join(server['name'].str.strip()).lower()
serverquery

# <codecell>

server_df = construct_repo_df(serverquery, description=False)

# <codecell>

server_df.head(20)

# <codecell>

red.sadd('servers', *server_df.full_name)

# <markdowncell>

# Around 0.3 M repos here

# <markdowncell>

# ## Hardware devices and platforms

# <codecell>

device_query = 'arduino|raspberry|android|ios|blackberry|armv|symbian'

# <codecell>

devices_df = construct_repo_df(device_query)

# <codecell>

red.sadd('devices', *devices_df.name)

# <codecell>

devices_df.head()

# <markdowncell>

# Ok, around 0.35M repos again -- this starting to sound familiar! Quite interesting to look more at ARM architectures, and perhaps follow up the very notion of architecture through code. 

# <markdowncell>

# ## Social media platforms
# 
# This is a huge one, combining several of the previous ones, again with several hundred cases

# <codecell>

socialmedia = pd.read_csv('topic_lists/social_media.csv', header=0)
socialmedia.shape
socialmedia.head()

# <codecell>

socialmediaquery = 'wikipedia|'+'|'.join(socialmedia['name'].str.strip()).lower()
print socialmediaquery

# <codecell>

socialmedia_df = construct_repo_df(socialmediaquery, description = False)

# <codecell>

red.sadd('social_media', *socialmedia_df.full_name)

# <markdowncell>

# Almost 157k repositories here. Is that mostly noise?

# <codecell>

socialmedia_df.head(30)

# <markdowncell>

# ## Internet and communication protocols
# 
# Again, these are so numerous when you take into account all the different ways computers talk to each other, and these protocols themselves could be a kind of map

# <codecell>

iplist  = pd.read_csv('topic_lists/internet_protocols.csv', header=None, names = ['name'])
iplist.shape

# <codecell>

ipquery = '|'.join(iplist['name'].str.strip()).lower()
print ipquery

# <codecell>

ip_df = construct_repo_df(ipquery)

# <codecell>

red.sadd('internet_protocols', *ip_df.full_name)

# <codecell>

ip_df.head(10)

# <markdowncell>

# Some of these look a little bit irrelevant, but even if only 50% are right, there are still 100k internet protocol related projects.

# <markdowncell>

# ## Machine learning code

# <codecell>

ml_list = pd.read_csv('topic_lists/ml.csv', header=None, names = ['name'])
ml_list.shape
ml_query  = 'data mining|machine learning|feature selection|prediction|' + '|'.join(ml_list['name'].str.strip()).lower()

# <codecell>

ml_df = construct_repo_df(ml_query, description=False, local=True)

# <codecell>

red.sadd('machine_learning', *ml_df.full_name)

# <codecell>

ml_df.head(10)

# <markdowncell>

# These results look a bit strange. Around 100k, so should be able find something here. 

# <markdowncell>

# ## Scientific software
# 
# This is a huge topic. I have a list of around 1000 fields

# <codecell>


scilist  = pd.read_csv('topic_lists/science.csv', header=None, names = ['name'])
scilist.shape
sci_qs = []
for i in range(100, scilist.shape[0], 100):
    sci_qs.append('|'.join(scilist['name'][i-100:i].str.strip()).lower())

# <codecell>

sci_dfs = []
for qu in sci_qs:
    sci_dfs.append(construct_repo_df(qu))

# <codecell>

sci_df = pd.DataFrame()
for df in sci_dfs:
    sci_df = sci_df.append(df)
print sci_df.shape
sci_df.head()

# <codecell>

red.sadd('science', *sci_df.full_name)

# <markdowncell>

# Ok, 0.17M -- not a huge amount but worth tracking a bit more

# <markdowncell>

# ## Geo, gis and mapping software
# 
# Mapserver is one of the most active repos on github. I gleaned a list from http://en.wikipedia.org/wiki/List_of_geographic_information_systems_software. There is lot of mapping software

# <codecell>

gengeolist  = ['gis', 'geo']
geolist  = pd.read_csv('topic_lists/geo_gis.csv', header=None, names = ['name'])
geolist.shape
geolist.head()

# <codecell>

geoquery = '|'.join(geolist['name'].str.strip()).lower()
geoquery = geoquery + '|geo|gis'
print geoquery

# <codecell>

geo_df = construct_repo_df(geoquery)

# <codecell>

red.sadd('geo_gis', *geo_df.full_name)
geo_df.full_name[:30]

# <markdowncell>

# The usual number here -- around 0.1 M. So substantial, but probably still very noisy

# <markdowncell>

# ## Data manipulations including statistics
# 

# <codecell>

datasoftware = pd.read_csv('topic_lists/data_stats.csv', header=None, names = ['name'])
datasoftware.drop_duplicates(inplace=True)
datasoftware.shape

# <codecell>

data_query1 = 'statistic|data scien|'+'|'.join(datasoftware['name'][:50].str.strip()).lower()
print data_query1
data_query2 = '|'.join(datasoftware['name'][50:100].str.strip()).lower()
print data_query2
data_query3 = '|'.join(datasoftware['name'][100:].str.strip()).lower()
print data_query3

# <codecell>

datastat_df = construct_repo_df(data_query1, description=False, local=True)

# <codecell>

datastat_df.head()

# <codecell>


# <codecell>


# <codecell>

datastat_df2 = construct_repo_df(data_query2, description=False, local=True)

# <codecell>

datastat_df3 = construct_repo_df(data_query3, description=False, local=True)

# <codecell>

delete = False

# <codecell>

datastat_df = pd.concat([datastat_df, datastat_df2, datastat_df3])
datastat_df.drop_duplicates(inplace=True)
print datastat_df.shape
datastat_df.head()

# <codecell>

if delete:
    red.delete('data_statistics')
red.sadd('data_statistics', *datastat_df.full_name)

# <markdowncell>

# The use of these datamining packages is huge. There seems to be around 0.8M. They probably need further analysis

# <markdowncell>

# ## Documents and publishing
# 
# This is an amorphous category but includes word processing, document formats, bibliographic and reference software, markup and publishing software. Mundane but ubiquitous.

# <codecell>

file_formats.domain.value_counts()
docs = file_formats['domain'] == 'document'
pub = file_formats['domain'] == 'desktop publishing'
refs = file_formats['domain'] == 'reference management software'
pres = file_formats['domain'] == 'presentation'
doc_types = file_formats[docs + pub + refs + pres].filetype
# .map(str) + "|" + file_formats[docs + pub + refs].description

doc_query = '\\b' + '\\b|\\b'.join(doc_types.dropna()).lower() + '\\b'
# doc_query

# <codecell>

docs_list = pd.read_csv('topic_lists/docs.csv', header = None, names = ['extension', 'description'])
doc_query = '|'.join(docs_list.extension.str.strip()).lower()
doc_query

# <codecell>

doc_df = construct_repo_df(doc_query, description=False)

# <codecell>

red.sadd('documents', *doc_df.full_name)

# <codecell>

doc_df.ix[60:100]

# <markdowncell>

# ## Github as a blog or webpage
# 
# Lots of repositories are actually blogs or webpages. This shows up in the repo name

# <codecell>

page_query  = 'github.com|github.io'
page_df = construct_repo_df(page_query, description = False)
red.sadd('github_webpages', *page_df.full_name)

# <markdowncell>

# 0.15M repos used as blogs or webpages

# <markdowncell>

# ## Policies, laws, standards, manifestos
# 
# Are there lots of legal documents on Github?

# <codecell>

policy_query = '|'.join(['policy', 'law', 'manifesto', 'agreement', 'guideline'])

policy_df = construct_repo_df(policy_query)

# <codecell>

red.sadd('policy_law', *policy_df.full_name)

# <codecell>

policy_df.head()

# <markdowncell>

# ## Books, buides, and articles
# 
# Are there lots of writing projects on Github?

# <codecell>

bookquery = '|'.join(['book', 'article', 'guide', 'how to', 'manual'])
print bookquery
book_df = construct_repo_df(bookquery)

# <codecell>

red.sadd('books_manuals', *book_df.full_name)

# <codecell>

book_df.head(10)

# <markdowncell>

# Around 0.25M. Need to check if these are too noisy, but they seem ok overall.

# <markdowncell>

# ## The image/video software
# 
# I'm thinking this will be quite important in terms of applications

# <codecell>

image_terms = ['video','image','jpeg', 'mp3', 'mpeg', 'audio', 'sound','photograph', 'camera', 'webcam']
image_query = '|'.join(image_terms)

# <codecell>

image_df = construct_repo_df(image_query)

# <codecell>

red.sadd('images', *image_df.full_name)

# <markdowncell>

# Ok, _195k_ is not so many. Perhaps need to add more terms here. 

# <codecell>

image_df.head(10)

# <markdowncell>

# ## Games and gaming

# <codecell>

game_list  = ['game', 'xbox', 'playstation', 'wii', 'kinect', 'nintendo', 'minecraft', 'warcraft', 'multiplayer']
game_query = '|'.join(game_list)

# <codecell>

game_df = construct_repo_df(game_query)
red.sadd('gaming', *game_df.full_name)

# <codecell>

game_df.head(10)

# <markdowncell>

# Again, around 150k hits here, but probably could be expanded quite a bit. 

# <markdowncell>

# 
# ## Icons, fonts and themes
# 
# I'm not whether these matter, but they are a showcase on Github

# <codecell>

iconlist = ['icon','font', 'emoji', 'theme']
iconquery = '|'.join(iconlist)
print iconquery

# <codecell>

icon_df = construct_repo_df(iconquery)

# <codecell>

red.sadd('icons_fonts', *icon_df.full_name)

# <codecell>

icon_df.head()

# <markdowncell>

# Around 100k repos on this, which is a lot, given that they don't that much ... 

# <markdowncell>

# ## Education platforms and moocs

# <codecell>

education = 'mooc|coursera|EdX|khan academy|opencourseware|P2PU|Udacity|Udemy'
edu_query = education.lower()
edu_df = construct_repo_df(edu_query)
red.sadd('education', *edu_df.full_name)

# <codecell>

red.sadd('moocs', *edu_df.full_name)
edu_df.head()

# <markdowncell>

# ## APIS and SDKs

# <codecell>

api_query = 'api|sdk'
api_df = construct_repo_df(api_query, description=False)

# <codecell>

red.sadd('api_sdk', *api_df.full_name)

# <markdowncell>

# # Save dataframes to redis for analysis

# <codecell>

red = redis.Redis(db='1')

# <codecell>

pipe = red.pipeline()

for i in range(0, editor_df.shape[0], 100000):
    pipe.sadd('editors', *editor_df.full_name[i:i + 100000])
res = pipe.execute()

# <codecell>

red.sadd('servers', *server_df.full_name)
red.sadd('ides', *ide_df.full_name)
red.sadd('gaming', *game_df.full_name)
red.sadd('icons_fonts', *icon_df.full_name)
red.sadd('images', *image_df.full_name)
red.sadd('books_manuals', *book_df.full_name)
red.sadd('data_statistics', *datastat_df.full_name)
red.sadd('geo_gis', *geo_df.full_name)
red.sadd('machine_learning', *ml_df.full_name)
red.sadd('internet_protocols', *ip_df.full_name)
red.sadd('social_media', *socialmedia_df.full_name)
red.sadd('devices', *devices_df.full_name)
red.sadd('packages', *package_df.full_name)
red.sadd('databases', *db_df.full_name)
red.sadd('webframeworks', *wf_df.full_name)
red.sadd('css', *css_df.full_name)
red.sadd('dotfiles', *dot_df.full_name)
red.sadd('webpages', *page_df.full_name)
red.sadd('tests', *test_df.full_name)
red.sadd('git', *git_df.full_name)
red.sadd('web_frontend_javascript', *javascript_df.full_name)
red.sadd('compilers', *compiler_df.full_name)
red.sadd('integration', *integration_df.full_name)
red.sadd('policy_law', *policy_df.full_name)
red.sadd('science', *sci_df.full_name)
red.sadd('documents', *doc_df.full_name)
red.sadd('spam', *spam_df.full_name)

# <codecell>

red.sadd('moocs', *edu_df.full_name)
red.sadd('spam', *spam_df.full_name)

# <codecell>


