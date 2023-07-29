This is a customised script I created myself to install grafana, influx, telegraf and start the services and get everything up and running
Telegraf is an agent which collects/sends logs to various dbs.
InfluxDB we have used influxdb as a database to collect the logs.
Grafana is used as a monitoring tool, a datasource needs to be added with influxdb( check readme below) 


This installtion is intended for Linux systems.

It will install telegraf, influxdb and grafana.
It will configure telegraf to send measurements to influxdb. 

One can login to grafana by browsing to http://localhost:3000
username: admin
password: admin
(you can change upon login)

You need to create a data source with the following details:
from administration choose datasources, create:
	type: influxdb
	url: http://localhost:3000
	username: admin
	password: admin

import the following dashboard from:  https://grafana.com/grafana/dashboards/928-telegraf-system-dashboard/

go to dashboards, new, import json, and paste the json which was downloaded from the above url.

Save and refresh, you should see measurements.