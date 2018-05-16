#!/bin/bash
set -e

# Variables expected to be set in the container environment
# - $environment
# - $instance_private_ip
# - $product
# - $repo_root
# - $requirements_file
# - $secrets_file
# - $uwsgi_file

cd $repo_root

export_environment_variables () {
  echo "[ENTRYPOINT] Exporting environment variables..."
  export PYTHONPATH=$repo_root
  export REPO_ROOT=$repo_root
}

run_migration () {
  echo "[ENTRYPOINT] Running DB upgrade..."
  alembic upgrade head
}

start_app_in_background () {
  echo "[ENTRYPOINT] Starting app in background..."
  uwsgi --ini $uwsgi_file
  tail -f /dev/null
}

fetch_secrets_file () {
  if [[ $environment == "prod"  ]]  || [[ $environment == "latest"  ]]; then
    echo "[ENTRYPOINT] Fetching configuration for $product..."
    curl -sS --fail -o $secrets_file "http://config-$environment.central:8080/getconfig?s3bucket=$s3bucket&product=$product"
    echo "[ENTRYPOINT] Succesfully fetched configuration for $product"
  elif [[ $environment == "staging" ]]; then
    echo "[ENTRYPOINT] Fetching configuration for $product..."
    curl -sS --fail -o $secrets_file ${config_url}
    echo "[ENTRYPOINT] Succesfully fetched configuration for $product"
  else
    if [[ -f $secrets_file ]] ; then
      echo "[ENTRYPOINT] Application configuration $secrets_file exists"
    else
      echo "[ENTRYPOINT] Copy secrets file ${secrets_file}.sample"
      cp -n $secrets_file.sample $secrets_file
    fi
  fi
}

start_worker () {
  echo "[ENTRYPOINT] Starting Worker: $worker_cmd"
  eval $worker_cmd
}

run_prod () {
  set +e
  fetch_secrets_file

  if [[ -z $worker_cmd ]]; then
    if [[ $environment == "latest"  ]]; then
      run_migration
    fi
    start_app_in_background
  else
    start_worker
  fi
}

run_staging () {
  set +e
  fetch_secrets_file
  echo "[ENTRYPOINT] Replacing $instance_private_ip in $secrets_file"
  # sed -i "s/{instance_private_ip}/$instance_private_ip/g" ${secrets_file}
  # sed -i "s#{SQS_QUEUE_URI}#${SQS_QUEUE_URI}#g" ${secrets_file}
  # touch $repo_root/newrelic.ini

  if [[ -z $worker_cmd ]]; then
    run_migration
    start_app_in_background
  else
    start_worker
  fi
  tail -f /dev/null
}

run_local () {
  fetch_secrets_file

  if [[ -z $worker_cmd ]]; then
    sleep 5
    run_migration
    start_app_in_background
  else
    start_worker
  fi
  tail -f /dev/null
}

export_environment_variables

if [[ $environment == "prod"  ]]  || [[ $environment == "latest"  ]]; then
  run_prod
elif [[ $environment == "staging" ]]; then
  run_staging
else
  run_local
fi
