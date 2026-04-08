# Original: https://wokwi.com/projects/354682548125570049

"""
Hardware Simulator - Encapsulated Classes
All components of the protoboard simulator organized into intuitive classes
"""

from encappedhw import *

# Usage example
if __name__ == "__main__":
    # Create simulator instance
    hw = HardwareSimulator()
    
    # Run demonstration
    hw.demo_sequence()
    
    # Wait a moment
    utime.sleep(1)
    
    # Initialize UFO position
    ufo_position = 0
    
    def update_ufo():
        global ufo_position
        if hw.buttons.is_pressed(0):
            ufo_position -= 1
        elif hw.buttons.is_pressed(2):
            ufo_position += 1
        
        # Ensure UFO stays within bounds
        if ufo_position < 0:
            ufo_position = 0
        elif ufo_position > hw.display.WIDTH - 4:  # Width of UFO is 4 characters
            ufo_position = hw.display.WIDTH - 4
        
        # Clear and redraw display
        hw.display.clear()
        hw.display.text('UFO Game', 1, 1)
        hw.display.text('<=>', ufo_position, 50)  # Draw UFO in visible area
    
    while True:
        update_ufo()
        utime.sleep(0.1)
