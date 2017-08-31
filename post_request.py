import requests
import json
import sendgrid
import os
from sendgrid.helpers.mail import *
import psycopg2
import urllib.parse as urlparse

os.environ['DATABASE_URL'] = "postgres://gynhccrrobqgsq:14e2f986d43812a19924c788be5d62e4558339cf5df1c3430d5a8b8aa77ba5a6@ec2-79-125-2-71.eu-west-1.compute.amazonaws.com:5432/dd8ted3qrtiaun"

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

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("WizzairPriceChange@konrad.com")
    to_email = Email("kdryja@gmail.com")
    subject = "WizzAir ABZ -> GDN Alert"
    message = "Changed from: " + str(currentPrice) + " GBP to: " + str(fullPrice) + " GBP."
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    to_email = Email("ddryja@wp.pl")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())


cur.close()
con.close()