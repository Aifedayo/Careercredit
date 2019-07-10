#!/bin/bash			
cd /mnt/assets && aws s3 sync . s3://$1/assets --acl public-read