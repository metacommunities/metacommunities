gcutil --service_version="v1" --project="metacommunities" addinstance "instance-1" --zone="europe-west1-b" --machine_type="n1-standard-1" --network="default" --external_ip_address="ephemeral" --metadata="sshKeys:" --service_account_scopes="https://www.googleapis.com/auth/devstorage.read_only" --disk="instance-1,deviceName=instance-1,mode=READ_WRITE,boot" --auto_delete_boot_disk="false"
#attach data disk
#mount disk
sudo /usr/share/google/safe_format_and_mount -m "mkfs.ext4 -F" /dev/disk/by-id/scsi-0Google_PersistentDisk_disk-1 /git_data

# start redis