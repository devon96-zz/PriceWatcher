import requests
import json
import sendgrid
import os
from sendgrid.helpers.mail import *
import psycopg2
import urllib.parse as urlparse

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
cur = con.cursor()

cur.execute("SELECT Price FROM Flights WHERE ID=1")
rdr = cur.fetchall()
currentPrice = float(rdr[0][0])

url = "https://be.wizzair.com/7.0.0/Api/search/search"
payload = {"isFlightChange":False,"isSeniorOrStudent":False,"flightList":[{"departureStation":"ABZ","arrivalStation":"GDN","departureDate":"2017-12-16"}],"adultCount":1,"childCount":0,"infantCount":0,"wdc":True,"rescueFareCode":""}
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)

jsonResponse = json.loads(response.text)
flights = jsonResponse["outboundFlights"]


adminPrice = flights[0]["fares"][0]["administrationFeePrice"]["amount"]
discBasePrice = flights[0]["fares"][0]["discountedFarePrice"]["amount"]

fullPrice =  (float(adminPrice) + float(discBasePrice))

if fullPrice != currentPrice:
    cur.execute("UPDATE Flights SET Price='"+str(fullPrice)+"' WHERE ID=1")
    con.commit()

    username = "kdryja"
    password = os.environ['SMS_API_KEY']
    smsTo = os.environ['DAD_NUMBER']
    message = "WizzAir Alert. Price changed ABZ to GDN. From %s GBP To %s GBP" % (str(currentPrice), str(fullPrice))
    url = "http://api.smsapi.com/sms.do?username=%s&password=%s&to=%s&message=%s" % (username, password, smsTo, message)
    r = requests.get(url)


cur.close()
con.close()