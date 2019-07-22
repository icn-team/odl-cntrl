# odl-cntrl
This is the Dockerfile to build the controler (management) of odl. In this docker you can configure the vSwitches through 
OpenDaylight. The communication between odl-cntrl and odl is through REST API. You can find the configuration in config.xml 
file including (mounting, adding face, adding punt, adding route). 
The odl.py allows the user to add face, punt, and route to the remote switch. Moreover, it allows to receive telemetry. 
The config file includes multiple tags (i.e., face, punt, route). 
Each tag allows to have the configuration of multiple remote switches. Please, follow the following steps:
* Run opendaylight 
* run the odl.py script to push the configuration
    *  cd /hicn/cntrl/ && ./odl.py -act add
    *  ./odl.py -act [face|punt|route|telem] -odl [odl IP address] -influx [Influxdb IP address]
 
Please note that [-act telem] is a blocking execution to receive telemetry 
