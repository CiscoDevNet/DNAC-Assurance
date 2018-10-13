# Assurance API Test Script
This script shows how to use the DNA Center assurance API's.

## Installing
If you are running python2 you will need the requests library.  If you are running and old version of the SSL library you will 
need to update that.
```buildoutcfg
pip install -r requirements.txt

```
## Running the script
The script uses the dnac_config.py file to specify the DNA Center, username and password.
These can also be set using environment variables too.  Run the following commands in the shell (changing the approiate values)

```buildoutcfg
export DNAC="1.1.1.1"
export DNAC_USER="admin"
export DNAC_PASSWORD="password"
export DNAC_PORT=443

```

Once the credentials are set, the script can be run without arguments.  This will assume the current time as a timestamp and access the 
following API
- site-health - shows the health score for the sites
- device-health - shows the health score for network devices
- client-health - shows the health score for clients (user devices)

The --raw option is used to get raw json output and the --timestamp argument returns health score at a specific time (historical).  This timestamp is in milliseconds.
Some examples include
```buildoutcfg
./assurance.py
./assurance.py --raw
./assurnace.py --timestamp <epoc>
```

The following options return client-detail and device-detail information.  Again they can be called with --raw and --timestamp
``
#  these can also be run with --raw and --timestamp
./assurance.py --mac 00:26:08:E0:F4:97
./assurance.py --hostName 3504

```
