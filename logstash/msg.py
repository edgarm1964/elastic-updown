#! /usr/bin/python3

import json
import datetime
import os
import sys
import random

def log (msg = None):
    if msg is None:
        return

    #
    # Write JSON string in a log file. You will need a logstash
    # configuration to copy the logging entries into elasticsearch.
    # Something like this:
	# output {
	# 	if ![index] {
	# 		# no index specified, use default
	# 		elasticsearch {
	# 			hosts => ["elastic-elk:9200"]
	# 			index => "logstash-unknown-%{+YYYY.MM.dd}"
	# 		}
	# 	} else {
	# 		# use specified index
	# 		elasticsearch {
	# 			hosts => ["elastic-elk:9200"]
	# 			index => "%{[index]}"
	# 		}
	# 	}
	# }
    #
    # Of course, you could use a filebeat configuration as well.
    with open (os.path.realpath (os.path.expanduser ("~/log/msg.log")), "a+") as fp:
        print (msg, file = fp)

for env in ("jboss", "postgres", "nginx"):
    msg = {
        "clusterenv": "env",
		"clusterid": "cluster1",
		"index": "cluster-status",
		"availability": "up",
		"@timestamp": "YYYY-mm-ddTHH:MM:SS+ZZ:00"
    }

    msg ["@timestamp"] = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat (sep = 'T', timespec = 'seconds')
    if random.randint (0, 1) > 0:
        msg ["availability"] = "up"
    else:
        msg ["availability"] = "down"

    msg["clusterenv"] = env
	msg["clusterid"] = "cluster-" + env

    log (json.dumps (msg))

sys.exit (0)
