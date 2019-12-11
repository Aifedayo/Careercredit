#!/usr/bin/bash

# deploy|remove dev|int|stage|pro|live region

# DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
create(){
    echo -e "\nStack does not exist, creating ..."
    aws cloudformation create-stack \
        --region $region \
        --stack-name $stack_name \
        --template-body file://cloudformation.json \
        --parameters  $params \
        ${@:4}  | jq '.'
        # ${@:3}  | jq -r .StackId

    echo "Waiting for stack to be created ..."
    aws cloudformation wait stack-create-complete \
        --region $region \
        --stack-name $stack_name 

    aws cloudformation describe-stacks --stack-name $stack_name | jq '.'
}

update(){
    echo -e "\nStack exists, attempting update ..."

    set +e
    update_output=$( aws cloudformation update-stack \
        --region $region \
        --stack-name $stack_name \
        --template-body file://cloudformation.json \
        --parameters  $params \
        ${@:4}  2>&1)
    status=$?
    set -e

    echo "$update_output"

    if [ $status -ne 0 ] ; then

        # Don't fail for no-op update
        if [[ $update_output == *"ValidationError"* && $update_output == *"No updates"* ]] ; then
            echo -e '{"msg":"Finished update - no updates to be performed"}' | jq '. |.msg'
            exit 0
        else
            exit $status
        fi

    fi

    echo "Waiting for stack update to complete ..."
    aws cloudformation wait stack-update-complete \
        --region $region \
        --stack-name $stack_name 
    echo '{"msg":"Finished update successfully!"}' | jq '. |.msg'
}

delete(){
    echo -e "\nStack exists, attempting delete ..."

    set +e
    delete_output=$( aws cloudformation delete-stack \
        --region $region \
        --stack-name $stack_name \
        ${@:4}  2>&1)
    status=$?
    set -e

    if [ $status -ne 0 ] ; then
        echo "An error occure while trying to delete stack"
        exit $status
    fi

    echo "Waiting for stack delete to complete ..."
    aws cloudformation wait stack-delete-complete \
        --region $region \
        --stack-name $stack_name 
    echo '{"msg":"Finished delete successfully!"}' | jq '. |.msg'
}

stack_not_exits(){
    stack_output=$( aws cloudformation describe-stacks \
        --region $region \
        --stack-name $stack_name 2>&1)
    [[ $stack_output == *"ValidationError"* && \
    $stack_output == *"does not exist"* ]]
}

random_string(){
  local random_str="$( \
        cat /dev/urandom | \
        tr -dc 'a-zA-Z0-9' | \
        fold -w ${1:-32} | \
        head -n 1 )"
  echo "$random_str"
}

usage="Usage: $(basename "$0") deploy|remove dev|int|stage|pro|live region [aws-cli-opts]
where:
  deploy       - deploy the api gateway
  remove       - remove the api gateway
  region       - the AWS region
  stack-name   - the stack name
  aws-cli-opts - extra options passed directly to create-stack/update-stack
"

if [ "$1" == "-h" ] || [ "$1" == "--help" ] || [ "$1" == "help" ] || [ "$1" == "usage" ] ; then
  echo "$usage"
  exit -1
fi

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ] ; then
  echo "$usage"
  exit -1
fi

shopt -s failglob
set -eu -o pipefail

#setup var and parameters
action=$1
stage=$2
region=$3
stack_name="groupclass-websocket-api-gateway-$stage"
params="ParameterKey=Stage,ParameterValue=$stage"
site_url="https://${stage}.linuxjobber.com"
new_deployment_name="WebsocketsDeployment"
new_deployment_name+="$( random_string 16 )"

if [ "$stage" != "pro" ]; then
    params+=" ParameterKey=BaseUrl,ParameterValue=$site_url"
fi

#rename WebsocketsDeployment in cloudformation file
sed -i "s/WebsocketsDeployment1/$new_deployment_name/g" cloudformation.json

#install jq if not present on pc (&> redirect both std[out/err])
if ! command -v jq &> /dev/null; then
    sudo yum install jq -y
    clear
fi

#deploy api
if [ "$action" == "deploy" ]; then
    echo "Checking if stack exists ..."

    if stack_not_exits; then
        create
    else
        update
    fi

    exit 0
fi

#remove api
if [ "$action" == "remove" ]; then
    echo "Checking if stack exists ..."
    
    if stack_not_exits; then
        echo "The specify stack does not exists"
    else
        delete
    fi     

    exit 0   
fi

#rename WebsocketsDeployment back in cloudformation file
sed -i "s/$new_deployment_name/WebsocketsDeployment1/g" cloudformation.json