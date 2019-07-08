#!/bin/bash
cd /mnt/media && aws s3 sync . s3://$1/media --acl public-read
