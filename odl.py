#!/usr/bin/python
import socket
import requests
import datetime
import time
import argparse
import sys
import xml.etree.ElementTree as ET
from influxdb import InfluxDBClient
from time import sleep

# Parsing argument
parser = argparse.ArgumentParser(description='Mounting nodes to ODL')
parser.add_argument('-act', action="store",  dest='act',
                    help='Indicate your operation')
parser.add_argument('-odl', action="store",  dest='odl'
                    )

parser.add_argument('-influx', action="store",  dest='influx'
                    )
results = parser.parse_args()

# acceptable response code
SUCCESS = [200,201,202]

# Mount point names
nodes = ['sc','sl']

# Action functions [mounting, facing, punting, routing, telemetering]
def mounting():
 for node in nodes:
   response= None
   url = 'http://'+str(results.odl)+':8181/restconf/config/network-topology:network-topology/topology/topology-netconf/node/'+str(node)
   print(url)
   exit
   tree = ET.parse('tnode.xml')
   root = tree.getroot()
   for elem in root:
      if(elem.tag=='{urn:TBD:params:xml:ns:yang:network-topology}node-id'):
         elem.text=str(node)
      if(elem.tag=='{urn:opendaylight:netconf-node-topology}schema-cache-directory'):
         elem.text=str(node)
      if(elem.tag=='{urn:opendaylight:netconf-node-topology}host'):
         elem.text="172.17.0.4"
   tree.write('node.xml')
   filename='node.xml'
   headers = {'content-type': 'application/xml','accept':'application/xml'}
   if str(results.act)=='del':
     response = requests.delete(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
   elif str(results.act)=='add':
     response = requests.put(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
   if response==None:
     print('usage: mount.py -del/add')
     break
   elif response.status_code in SUCCESS:
     if str(results.act)=='del':
       exit
     print(response.text)
     sleep(0.1)
   else:
     print('operation failed'+str(node)+str(response))



def facing():
# hicn add face API parameters
  lip6=0
  rip6=0
  swif=0
  for node in nodes:
      response=None
      url=None
      tree = ET.parse('config.xml')
      root = tree.getroot()
      for faces in root:
         if faces.tag=='faces':
           for face in faces:
             for elem in face:
                 if elem.tag=='lip6':
                     lip6=face.text
                 if elem.tag=='rip6':
                     rip6=face.text
                 if elem.tag=='swif':
                     swif=face.text
             url = 'http://'+str(results.odl)+':8181/restconf/operations/network-topology:network-topology/topology/topology-netconf/node/'+str(node)+'/yang-ext:mount/hicn:face-ip-add'
             headers = {'content-type': 'application/xml','accept':'application/xml'}

             xtop = ET.Element('input')
             xtop.attrib["xmlns"]="urn:sysrepo:hicn"
             xroute = 'lip6'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(lip6)

             xroute = 'lip4'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text='-1'

             xroute = 'rip6'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(rip6)

             xroute = 'rip4'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text='-1'


             xroute = 'swif'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(swif)

             final = ET.ElementTree(xtop)
             final.write('face.xml')
             filename='face.xml'
             response = requests.post(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
             if response.status_code in SUCCESS:
                 sleep(0.1)
             else:
                 print('operation failed'+str(node)+response.text)


def punting():
# hicn add punt API parameters
  ip6=0
  lent=0
  swif=0
  for node in nodes:
      response=None
      url=None
      tree = ET.parse('config.xml')
      root = tree.getroot()
      for puntes in root:
         if puntes.tag=='puntes':
          for punt in puntes:
             for elem in punt:
                 if elem.tag=='ip6':
                     ip6=elem.text
                 if elem.tag=='len':
                     lent=elem.text
                 if elem.tag=='swif':
                     swif=elem.text
             url = 'http://'+str(results.odl)+':8181/restconf/operations/network-topology:network-topology/topology/topology-netconf/node/'+str(node)+'/yang-ext:mount/hicn:punting-add'
             headers = {'content-type': 'application/xml','accept':'application/xml'}
        
             xtop = ET.Element('input')
             xtop.attrib["xmlns"]="urn:sysrepo:hicn"
             xroute = 'ip6'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(ip6)

             xroute = 'ip4'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text='-1'

             xroute = 'len'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(lent)

             xroute = 'swif'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(swif)

             final = ET.ElementTree(xtop)
             final.write('punt.xml')
             filename='punt.xml'

             response = requests.post(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
             if response.status_code in SUCCESS:
                   sleep(0.1)
             else:
                   print('operation failed'+str(node)+response.text)


def routing():
# hicn add route API parameters
 prefix=0
 lent=0
 faceid=0
 face_list = ['face_ids1','face_ids2','face_ids3','face_ids4','face_ids5','face_ids6']
 for node in nodes:
      response=None
      url=None
      tree = ET.parse('config.xml')
      root = tree.getroot()
      for routes in root:
         if routes.tag=='routes':
           for route in routes:
             for elem in route:
                 if elem.tag=='prefix':
                     prefix=elem.text
                 if elem.tag=='len':
                     lent=elem.text
                 if elem.tag=='faceid':
                     faceid=elem.text
             url = 'http://'+str(results.odl)+':8181/restconf/operations/network-topology:network-topology/topology/topology-netconf/node/'+str(node)+'/yang-ext:mount/hicn:route-nhops-add'
             headers = {'content-type': 'application/xml','accept':'application/xml'}


             xtop = ET.Element('input')
             xtop.attrib["xmlns"]="urn:sysrepo:hicn"
             xroute = 'ip6'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(prefix)

             xroute = 'ip4'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text='-1'

             xroute = 'len'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(lent)


             xroute = 'face_ids0'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text=str(faceid)

             for fl in face_list:
                xroute = fl
                nnode = ET.SubElement(xtop,xroute)
                nnode.text='0'

             xroute = 'n_faces'
             nnode = ET.SubElement(xtop,xroute)
             nnode.text='1'

             final = ET.ElementTree(xtop)
             final.write('route.xml')
             filename='route.xml'


             response = requests.post(url, auth=('admin', 'admin'),data=open(filename).read(),headers=headers)
             if response.status_code in SUCCESS:
                   sleep(0.1)
             else:
                   print('operation failed'+str(node)+response.text)


def telemetering():
# Parameters for computing the telemetry
 TX=0
 RX=1
 itx=0
 irx=0
 drx=0
 dtx=0
 faceid=0
 flag=0

 link={'sc-sl':(0,0),'sc-cc':(0,0),'sl-cl1':(0,0),'sl-cl2':(0,0)}
 old={'sc-sl':(0,0),'sc-cc':(0,0),'sl-cl1':(0,0),'sl-cl2':(0,0)}

# Set up a client for InfluxDB
if str(results.influx)!='':
 print('Please indicate the influxdb IP address')
else:
 dbclient = InfluxDBClient(str(results.influx), 8086, 'admin', 'masmas', 'demo_clus')

 while True:
   for node in nodes:
      response=None
      url=None
      url = 'http://'+str(results.odl)+':8181/restconf/operational/network-topology:network-topology/topology/topology-netconf/node/'+str(node)+'/yang-ext:mount'
      headers = {'content-type': 'application/xml','accept':'application/xml'}
      response = requests.get(url, auth=('admin', 'admin'),headers=headers)
      if response.status_code in SUCCESS:
         receiveTime=datetime.datetime.utcnow()
         root = ET.fromstring(response.text)
         for hicn in root.findall("./{urn:sysrepo:hicn}hicn-state"):
            for faces in hicn.findall('{urn:sysrepo:hicn}faces'):
               for face in faces:
                  for elem in face:
                     if elem.tag=='{urn:sysrepo:hicn}faceid':
                           faceid=int(elem.text)
                     if elem.tag=='{urn:sysrepo:hicn}drx_bytes':
                           drx=int(elem.text)
                     if elem.tag=='{urn:sysrepo:hicn}dtx_bytes':
                           dtx=int(elem.text)
                     if elem.tag=='{urn:sysrepo:hicn}irx_bytes':
                           irx=int(elem.text)
                     if elem.tag=='{urn:sysrepo:hicn}itx_bytes':
                           itx=int(elem.text)

                  if node=='sc' and faceid==0:
                     link['sc-sl']=((dtx+itx)-old['sc-sl'][TX],(drx+irx)-old['sc-sl'][RX])
                     old['sc-sl']=((dtx+itx),(drx+irx))
                     val=(link['sc-sl'][TX]+link['sc-sl'][RX])*8
                     label='sc-sl'
                     flag=1

                  if node=='sc' and faceid==1:
                     link['sc-cc']=((dtx+itx)-old['sc-cc'][TX],(drx+irx)-old['sc-cc'][RX])
                     old['sc-cc']=((dtx+itx),(drx+irx))
                     val=(link['sc-cc'][TX]+link['sc-cc'][RX])*8
                     label='sc-cc'
                     flag=1

                  if node=='sl' and faceid==0:
                     link['sl-cl1']=((dtx+itx)-old['sl-cl1'][TX],(drx+irx)-old['sl-cl1'][RX])
                     old['sl-cl1']=((dtx+itx),(drx+irx))
                     val=(link['sl-cl1'][TX]+link['sl-cl1'][RX])*8
                     label='sl-cl1'
                     flag=1

                  if node=='sl' and faceid==1:
                     link['sl-cl2']=((dtx+itx)-old['sl-cl2'][TX],(drx+irx)-old['sl-cl2'][RX])
                     old['sl-cl2']=((dtx+itx),(drx+irx))
                     val=(link['sl-cl2'][TX]+link['sl-cl2'][RX])*8
                     label='sl-cl2'
                     flag=1


                  if flag==1:
                     json_body = [
                            {
                                "measurement": label,
                                "time": receiveTime,
                                "fields": {
                                    "value": val
                                }
                            }
                     ]

                     try:
                        dbclient.write_points(json_body)
                        print("Finished writing to InfluxDB "+str(label))
                        flag=0
                     except Exception:
                        print("<<<<<Error writing to InfluxDB>>>>")
                        flag=0
      else:
         print('Error connecting to node: '+str(node)+str(response.status_code))

   time.sleep(1)

# Parsing actions

print('Applying configuration')

# Mounting node to odl
if str(results.act)=='add' or str(results.act)=='del':
 mounting()

# Adding face to the remote node
elif str(results.act)=='face':
 facing()

# Adding punt to the remote node
elif str(results.act)=='punt':
 punting()

# Adding route to the remote node
elif str(results.act)=='route':
 routing()

# telemetrying from the remote node
elif str(results.act)=='telem':
 telemetering()

else:
 print('Usage -act [face|punt|route|add|del|telem]  -odl [odl IP address] -influx [IP address]')
