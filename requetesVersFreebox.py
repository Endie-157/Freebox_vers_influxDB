#libraries
import requests
from requests.auth import HTTPDigestAuth
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from hashlib import sha1
import hmac

#variables influxDB
influxToken = "" #mettre votre token influxdb
org = "" #mettre le nom de votre organisation influxdb
url = "" #mettre ip:port de votre influxdb
bucket="" #mettre le nom de votre bucket

client = influxdb_client.InfluxDBClient(url=url, token=influxToken, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

#variables freebox
freeboxUrl="http://mafreebox.freebox.fr" #addresse par défaut de la freebox
rrd=freeboxUrl+"/api/v12/rrd/"
freeboxToken="" #token obtenu dans authrep.json
freeboxAppId="" #nom de l'application que vous avez noté dans authreq

#Création du mot de passe avec un challenge
rep=requests.get(freeboxUrl+"/api/v12/login/")
challenge=json.loads(rep.text)["result"]["challenge"]

passw=hmac.new(freeboxToken.encode(), challenge.encode(), "sha1")
passw=passw.hexdigest()
jpass=json.dumps({
   "app_id": freeboxAppId,
   "password": passw,
})
login=requests.post(freeboxUrl+"/api/v12/login/session/", data=jpass)
password=json.loads(login.text)["result"]["session_token"]

#Boucle de collection de data
while True:
   #Traffic entrant et sortant
   netReq={
      "date_start":time.time(),
      "date_end":time.time(),
      "db": "net",
   }

   #temperature et ventilateurs
   tempstart=time.time()-120
   tempReq={
      "date_start":tempstart,
      "db": "temp",
   }

   #Traffic switch
   switchStart=time.time()-120
   switchReq={
      "date_start":switchStart,
      "db": "switch",
   }

   #Stats router requête et envoi à influxDB
   netRep=requests.post(rrd, headers={"X-Fbx-App-Auth":password}, data=json.dumps(netReq))
   dataNet=json.loads(netRep.text)
   print(dataNet)

   intUpMax=dataNet["result"]["data"][0]["bw_up"]
   dataIntUpMax = (
      Point("internet")
      .tag("external", "upload")
      .field("internet upload max", intUpMax)
   )
   write_api.write(bucket=bucket, org=org, record=dataIntUpMax)

   intDownMax=dataNet["result"]["data"][0]["bw_down"]
   dataIntDownMax = (
      Point("internet")
      .tag("external", "download")
      .field("internet download max", intDownMax)
   )
   write_api.write(bucket=bucket, org=org, record=dataIntDownMax)

   intUp=dataNet["result"]["data"][0]["rate_up"]
   dataIntUp = (
      Point("internet")
      .tag("external", "upload")
      .field("internet upload live", intUp)
   )
   write_api.write(bucket=bucket, org=org, record=dataIntUp)

   intDown=dataNet["result"]["data"][0]["rate_down"]
   dataIntDown = (
      Point("internet")
      .tag("external", "download")
      .field("internet download live", intDown)
   )
   write_api.write(bucket=bucket, org=org, record=dataIntDown)

   #Stats température requête et envoi à influxDB
   tempRep=requests.post(rrd, headers={"X-Fbx-App-Auth":password}, data=json.dumps(tempReq))
   dataTemp=json.loads(tempRep.text)
   print(dataTemp)

   tempCpub=dataTemp["result"]["data"][0]["temp_cpub"]
   dataTempCpub = (
      Point("temperature")
      .tag("temperature", "CPU")
      .field("Temperature CPUb", tempCpub)
   )
   write_api.write(bucket=bucket, org=org, record=dataTempCpub)
   
   tempCpum=dataTemp["result"]["data"][0]["temp_cpum"]
   dataTempCpum = (
      Point("temperature")
      .tag("temperature", "CPU")
      .field("Temperature CPUm", tempCpum)
   )
   write_api.write(bucket=bucket, org=org, record=dataTempCpum)

   tempSw=dataTemp["result"]["data"][0]["temp_sw"]
   dataTempSw = (
      Point("temperature")
      .tag("temperature", "SW")
      .field("Temperature switch", tempSw)
   )
   write_api.write(bucket=bucket, org=org, record=dataTempSw)

   tempHdd=dataTemp["result"]["data"][0]["temp_hdd"]
   dataTempHdd = (
      Point("temperature")
      .tag("temperature", "HDD")
      .field("Temperature Storage Drive", tempHdd)
   )
   write_api.write(bucket=bucket, org=org, record=dataTempHdd)

   tempFan=dataTemp["result"]["data"][0]["fan0_speed"]
   dataTempFan = (
      Point("temperature")
      .tag("fan speed", "fan")
      .field("Fan Speed", tempFan)
   )
   write_api.write(bucket=bucket, org=org, record=dataTempFan)

   #Stats switch requête et envoi à influxDB
   switchRep=requests.post(rrd, headers={"X-Fbx-App-Auth":password}, data=json.dumps(switchReq))
   dataSwitch=json.loads(switchRep.text)
   print(dataSwitch)

   rx1=dataSwitch["result"]["data"][0]["rx_1"]
   dataRx1 = (
      Point("Switch")
      .tag("switch port 1", "download")
      .field("Switch port 1 download", rx1)
   )
   write_api.write(bucket=bucket, org=org, record=dataRx1)

   tx1=dataSwitch["result"]["data"][0]["tx_1"]
   dataTx1 = (
      Point("Switch")
      .tag("switch port 1", "upload")
      .field("Switch port 1 upload", tx1)
   )
   write_api.write(bucket=bucket, org=org, record=dataTx1)

   rx2=dataSwitch["result"]["data"][0]["rx_2"]
   dataRx2 = (
      Point("Switch")
      .tag("switch port 2", "download")
      .field("Switch port 2 download", rx2)
   )
   write_api.write(bucket=bucket, org=org, record=dataRx2)

   tx2=dataSwitch["result"]["data"][0]["tx_2"]
   dataTx2 = (
      Point("Switch")
      .tag("switch port 2", "upload")
      .field("Switch port 2 upload", tx2)
   )
   write_api.write(bucket=bucket, org=org, record=dataTx2)

   rx3=dataSwitch["result"]["data"][0]["rx_3"]
   dataRx3 = (
      Point("Switch")
      .tag("switch port 3", "download")
      .field("Switch port 3 download", rx3)
   )
   write_api.write(bucket=bucket, org=org, record=dataRx3)

   tx3=dataSwitch["result"]["data"][0]["tx_3"]
   dataTx3 = (
      Point("Switch")
      .tag("switch port 3", "upload")
      .field("Switch port 3 upload", tx3)
   )
   write_api.write(bucket=bucket, org=org, record=dataTx3)

   rx4=dataSwitch["result"]["data"][0]["rx_4"]
   dataRx4 = (
      Point("Switch")
      .tag("switch port 4", "download")
      .field("Switch port 4 download", rx4)
   )
   write_api.write(bucket=bucket, org=org, record=dataRx4)

   tx4=dataSwitch["result"]["data"][0]["tx_4"]
   dataTx4 = (
      Point("Switch")
      .tag("switch port 4", "upload")
      .field("Switch port 4 upload", tx4)
   )
   write_api.write(bucket=bucket, org=org, record=dataTx4)

   #pause entre les requêtes
   time.sleep(5)
