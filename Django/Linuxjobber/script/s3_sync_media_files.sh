#!/bin/bash
aws s3 sync /mnt/media s3://$1/media --acl public-read
