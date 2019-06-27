#!/bin/bash
aws s3 sync /mnt/media s3://linuxjobbber-assets-$1/media --acl public-read
