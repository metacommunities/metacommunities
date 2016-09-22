#!/bin/bash
cat jobids.txt|while read job
do
    echo $job
    bq show --format json -j $job >> data/jobs.json
done
