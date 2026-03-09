# this script runs on boot, and controls when the pi turns on or off and which program to run based on second switch input
import subprocess
from gpiozero import Button
from signal import pause


#this wont matter on ur computer since itll only really be used in the pi
prog1=["python3", "/home/pi/piggy/objectDETmotor.py" ]
prog2=["python3", "/home/pi/piggy/sensors_pi.py" ]

toggle_switch=Button(17)
current_process= None

def programRun():
    global current_process
    if current_process:
        current_process.terminate()
        current_process.wait()
    
    if toggle_switch.is_pressed:
        current_process = subprocess.Popen(prog1)
    else:
        current_process = subprocess.Popen(prog2)

toggle_switch.when_pressed = programRun
toggle_switch.when_released = programRun

programRun()
pause()

