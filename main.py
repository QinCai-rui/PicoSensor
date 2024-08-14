"""
/***************************************************************
 *                                                             *
 *                    GNU GENERAL PUBLIC LICENSE               *
 *                       Version 3, 29 June 2007               *
 *                                                             *
 *  This program is free software: you can redistribute it and *
 *  or modify it under the terms of the GNU General Public     *
 *  License as published by the Free Software Foundation,      *
 *  either version 3 of the License, or (at your option) any   *
 *  later version.                                             *
 *                                                             *
 *  This program is distributed in the hope that it will be    *
 *  useful, but WITHOUT ANY WARRANTY; without even the implied *
 *  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR    *
 *  PURPOSE. See the GNU General Public License for more       *
 *  details.                                                   *
 *                                                             *
 *  You should have received a copy of the GNU General Public  *
 *  License along with this program. If not, see               *
 *  <https://www.gnu.org/licenses/>.                           *
 *                                                             *
 ***************************************************************/
"""

from machine import Pin, I2C
import ssd1306
import dht
from utime import localtime, sleep

# Initialise the Pico onboard LED
LED_onboard = Pin("LED", Pin.OUT)

# Initialise I2C for the SSD1306 OLED display
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialise the DHT22 sensor
sensor = dht.DHT22(Pin(22))

tempHist = []
humidHist = []

def calculate_mean(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)    

def main():
    while 1: 
        # Measure temperature and humidity
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()
        
        # Add current temperature and humidity to the history lists
        tempHist.append(temp)
        humidHist.append(humid)

        # Calculate average temperature and humidity
        avg_temp = calculate_mean(tempHist)
        avg_humid = calculate_mean(humidHist)

        # Get the current time
        current_time = localtime()
        time_str = "{:02}:{:02}:{:02}".format(current_time[3], current_time[4], current_time[5])

        # Clear the display
        oled.fill(0)
        
        # Display temperature, humidity, and time
        oled.text("Time: {}".format(time_str), 0, 0)
        oled.text("Temp: {:.1f}C".format(temp), 0, 10)
        oled.text("Humid: {:.1f}%".format(humid), 0, 20)
        oled.text("Avg Temp: {:.1f}C".format(avg_temp), 0, 40)
        oled.text("Avg Humid: {:.1f}%".format(avg_humid), 0, 50)
        
        # Update the display
        oled.show()
    
        # Toggle the onboard LED to show updating
        LED_onboard.value(1)
        sleep(0.2)
        LED_onboard.value(0)
    
        # Wait for 0.8 second before the next update
        sleep(0.8)
        

if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Oops... Something happened")
    except Exception as ex: 
        print(ex)
