from gpiozero import LED
from time import sleep

# Define Pins
lane1_green = LED(17)
lane1_red = LED(27)

def switch_lights(lane_id, duration):
    if lane_id == 1:
        print(f"Switching Lane 1 GREEN for {duration} seconds")
        lane1_red.off()
        lane1_green.on()
        sleep(duration)
        lane1_green.off()
        lane1_red.on()

# This function would be called by your AI logic
# switch_lights(1, 45)