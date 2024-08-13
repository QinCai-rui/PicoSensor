from machine import Pin, I2C
import ssd1306
import dht
import utime # Apparently you can't use the time library

""" This is a version that works right now but doesn't have all features """

# Initialize I2C for the SSD1306 OLED display
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize the DHT22 sensor
sensor = dht.DHT22(Pin(22))


while True:
    try:
        # Measure temperature and humidity
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()
        
        # Get the current time
        current_time = utime.localtime()
        time_str = "{:02}:{:02}:{:02}".format(current_time[3], current_time[4], current_time[5])
        
        # Clear the display
        oled.fill(0)
        
        # Display temperature, humidity, and time
        oled.text("Temp: {:.1f}C".format(temp), 0, 0)
        oled.text("Humid: {:.1f}%".format(humid), 0, 10)
        oled.text("Time: {}".format(time_str), 0, 20)
        
        # Update the display
        oled.show()
        
        # Wait for 1 second before the next update
        utime.sleep(1)
        
    except OSError as e:
        print('Oops! Something went wrong...')
    except Exceptions as exc:
        print('Hmm... Something unexpected happened.')
        print(exc)
