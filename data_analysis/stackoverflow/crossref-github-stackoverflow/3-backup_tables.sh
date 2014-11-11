read -p "Enter user for localhost: " -s MYSQL_PASSWD
read -p "Enter password for localhost: " -s MYSQL_PASSWD

declare -a TBL=("url_tag" "tags")
DATASET='stack_overflow'

for i in "${TBL[@]}"
do
    echo "Dumping '$i' table to CSV."
    
    mysqldump -u $MYSQL_USER -p$MYSQL_PASSWD \
        --tab /tmp \
        --fields-terminated-by=',' \
        --fields-optionally-enclosed-by='"' \
        --fields-escaped-by='\\' \
        --lines-terminated-by='\n' \
        so $i
    
    cp /tmp/$i.txt .$i.csv
    
    echo "Uploading '$i' table to BQ."
    
    bq load --source_format=CSV "${DATASET}.${i}" ./$i.csv \
      "schema/${i}"
done
