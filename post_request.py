"""Price watcher for WizzAir flight on 16.12"""
import os
import json
import urllib.parse as urlparse
import requests
import psycopg2
from send_email import send_email

def main():
    """Main method"""
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
        port=port)
    cur = con.cursor()

    cur.execute("SELECT Price FROM Flights WHERE ID=1")
    rdr = cur.fetchall()
    current_price = float(rdr[0][0])

    url = "https://be.wizzair.com/7.0.0/Api/search/search"
    payload = {"isFlightChange":False,
               "isSeniorOrStudent":False,
               "flightList":[
                   {"departureStation":"ABZ",
                    "arrivalStation":"GDN",
                    "departureDate":"2017-12-16"}],
               "adultCount":1,
               "childCount":0,
               "infantCount":0,
               "wdc":True,
               "rescueFareCode":""}
    headers = {'content-type': 'application/json'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    json_response = json.loads(response.text)
    flights = json_response["outboundFlights"]


    admin_price = flights[0]["fares"][0]["administrationFeePrice"]["amount"]
    disc_baseprice = flights[0]["fares"][0]["discountedFarePrice"]["amount"]

    full_price = (float(admin_price) + float(disc_baseprice))

    if full_price != current_price:
        cur.execute("UPDATE Flights SET Price='"+str(full_price)+"' WHERE ID=1")
        con.commit()

        username = "kdryja"
        password = os.environ['SMS_API_KEY']
        sms_to = os.environ['DAD_NUMBER']
        message = "WizzAir Alert. Price changed ABZ to GDN. From %s GBP To %s GBP" % (str(current_price), str(full_price))
        url = "http://api.smsapi.com/sms.do?username=%s&password=%s&to=%s&message=%s" % (username, password, sms_to, message)
        requests.get(url)

        send_email("kdryja@gmail.com", str(current_price), str(full_price))

    cur.close()
    con.close()
main()
