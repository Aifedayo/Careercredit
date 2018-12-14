#!/bin/bash
appPath=$2

#
# script to transfer clientapp and all necessary artificats to client machine
# once transfer is complete to client machine, just go to client machine and run #./setup /opt/ gclient server 
#     where gclient above instructs the setup script to install only grader client 
#     where server above only refers to os versions
#     then run #service chuckService start
#
# run this script as, for example, deploy_clientapp.sh 12.23.12.123 /full/path/to/whereDScriptShouldReside
#

#[ -s GraderClient.py ] || { echo "the file GraderClient.py is missing in this location. Provide the file to continue" && exit 1; }
#[ $(find . -type f -name "logging.ini") != "" ] || { echo "the file logging.ini is missing in this location. Provide the file to continue" && exit 1; }

#cfLPath=$(find . -type f -name "logging.ini")
#scp GraderClient.py $cfLPath sysadmin@$1:/tmp
#ssh sysadmin@$1 sudo "mkdir -p $appPath/{conf,logs};
#sudo chown sysadmin:sysadmin $appPath/{conf,logs}; 
#sudo mv -f /tmp/GraderClient.py $appPath; 
#sudo mv -f /tmp/logging.ini $appPath/conf;
#sudo touch $appPath/logs/graderclient.log;
#sudo chown -R sysadmin:sysadmin $appPath/{GraderClient.py,conf,logs}; 
#chmod 744 $appPath/logs; chmod 700 $appPath/conf"

sshpass -p '8iu7*IU&' scp -o StrictHostKeyChecking=no  -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null /linuxdev/Django/Linuxjobber/home/utils/python/GraderClient.py sysadmin@$1:$2
sshpass -p '8iu7*IU&' ssh -o StrictHostKeyChecking=no  -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null  sysadmin@$1 mkdir $2/conf
sshpass -p '8iu7*IU&' ssh -o StrictHostKeyChecking=no  -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null sysadmin@$1 mkdir $2/logs
sshpass -p '8iu7*IU&' scp -o StrictHostKeyChecking=no  -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null /linuxdev/Django/Linuxjobber/home/utils/conf/logging.ini sysadmin@$1:$2/conf/

