UPPER_ENVIRONMENT_NAME=$(echo $CI_ENVIRONMENT_NAME | tr [a-z] [A-Z])
sed -i "s|%%ENVIRONMENT%%|$UPPER_ENVIRONMENT_NAME|g" ./deploy/deploy.sh