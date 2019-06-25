#!/bin/bash
aws s3 sync /mnt/static s3://linuxjobbber-assets-$1/static --acl public-read