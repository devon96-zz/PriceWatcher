import requests
import json

url = "https://be.wizzair.com/7.0.0/Api/search/search"
payload = {"isFlightChange":False,"isSeniorOrStudent":False,"flightList":[{"departureStation":"ABZ","arrivalStation":"GDN","departureDate":"2017-12-16"}],"adultCount":1,"childCount":0,"infantCount":0,"wdc":True,"rescueFareCode":""}
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(payload), headers=headers)

jsonResponse = json.loads(response.text)
flights = jsonResponse["outboundFlights"]

f = open("currentPrice.txt", "r+")
currentPrice = float(f.read())
f.close()

adminPrice = flights[0]["fares"][0]["administrationFeePrice"]["amount"]
discBasePrice = flights[0]["fares"][0]["discountedFarePrice"]["amount"]

fullPrice =  (float(adminPrice) + float(discBasePrice))

if fullPrice != currentPrice:
    f = open("currentPrice.txt", "w")
    f.write(str(fullPrice))
    f.close()
    print ("PRICE CHANGED")