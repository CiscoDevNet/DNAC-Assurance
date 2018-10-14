# Assurance API Test Script
This script shows how to use the DNA Center assurance API's.

DNA Center 1.2.5 is required as it has the platform API, which include Assurance.

## Installing
If you are running python2 you will need the requests library.  If you are running and old version of the SSL library you will 
need to update that.
```buildoutcfg
pip install -r requirements.txt

```
## Running the script
The script uses the dnac_config.py file to specify the DNA Center, username and password.
These can also be set using environment variables too.  Run the following commands in the shell (changing the appropriate values)

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
```
#  these can also be run with --raw and --timestamp
./assurance.py --mac 00:26:08:E0:F4:97
./assurance.py --hostName 3504

```

## Example
```buildoutcfg
$ ./assurance.py
https://adam-dnac:443/dna/intent/api/v1/site-health?timestamp=
Site Health
SiteName            SiteType  Issues  RouterHealth  AccessHealth  
 All Sites          area      None    100           80            
NSD-5               building  None    None          None          
 All Buildings      building  None    100           80            
DMZ                 building  None    100           None          
san jose            building  None    None          None          
MEL1                building  None    None          None          
Melbourne           area      None    None          None          
Melbourne Campus1   area      None    None          None          
STL-3               building  None    100           100           
Sydney              area      None    100           100           


https://adam-dnac:443/dna/intent/api/v1/client-health?timestamp=1539408888000
Client health @ 2018-10-13 16:27:00 <-> 2018-10-13 16:32:00 (1539408420000-1539408720000)
ALL 12
WIRED 9
 POOR (1) rootCause:AAA(1)
 FAIR (0) 
 GOOD (8) 
 IDLE (0) 
 NEW (0) 
WIRELESS 3
 POOR (1) rootCause:OTHER(1)
 FAIR (0) 
 GOOD (2) 
 IDLE (0) 
 NEW (0) 


https://adam-dnac:443/dna/intent/api/v1/network-health?timestamp=
Network Health: 89% at 2018-10-13 16:26:00

 Devices Monitored 17, unMonitored 2
Category   Score     Good%     KPI
 Access    60        60        MEMORY:POOR  
 Router    100       100       
 Wireless  86        85.7  
 WLC       100       100       
 AP        83        83.3 


```

The client detail shows a view of the topology for the client.  Client is connected to "SDA-Guest" ssid, then to a 3802 AP then a 3504 WLC.

```buildoutcfg
$ ./assurance.py --mac B8:27:EB:70:9F:83
https://adam-dnac:443/dna/intent/api/v1/client-detail?timestamp=&macAddress=B8:27:EB:70:9F:83
Client Detail for:00:F6:63:34:6A:C0 at 2018-10-14 12:11:29 (1539479489498)
HostType: WIRELESS connected to 3804_sda

10.11.200.23(None)[Linux-Workstation] - Health:1 ->
SSID: SDA-Guest(2.4 GHZ) ->
3804_sda:10.11.250.14:AIR-AP3802E-Z-K9(8.5.131.0) - Health:10 ->
3504:10.10.10.147:AIR-CT3504-K9(8.5.131.0) - Health:10

```
