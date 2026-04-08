from encappedhw import *

# Create hardware object
hw = HardwareSimulator()

# LEDs
hw.leds.on(0)           # Turn on LED0
hw.leds.off(1)          # Turn off LED1
hw.leds.toggle(2)       # Toggle LED2
hw.leds.all_on()        # All LEDs on
hw.leds.blink(3, 0.5)   # Blink LED3 for 0.5s

# Buttons
hw.buttons.set_callback(0, my_function)  # Set callback for button 0
hw.buttons.is_pressed(1)                  # Check if button 1 is pressed

# Rotary Knob
hw.knob.set_rotation_callback(my_rotate_func)
hw.knob.set_switch_callback(my_press_func)
value = hw.knob.get_counter()
hw.knob.reset_counter()

# Display
hw.display.clear()
hw.display.text("Hello", 10, 20)
hw.display.show_info(["Line1", "Line2"])
hw.display.highlight_rectangle()

# Heart Rate Sensor
raw = hw.heart_rate.read_raw()
voltage = hw.heart_rate.read_voltage()
percent = hw.heart_rate.read_percentage()