import os

import requests
from twilio.rest import Client

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
client = Client(account_sid, auth_token)


api_key = os.environ.get("OWM_API_KEY")
latitude = 53.383
longitude = -1.4659
records_needed = 4

parameters = {
    "lat": latitude,
    "lon": longitude,
    "cnt": records_needed,
    "appid": api_key
}

# lat={lat}&lon={lon}&appid={API key}

api_response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
api_response.raise_for_status()
forecast_data = api_response.json()
print(forecast_data)
print(api_response.status_code)

#Get the list of updates from json response
time_periods = forecast_data["list"]
#Iterate through the list to check for code <700 and set rain to True
rain_forecasted = False
for period in time_periods:
    weather_records = period["weather"]
    for record in weather_records:
        print(f"Weather code {record["id"]}")
        if record["id"] < 700:
            rain_forecasted = True

if rain_forecasted:
    message_body="It's going to rain in the next 12 hours. Bring an ☂️",
else:
    message_body="No rain forecast in next 12 hours"

message = client.messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+447795387771',
        body=message_body,
    )
