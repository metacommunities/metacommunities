### Setup

Install dependencies:

    sudo pip install MySQLdb pandas requests PyGithub

Copy `settings.conf` to `~\.history-git\settings.conf` and fill in the details.

The first time you run `history-git.py` it will connect to your MySQL instance
and create the tables as described below in **Schema**. After that it will
begin fetching the event history for each of the repositories listed in
`repos.txt`.

### Schema



### repos.txt


### What events are stored?



