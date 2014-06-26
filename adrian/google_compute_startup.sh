# to start

gcutil --service_version="v1" --project="metacommunities" addinstance "instance-1" --zone="europe-west1-b" --machine_type="n1-standard-2" --network="default" --external_ip_address="ephemeral" --metadata="sshKeys:" --service_account_scopes="https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/bigquery" --disk="instance-1,deviceName=instance-1,mode=READ_WRITE,boot"  --auto_delete_boot_disk="false"

# to stop
gcutil --project="metacommunities" deleteinstance "instance-1"

#attach data disk
gcutil attachdisk  --project="metacommunities"  --zone="europe-west1-b"  --disk="disk-1,deviceName=disk-1,mode=READ_WRITE" "instance-1"

# to fix ssh
eval `ssh-agent -s`
ssh-add ~/.ssh/google_compute_engine

##ssh into instance
gcutil ssh "instance-1"

#mount disk first
sudo /usr/share/google/safe_format_and_mount -m "mkfs.ext4 -F" /dev/disk/by-id/scsi-0Google_PersistentDisk_disk-1 /git_data

# start redis
sudo /etc/init.d/redis_6379 start
sudo /etc/init.d/redis-server stop
# sudo redis-server /etc/redis/6379.conf 

# to get some github archive files
wget http://data.githubarchive.org/2012-07-{01..31}-{0..23}.json.gz