This is my attempt to document my method of getting a Stack Overflow data dump
on to Google BigQuery and Google Cloud SQL.

First grab the torrent for latest data dump from
[ClearBits](http://www.clearbits.net/creators/146-stack-exchange-data-dump).

Once downloaded, take the files from this repo and place them in the
directory of the torrented files i.e. inside 'stackexchange' and
then open up a terminal and enter:

        ./upload_so

## Dependencies

I'm running Ubuntu 12.04 and here's all the packages I think I had to
install:

        sudo apt-get install p7zip-full
        sudo pip install MySQL-python


You'll need a couple of tools but they're not in Ubuntu repo:
- [BigQuery command line tool](https://developers.google.com/bigquery/docs/cli_tool)
- [Google Storage tool](https://developers.google.com/storage/docs/gsutil)

You'll also need a local MySQL instance.

## Method

The current method is for uploading to big query:
- convert the XML files to JSON, and compress
- using the schema for each table (see `/schema`), upload directly to big query

For cloud storage things are a bit more tedious:
- import XML into local instance of MySQL
- dump tables to SQL files
- upload to google storage
- go to the cloud SQL settings on the developers console on google and import 
from there, specifying the database i.e. `so`

## Question tags

Questions on stackoverflow are tagged (max number of tags is 5). But in the
database these are stored in a single field like this; `<tag1><tag2>...<tag5>`.
The `create_tag.py` script will split this field out and create two new tables;
a 'tags' and a 'posttags' table.

The 'tags' table will look like this:
        +----+---------------+-------+----------------+---------------------+
        | id | tag           | count | first_question | first_question_date |
        +----+---------------+-------+----------------+---------------------+
        |  1 | .a            |    43 |        2157629 | 2010-01-28 20:14:23 |
        |  2 | .app          |    60 |        1710893 | 2009-11-10 20:17:10 |
        |  3 | .aspxauth     |    31 |        2122831 | 2010-01-23 10:33:10 |
        |  4 | .bash-profile |   178 |         902946 | 2009-05-24 02:37:21 |
        |  5 | .class-file   |   103 |        1768256 | 2009-11-20 04:01:01 |
        |  6 | .cs-file      |    28 |         236403 | 2008-10-25 13:28:29 |
        |  7 | .doc          |    83 |        1043768 | 2009-06-25 13:00:33 |
        |  8 | .each         |   353 |        2311618 | 2010-02-22 14:52:12 |
        |  9 | .emf          |    41 |         152729 | 2008-09-30 11:59:49 |
        | 10 | .hgtags       |     7 |        5080291 | 2011-02-22 15:40:27 |
        +----+---------------+-------+----------------+---------------------+

While 'posttags' will look like this:
        +------+---------------------+-------+---------------------+
        | pid  | tag                 | tid   | post_creation_date  |
        +------+---------------------+-------+---------------------+
        |    4 | c#                  |  3692 | 2008-07-31 21:42:52 |
        |    4 | forms               | 11071 | 2008-07-31 21:42:52 |
        |    4 | type-conversion     | 31985 | 2008-07-31 21:42:52 |
        |    4 | winforms            | 34357 | 2008-07-31 21:42:52 |
        |    4 | opacity             | 21691 | 2008-07-31 21:42:52 |
        |    6 | css3                |  6352 | 2008-07-31 22:08:08 |
        |    6 | internet-explorer-7 | 14703 | 2008-07-31 22:08:08 |
        |    6 | html                | 13439 | 2008-07-31 22:08:08 |
        |    6 | css                 |  6312 | 2008-07-31 22:08:08 |
        |    8 | c#                  |  3692 | 2008-07-31 23:33:19 |
        +------+---------------------+-------+---------------------+

For bigquery, these will be dumped to CSV and uploaded. While for Cloud SQL,
a straight SQL dump will be used.

## Warnings

The 'posts' table is big, make sure you've got a constant Internet connection
because it's going to take a few hours.

