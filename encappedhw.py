import machine
from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
import utime


class LEDs:
    """Controls all LEDs on the protoboard"""
    
    # Pin mappings (class constants)
    D0_PIN = 25  # Pico's internal LED
    D1_PIN = 22  # Protoboard's LED1
    D2_PIN = 21  # Protoboard's LED2
    D3_PIN = 20  # Protoboard's LED3
    
    def __init__(self):
        """Initialize all LEDs"""
        self.led0 = Pin(self.D0_PIN, Pin.OUT)
        self.led1 = Pin(self.D1_PIN, Pin.OUT)
        self.led2 = Pin(self.D2_PIN, Pin.OUT)
        self.led3 = Pin(self.D3_PIN, Pin.OUT)
        self.all_leds = [self.led0, self.led1, self.led2, self.led3]
    
    def on(self, led_number):
        """Turn on specific LED (0-3)"""
        self.all_leds[led_number].value(1)
    
    def off(self, led_number):
        """Turn off specific LED (0-3)"""
        self.all_leds[led_number].value(0)
    
    def toggle(self, led_number):
        """Toggle specific LED (0-3)"""
        self.all_leds[led_number].toggle()
    
    def all_on(self):
        """Turn on all LEDs"""
        for led in self.all_leds:
            led.value(1)
    
    def all_off(self):
        """Turn off all LEDs"""
        for led in self.all_leds:
            led.value(0)
    
    def blink(self, led_number, duration=0.5):
        """Blink specific LED for given duration"""
        self.toggle(led_number)
        utime.sleep(duration)
        self.toggle(led_number)


class MicroButtons:
    """Controls the three microbuttons with interrupt handlers"""
    
    # Pin mappings
    SW0_PIN = 9
    SW1_PIN = 8
    SW2_PIN = 7
    
    def __init__(self):
        """Initialize microbuttons with pull-up resistors"""
        self.button0 = Pin(self.SW0_PIN, Pin.IN, Pin.PULL_UP)
        self.button1 = Pin(self.SW1_PIN, Pin.IN, Pin.PULL_UP)
        self.button2 = Pin(self.SW2_PIN, Pin.IN, Pin.PULL_UP)
        
        # Store callbacks
        self.callbacks = [None, None, None]
    
    def set_callback(self, button_number, callback_function):
        """Set callback for button press (0, 1, or 2)"""
        self.callbacks[button_number] = callback_function
        
        # Assign to appropriate button
        if button_number == 0:
            self.button0.irq(self._handler0, Pin.IRQ_FALLING)
        elif button_number == 1:
            self.button1.irq(self._handler1, Pin.IRQ_FALLING)
        elif button_number == 2:
            self.button2.irq(self._handler2, Pin.IRQ_FALLING)
    
    def _handler0(self, pin):
        """Internal handler for button 0"""
        if self.callbacks[0]:
            self.callbacks[0]()
    
    def _handler1(self, pin):
        """Internal handler for button 1"""
        if self.callbacks[1]:
            self.callbacks[1]()
    
    def _handler2(self, pin):
        """Internal handler for button 2"""
        if self.callbacks[2]:
            self.callbacks[2]()
    
    def is_pressed(self, button_number):
        """Check if button is currently pressed"""
        buttons = [self.button0, self.button1, self.button2]
        return buttons[button_number].value() == 0


class RotaryKnob:
    """Controls the rotary encoder with push button"""
    
    LEFT_PIN = 10
    RIGHT_PIN = 11
    SWITCH_PIN = 12
    
    def __init__(self):
        """Initialize rotary encoder"""
        self.pin_left = Pin(self.LEFT_PIN, Pin.IN)
        self.pin_right = Pin(self.RIGHT_PIN, Pin.IN)
        self.pin_switch = Pin(self.SWITCH_PIN, Pin.IN, Pin.PULL_UP)
        
        self.counter = 0
        self.rotation_callback = None
        self.switch_callback = None
        
        # Set up interrupts
        self.pin_left.irq(self._handle_rotation, Pin.IRQ_FALLING)
        self.pin_switch.irq(self._handle_switch, Pin.IRQ_FALLING)
    
    def _handle_rotation(self, pin):
        """Handle rotation events"""
        if self.pin_right.value() == 1:
            self.counter += 1
            if self.rotation_callback:
                self.rotation_callback(self.counter, "clockwise")
        else:
            self.counter -= 1
            if self.rotation_callback:
                self.rotation_callback(self.counter, "counter-clockwise")
    
    def _handle_switch(self, pin):
        """Handle button press events"""
        self.counter = 0
        if self.switch_callback:
            self.switch_callback()
    
    def set_rotation_callback(self, callback):
        """Set function to call on rotation"""
        self.rotation_callback = callback
    
    def set_switch_callback(self, callback):
        """Set function to call when knob is pressed"""
        self.switch_callback = callback
    
    def get_counter(self):
        """Get current counter value"""
        return self.counter
    
    def reset_counter(self):
        """Reset counter to zero"""
        self.counter = 0


