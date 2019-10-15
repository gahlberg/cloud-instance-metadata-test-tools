#!/usr/bin/python

import requests
print 'Hostname: ' + requests.get("http://169.254.169.254/latest/meta-data/local-hostname/").text
print 'Private-ipv4-Address: ' + requests.get("http://169.254.169.254/latest/meta-data/local-ipv4/").text
print 'MAC-Address: ' + requests.get("http://169.254.169.254/latest/meta-data/mac/").text

