#!/bin/sh

source ~/projects/my_env

# build
cd lambda
./build.sh
cd ..

# deploy
cd terraform
echo "REDDIT_CLIENT_ID = \"${REDDIT_CLIENT_ID}\"" >> terraform.tfvars
echo "REDDIT_CLIENT_SECRET = \"${REDDIT_CLIENT_SECRET}\"" >> terraform.tfvars
echo "REDDIT_CLIENT_USERNAME = \"${REDDIT_CLIENT_USERNAME}\"" >> terraform.tfvars
echo "REDDIT_CLIENT_PASSWORD = \"${REDDIT_CLIENT_PASSWORD}\"" >> terraform.tfvars
echo "REDDIT_SUBREDDIT = \"${REDDIT_SUBREDDIT}\""  >> terraform.tfvars
if [ ! -z "$SCHEDULE" ] ; then echo "SCHEDULE = \"${SCHEDULE}\"" >> terraform.tfvars; fi
cat terraform.tfvars | awk '{ print $1}'
terraform init -reconfigure -backend-config=${REDDIT_SUBREDDIT}.tfbackend
terraform plan -out tfplan
terraform apply tfplan

# reset vars
git checkout terraform.tfvars
