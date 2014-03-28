#!/bin/bash

MYSQL_USER="root"
MYSQL_HOST="173.194.105.217"
read -p "Enter password for localhost: " -s MYSQL_PASSWD

SODIR='stackoverflow.com'
CSVDIR="${SODIR}_CSV"
JSONDIR="${SODIR}_JSON"
SQLDIR="${SODIR}_SQL"

GSDIR="sandboxx"

# extract just stackoverflow
7za e 'stackoverflow.com-*.7z' -o$SODIR

# interesting tables 
declare -a TBL=("posts" "users") # "badges" "comments" "votes"


# ==============================================================================
# load into local mysql instance
# ==============================================================================
mysql -u $MYSQL_USER -p$MYSQL_PASSWD -e 'CREATE DATABASE IF NOT EXISTS so;'
mkdir $SQLDIR

for i in "${TBL[@]}"
do
    echo "$i table."
    echo "  Importing."
    mysql -u $MYSQL_USER -p$MYSQL_PASSWD so < import_$i.sql
    echo "  Dumping."
    mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD so $i | gzip > $SQLDIR/$i.sql.gz
done

# ------------------------------------------------------------------------------
# create a 'tag' table from the 'tags' field in 'post' table
# ------------------------------------------------------------------------------
# create
python create_tag_files.py -u $MYSQL_USER -p $MYSQL_PASSWD --host $MYSQL_HOST
# import
mysql -u $MYSQL_USER -p$MYSQL_PASSWD so < import_tags.sql
# dump
mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD so tags     | gzip > $SQLDIR/tags.sql.gz
mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD so posttags | gzip > $SQLDIR/posttags.sql.gz

# ------------------------------------------------------------------------------
# upload to google storage
# ------------------------------------------------------------------------------
gsutil md gs://$GSDIR
FILES=`ls $SQLDIR`
for f in $FILES
  do
  gsutil cp $SQLDIR/$f  gs://$GSDIR/$f
done

echo -e '\nAll done. Now go manually import the tables into Cloud SQL via google console.\n'


# ==============================================================================
# iterate over the XML and convert to JSON
#   -i    input dir
#   -t    table to convert
#   -s    split size (MB) of JSON file (default is no split)
# ==============================================================================
echo -e '\n\nConverting XML to JSON for BigQuery.\n'
#python convert_xml_to_json.py -i$SODIR -t'Badges'   -s2000 
#python convert_xml_to_json.py -i$SODIR -t'Comments' -s2000 
python convert_xml_to_json.py -i$SODIR -t'Posts'    -s2000 
python convert_xml_to_json.py -i$SODIR -t'Users'    -s2000 
#python convert_xml_to_json.py -i$SODIR -t'Votes'    -s2000 


# ==============================================================================
# upload stackoverflow to bigquery
# ==============================================================================
# make sure you've ran 'bq init' to setup your credentials
DATASET='stack_overflow'

bq mk $DATASET

function upload2bq {
  FILES=`ls $JSONDIR/$1*`
  for f in $FILES
    do
    echo -e "\n\n\nUploading '${f}' to '${DATASET}.${1}':"
    bq load --source_format=NEWLINE_DELIMITED_JSON "${DATASET}.${1}" $f \
      "schema/${1}"
  done
}

#upload2bq 'badges'
#upload2bq 'comments'
upload2bq 'posts'
upload2bq 'users'
#upload2bq 'votes'


# ==============================================================================
# upload 'tags' and 'posttags' to bigquery
# ==============================================================================
declare -a CSV_TBL=("tags" "posttags")
DATASET='stack_overflow'

mkdir $CSVDIR

for i in "${CSV_TBL[@]}"
do
    echo "Dumping '$i' table to CSV."
    
    mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD \
        --tab /tmp \
        --fields-terminated-by=',' \
        --fields-optionally-enclosed-by='"' \
        --fields-escaped-by='\\' \
        --lines-terminated-by='\n' \
        so $i
    
    cp /tmp/$i.txt ./$CSVDIR/$i.csv
    
    echo "Uploading '$i' table to BQ."
    
    bq load --source_format=CSV "${DATASET}.${i}" $CSVDIR/$i.csv \
      "schema/${i}"
done
