
# Demo program for the I2C 16x2 Display 
# Created by IZ0FIU Max 

# Import necessary libraries for communication and display use
import lcddriver
import time
from datetime import datetime
import sys
import Adafruit_DHT
import requests
from time import sleep

humidity_I, temperature_I = Adafruit_DHT.read_retry(11, 4)  #my GPIO input is 4
humidity_E, temperature_E = Adafruit_DHT.read_retry(11, 17) #my GPIO input is 17

display = lcddriver.lcd()

cities = [('Formia', '41.25', '13.60', 'Europe/Rome'),
          ('New York', '40.71', '-74.01', 'America/New_York'),
          ('Tokyo', '35.68', '139.64', 'Asia/Tokyo')]

def getWeatherConditions(lat, lon):
    """Get weather data from FCC weather API.

    Args:
        lat (string): Latitude
        lon (string): Longitude
    """

# Main body of code
    try:
        url = 'https://fcc-weather-api.glitch.me/api/current'
        # encode query string for request
        query_strings = {'lon': lon, 'lat': lat}
        # headers to disable caching (in theory)
        headers = {'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
        while True:
            # get weather data from Free Code Camp Weather API
            r = requests.get(url,
                             params=query_strings,
                             headers=headers,
                             timeout=30)
            data = r.json()
            status_code = r.status_code
            r.close()
            # If data is unavailble city will equal Shuzenji
            if data['name'] != 'Shuzenji':
                break
            print('data unavailable...')
            sleep(3)
        # return data formatted to JSON
        return data, status_code
    except requests.exceptions.Timeout:
        return "Timeout", 408
    except requests.exceptions.ConnectionError:
        return "Connection Error", 404
    except Exception:
        e = sys.exc_info()[0]
        print("Error: {0}".format(e))
        return "Undefined Error", 0

if __name__ == "__main__":

    while 1:
        # Remember that your sentences can only be 16 characters long!
        now = datetime.now()
        date_time = now.strftime("%d/%m %a,%H:%M")
        display.lcd_display_string("     IZ0FIU", 1) # Write line of text to first line of display, change wit your call or your name
        display.lcd_display_string(date_time , 2) # Write line of text to second line of display
        time.sleep(30)                                     # Give time for the message to be read
        display.lcd_display_string("Ti:{:.1f} Hi:{}%".format(temperature_I, humidity_I), 2)
        time.sleep(10)
        display.lcd_display_string("Te:{:.1f} He:{}%".format(temperature_E, humidity_E), 2)
        time.sleep(10)
        display.lcd_clear()
        for city in cities:
            data, code = getWeatherConditions(city[1], city[2])
            if code != 200:
                # Status Code Error
                print (data)
                if not isinstance(data, str):
                    data = "Unknown"
#                lcd.clear()
                print("ERROR {0}\n{1}".format(code, data))
                sleep(4)
            elif not isinstance(data, dict) or "error" in data:
                # Feed Error
                print (data)
#                lcd.clear()
                print("FEED\nERROR")
                sleep(4)
            else:
                # Retrieve city name, condition and temperature
                cond = data['weather'][0]['description']
                temp = data['main']['temp']
#                lcd.clear()
                # Display city temperature and condition
                display.lcd_display_string(city[0] + ' {0:.1f}C'.format(temp), 1)
#                print(223, True)
                display.lcd_display_string((cond), 2)
                sleep(10)
                display.lcd_clear()


