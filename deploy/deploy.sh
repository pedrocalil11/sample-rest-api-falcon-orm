echo "=============== Creating credentials file ================"
mkdir ~/.aws/
touch ~/.aws/credentials
printf "[default]\naws_access_key_id = %s\naws_secret_access_key = %s\n" "$%%ENVIRONMENT%%_AWS_ACCESS_KEY_ID" "$%%ENVIRONMENT%%_AWS_SECRET_ACCESS_KEY" >> ~/.aws/credentials

echo "================ Building image ======================="
sed -i 's/$$GIT_COMMIT/'$CI_COMMIT_SHA'/g' ./src/constants.py
sed -i 's/$$GIT_BRANCH/'$CI_COMMIT_REF_SLUG'/g' ./src/constants.py

ECR_IMAGE="$%%ENVIRONMENT%%_AWS_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"

docker build -t $ECR_IMAGE .

echo "=============Starting docker containers============="
docker-compose up -d
apk add --update python3 python3-dev py3-pip
pip3 install awscli --upgrade

cd test
sleep 50
echo "===================Starting tests==================="
{
    pytest --html=output.html --self-contained-html && 
    docker logs -t sample_api > api_logs.txt
} || {
    docker logs -t sample_api > api_logs.txt
    exit 1
}
echo "===================Finished tests==================="
docker-compose down -v
cd ..


echo "===================Inserting vars on TD==================="
sed -i "s|%DB_HOSTNAME|$%%ENVIRONMENT%%_DB_HOSTNAME|g" ./deploy/task-definition.json
sed -i "s|%DB_PASSWORD|$%%ENVIRONMENT%%_DB_PASSWORD|g" ./deploy/task-definition.json
sed -i "s|%AWS_REGION|$%%ENVIRONMENT%%_AWS_REGION|g" ./deploy/task-definition.json
sed -i "s|%EXECUTION_ROLE_ARN|$%%ENVIRONMENT%%_EXECUTION_ROLE_ARN|g" ./deploy/task-definition.json
sed -i "s|%TASK_ROLE_ARN|$%%ENVIRONMENT%%_TASK_ROLE_ARN|g" ./deploy/task-definition.json
sed -i "s|%ENVIRONMENT|$CI_ENVIRONMENT_SLUG|g" ./deploy/task-definition.json
sed -i "s|%ECR_IMAGE|$ECR_IMAGE|g" ./deploy/task-definition.json
sed -i "s|%SERVICE_NAME|$%%ENVIRONMENT%%_SERVICE_NAME|g" ./deploy/task-definition.json
sed -i "s|%MASTER_ADMIN_KEY|$%%ENVIRONMENT%%_MASTER_ADMIN_KEY|g" ./deploy/task-definition.json

echo "=================== Get Login Stage ==================="
$(aws ecr get-login --no-include-email --region $%%ENVIRONMENT%%_AWS_REGION | tr -d '\r')

echo "===================Pushing docker image==================="
docker push $ECR_IMAGE

echo "===================Register Task Definition==================="
aws ecs register-task-definition --family $%%ENVIRONMENT%%_SERVICE_NAME --cli-input-json file://deploy/task-definition.json --region $%%ENVIRONMENT%%_AWS_REGION
aws ecs update-service --cluster sample-cluster --service $%%ENVIRONMENT%%_SERVICE_NAME --task-definition $%%ENVIRONMENT%%_SERVICE_NAME --region $%%ENVIRONMENT%%_AWS_REGION