#!/bin/bash			
aws s3 sync /mnt/asset s3://$1/assets --acl public-read