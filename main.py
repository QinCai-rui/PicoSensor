from machine import Pin, I2C
import ssd1306
import dht
import utime
import statistics

# Initialize I2C for the SSD1306 OLED display
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize the DHT22 sensor
sensor = dht.DHT22(Pin(22))

tempHist = []
humidHist = []

while True:
    try:
        # Measure temperature and humidity
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()
        
        # Add current temperature and humidity to the history lists
        tempHist.append(temp)
        humidHist.append(humid)

        # Calculate average temperature and humidity
        avg_temp = statistics.mean(tempHist)
        avg_humid = statistics.mean(humidHist)

        # Get the current time
        current_time = utime.localtime()
        time_str = "{:02}:{:02}:{:02}".format(current_time[3], current_time[4], current_time[5])
        
        # Clear the display
        oled.fill(0)
        
        # Display temperature, humidity, and time
        oled.text("Temp: {:.1f}C".format(temp), 0, 0)
        oled.text("Humid: {:.1f}%".format(humid), 0, 10)
        oled.text("Time: {}".format(time_str), 0, 20)
        oled.text("Avg. Temp: {:.1f}C".format(avg_temp), 0, 30)
        oled.text("Avg. Humid: {:.1f}%".format(avg_humid), 0, 40)
        
        # Update the display
        oled.show()
        
        # Wait for 1 second before the next update
        utime.sleep(1)
        
    except OSError as e:
        print("Oops... Something happened")
