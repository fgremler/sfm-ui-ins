#!/bin/bash
set -e

sh /opt/sfm-setup/setup_reqs.sh
appdeps.py --wait-secs 90 --port-wait db:5432 --file /opt/sfm-ui --port-wait mq:5672 --port-wait ui:8080 --file-wait /sfm-data/collection_set

echo "Running consumer"
exec gosu sfm /opt/sfm-ui/sfm/manage.py startconsumer
