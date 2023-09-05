import schedule
import time
import requests
from pushbullet import PushBullet  
from pywebio.input import *  
from pywebio.output import *  
from pywebio.session import *  

def get_weather(Latitude, Longitude):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude={Latitude}&longitude={Longitude}&hourly=temperature_2m,relativehumidity_2m,windspeed_180m"
    response = requests.get(base_url)
    data = response.json()
    return data

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def send_a_text_message(Body):
    access_token = "o.r7iQu3DdWRWREXLmlP78Ub8JPZ7RZj58"
    pb = PushBullet(access_token)
    push = pb.push_note("The Weather Update fool",Body)

    #make sure the push was successful
    if push["active"]:
        print("Weather Update was sent successfully")
    else:
        print("Weather Update fail to sent")


    

def SendWeatherUpdate():
    # Hard-coded latitude and longitude for Michigan, Warren
    Latitude = 42.4904
    Longitude = -83.013

    weatherData = get_weather(Latitude, Longitude)
    temperature_for_celsius = weatherData["hourly"]["temperature_2m"][0]
    relativehumidity = weatherData["hourly"]["relativehumidity_2m"][0]
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
    schedule.every().day.at("10:00").do(SendWeatherUpdate)
    while True:
        schedule.run_pending()
        time.sleep(1)

    

if __name__ == "__main__":
    main()
