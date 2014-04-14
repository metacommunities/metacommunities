### Setup

Install dependencies:

    sudo pip install MySQLdb pandas requests PyGithub

Copy `settings.conf` to `~\.history-git\settings.conf` and fill in the details.

The first time you run `history-git.py` it will connect to your MySQL instance
and create the tables as described below in **Schema**. After that it will
begin fetching the event history for each of the repositories listed in
`owner-repo.txt`. Though you can also specifiy particular owner_repos on the
command line but I would advise against this, and instead maintain the list.

To get started run the following:

        python history-git.py

You will be asked if you would History Git to scrape the names of all currently
existing repos on github. If you've never run this before it will take a long
time, 10 million 'owner/repo' names takes about 5 days.

To request scraping of events for a particular repo on the command line do:

        python history-git.py '<owner1>/<repo1>' '<owner2>/<repo2>'

### Why would I want a list of all currently existing repo names?

First off, you probably do not want this. We use this list to identify whether
or not repos that are visible on the GitHub Event Timeline Archive are in fact
still around or have been deleted. We have to do it this way as there does not
exist a delete event.

If you never want History Git to scrape a list of names (which is likely) then
set `get_repo_names = False` in `settings.conf`.

### Schema

Five tables are currently used.


### What events are stored?

 - commits
 - forks
 - pull requests
 - issues

