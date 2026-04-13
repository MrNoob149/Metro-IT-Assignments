import machine
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import utime

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c) 

SW_2 = 7
SW_1 = 8
SW_0 = 9

but0 = Pin(SW_0, Pin.IN, Pin.PULL_UP)
but1 = Pin(SW_1, Pin.IN, Pin.PULL_UP)
but2 = Pin(SW_2, Pin.IN, Pin.PULL_UP)

x = 0
y = 32


while True:
    oled.pixel(x, y, 1)
    x += 1

    if but0.value() == 0:
        y += 1

        
    if but2.value() == 0:
        y -= 1

    if but1.value() == 0:
        oled.fill(0)
        x = 0
        y = 32

    if x > 127:
        x = 0

    if y < 0:
        y = 63

    if y > 63:
        y = 0
    
    
    oled.show()
