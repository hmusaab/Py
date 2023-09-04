import schedule
import time
import datetime as dt
import requests
from twilio.rest import Client





def get_weather(Latitude, Longitude):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude={Latitude}&longitude={Longitude}&hourly=temperature_2m,relativehumidity_2m,windspeed_180m"
    response = requests.get(base_url)
    data = response.json
    return data
def celsius_to_fahrenheit(celsius):
    return(celsius * 9/5) + 32  #helper function

def send_a_text_message(Body):
    account_sid = "AC6d138c5f196062bf72a0ebe33e45f890"
    auth_token = "199bb331e292aca89155f3d1e629214d"
    from_phone_number = "+18773815389"
    to_phone_number = "+3133981074"

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=Body,
        from_=from_phone_number,
        to_=to_phone_number
    )
    print("Text Message SENT!!")


def SendWeatherUpdate():
    #hard coded latitude and longitude for Michigan, Warren
    Latitude = 42.4904
    Longitude = -83.013

    weatherData = get_weather(Latitude, Longitude)
    temperature_for_celsius = weatherData["hourly"]["temperature_2m"][0]
    relativehumidity = weatherData["hourly"]["relativehumidity_2m"][1]
    windspeed = weatherData["hourly"]["windspeed_180m"][0]
    temperature_for_fahrenheit = celsius_to_fahrenheit(temperature_for_celsius)

    WeatherInfo = (
        f"Good Morning Musaab!\n"
        f"Current Weather In Warren, Michigan is:\n"
        f"Temperature: {temperature_for_fahrenheit:.2f}°F\n"
        f"Relative Humidity: {relativehumidity}%\n"
        f"WindSpeed: {windspeed} m/s"
    )
    send_a_text_message(WeatherInfo)




def main():
    schedule.every().day.at("06:00").do(SendWeatherUpdate)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main() 
