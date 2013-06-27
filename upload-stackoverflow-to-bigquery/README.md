This is my attempt to document my method of getting a Stack Overflow data dump
on to Google BigQuery.

First grab the torrent for latest data dump from
[ClearBits](http://www.clearbits.net/creators/146-stack-exchange-data-dump).

Once downloaded, take these files and place them in the save directory for the
torrent i.e. inside 'Stack Exchange Data Dump - mmm yyyy' and then do
`./process_so`.

## Dependencies

I'm running Ubuntu 12.04 and here's all the packages I think I had to
install:
`p7zip-full python-sqlite sqlite3`

You'll also need this but it's not in Ubuntu repo:
- [BigQuery command line tool](https://developers.google.com/bigquery/docs/cli_tool)


## Method

The current method is:
- extract the XML files
- import them in to SQLite
- export from SQLite in to CSVs that are under 4GB
- compress each CSV using gzip
- upload them to BiqQuery (started)


## To Do List

- automate uploading to big query