class OLED_Display:
    """Controls the 128x64 OLED display"""
    
    WIDTH = 128
    HEIGHT = 64
    SDA_PIN = 14
    SCL_PIN = 15
    
    def __init__(self):
        """Initialize OLED display"""
        i2c = I2C(1, scl=Pin(self.SCL_PIN), sda=Pin(self.SDA_PIN), freq=400000)
        self.display = SSD1306_I2C(self.WIDTH, self.HEIGHT, i2c)
    
    def clear(self):
        """Clear the display"""
        self.display.fill(0)
        self.display.show()
    
    def fill(self):
        """Fill the display with light"""
        self.display.fill(1)
        self.display.show()
    
    def text(self, message, x=1, y=1):
        """Write text at specified position"""
        self.display.text(message, x, y)
        self.display.show()
    
    def rect(self, x, y, width, height, border=1):
        """Draw rectangle"""
        self.display.rect(x, y, width, height, border)
        self.display.show()
    
    def show_info(self, info_list):
        """Show multiple lines of text"""
        self.clear()
        y_position = 1
        for line in info_list:
            self.display.text(str(line), 1, y_position)
            y_position += 10
        self.display.show()
    
    def highlight_rectangle(self, x=0, y=41, width=128, height=23):
        """Draw double rectangle for highlighting"""
        self.rect(x, y, width, height, 2)
        self.rect(x, y+1, width, height-2, 2)


class HeartRateSensor:
    """Controls the heart rate sensor (simulated)"""
    
    A0_PIN = 26
    
    def __init__(self):
        """Initialize ADC for heart rate sensor"""
        self.sensor = ADC(Pin(self.A0_PIN))
    
    def read_raw(self):
        """Read raw analog value (0-65535)"""
        return self.sensor.read_u16()
    
    def read_voltage(self):
        """Read voltage value (0-3.3V)"""
        return self.sensor.read_u16() * (3.3 / 65535)
    
    def read_percentage(self):
        """Read as percentage (0-100%)"""
        return (self.sensor.read_u16() / 65535) * 100


class HardwareSimulator:
    """Main simulator class that combines all components"""
    
    def __init__(self):
        """Initialize all hardware components"""
        self.leds = LEDs()
        self.buttons = MicroButtons()
        self.knob = RotaryKnob()
        self.display = OLED_Display()
        self.heart_rate = HeartRateSensor()
    
    def demo_sequence(self):
        """Run a demonstration sequence"""
        # Test LEDs
        print("Testing LEDs...")
        self.leds.all_on()
        utime.sleep(1)
        self.leds.all_off()
        
        # Test display
        print("Testing display...")
        self.display.fill()
        utime.sleep(1)
        self.display.clear()
        
        # Setup button callbacks example
        def on_button0():
            print("Button 0 pressed - Toggling LED1")
            self.leds.toggle(1)
        
        def on_button1():
            print("Button 1 pressed - Toggling LED2")
            self.leds.toggle(2)
        
        def on_button2():
            print("Button 2 pressed - Toggling LED3")
            self.leds.toggle(3)
        
        self.buttons.set_callback(0, on_button0)
        self.buttons.set_callback(1, on_button1)
        self.buttons.set_callback(2, on_button2)
        
        # Setup knob callbacks
        def on_rotate(value, direction):
            print(f"Knob rotated {direction}: {value}")
            self.display.clear()
            self.display.text(f"Counter: {value}")
        
        def on_knob_press():
            print("Knob pressed - Counter reset")
            self.display.clear()
            self.display.text("Counter reset!")
        
        self.knob.set_rotation_callback(on_rotate)
        self.knob.set_switch_callback(on_knob_press)
    
    def run_info_loop(self):
        """Run main info display loop"""
        while True:
            # Display project info
            info_lines = [
                'Hardware project',
                'School of ICT',
                'Metropolia UAS',
                '18.3.2024',
                f'Knob: {self.knob.get_counter()}'
            ]
            self.display.show_info(info_lines)
            self.display.highlight_rectangle()
            
            utime.sleep(2)
            self.display.clear()
            
            # Blink internal LED
            self.leds.blink(0, 0.5)
