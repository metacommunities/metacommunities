#!/bin/bash

MYSQL_USER="root"
MYSQL_HOST="173.194.105.217"
read -p "Enter password for localhost: " -s MYSQL_PASSWD

SODIR='stackoverflow.com'
JSONDIR="${SODIR}_JSON"
ZIPDIR="${SODIR}_ZIP"
SQLDIR="${SODIR}_SQL"

GSDIR="sandboxx"

# extract just stackoverflow
7za e 'stackoverflow.com-*.7z' -o$SODIR

# ==============================================================================
# load into local mysql instance
# ==============================================================================
mysql -u $MYSQL_USER -p$MYSQL_PASSWD -e 'CREATE DATABASE IF NOT EXISTS so;'

#mysql -u $MYSQL_USER -p$MYSQL_PASSWD so < import_badges.sql
#mysql -u $MYSQL_USER -p$MYSQL_PASSWD so < import_comments.sql
mysql -u $MYSQL_USER -p$MYSQL_PASSWD so < import_posts.sql
mysql -u $MYSQL_USER -p$MYSQL_PASSWD so < import_users.sql
#mysql -u $MYSQL_USER -p$MYSQL_PASSWD so < import_votes.sql

# dump tables
mkdir stackoverflow.com_SQL
#mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD so badges > $SQLDIR/badges.sql
#mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD so comments > $SQLDIR/comments.sql
mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD so posts > $SQLDIR/posts.sql
mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD so users > $SQLDIR/users.sql
#mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD so votes > $SQLDIR/votes.sql

# upload to google storage
gsutil md gs://$GSDIR
FILES=`ls $SQLDIR`
for f in $FILES
  do
  gsutil cp $SQLDIR/$f  gs://$GSDIR/$f
done

echo -e '\nAll done. Now go manually import the tables via google console.\n'

# ==============================================================================
# iterate over the XML and convert to JSON
#   -i    input dir
#   -t    table to convert
#   -s    split size (MB) of JSON file (default is no split)
# ==============================================================================
#python convert_xml_to_json.py -i$SODIR -t'Badges'   -s2000 
#python convert_xml_to_json.py -i$SODIR -t'Comments' -s2000 
python convert_xml_to_json.py -i$SODIR -t'Posts'    -s2000 
python convert_xml_to_json.py -i$SODIR -t'Users'    -s2000 
#python convert_xml_to_json.py -i$SODIR -t'Votes'    -s2000 


# ==============================================================================
# compress each JSON for uploading
# gz seems to achieve around 70% compression
# ==============================================================================
FILES=`ls $JSONDIR`
for f in $FILES
  do
  gzip -cv $JSONDIR/$f > $ZIPDIR/$f.gz
done

# ==============================================================================
# upload stackoverflow to bigquery
# ==============================================================================
# make sure you've ran 'bq init' to setup your credentials
DATASET='stack_overflow'

bq mk $DATASET

function upload2bq {
  FILES=`ls $ZIPDIR/$1*`
  for f in $FILES
    do
    echo -e "\n\n\nUploading '${f}' to '${DATASET}.${1}':"
    bq load --source_format=NEWLINE_DELIMITED_JSON "${DATASET}.${1}" $f \
      "schema/${1}"
  done
}

upload2bq 'Users'
upload2bq 'Badges'
upload2bq 'Votes'
upload2bq 'Comments'
upload2bq 'Posts'

# ==============================================================================
# create a 'tag' table from the 'tags' field in 'post' table
# ==============================================================================
python create_tag_files.py -u$MYSQL_USER -p$MYSQL_PASSWD -h$MYSQL_HOST 

