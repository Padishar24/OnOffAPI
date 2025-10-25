from rpi_hardware_pwm import HardwarePWM
import logging
import os
from simple_pid import PID
import time
import threading

# prepare the PWM
pwm = HardwarePWM(pwm_channel=0, hz=60, chip=0)
pwm.change_frequency(25_000)

fan_speed = 50.
pwm.start(int(fan_speed))

def getFanSpeed() -> float:
    global fan_speed
    return fan_speed

def setFanSpeed(speedPerc) -> None:
    global fan_speed
    fan_speed = float(speedPerc)
    pwm.change_duty_cycle(int(fan_speed))

# Get CPU's temperature
def getCpuTemperature() -> float:
    res = os.popen('cat /sys/devices/virtual/thermal/thermal_zone0/temp').readline()
    return (float(res)/1000)

def fan_control():
    #   tuning uses negative values to increase fan speed when temperature is too high and vice versa
    #   current settings use Proprortional, Integral, but no Derivative gain of PID controller
    pid = PID(-1.0, -0.1, 0, setpoint=50.)
    pid.output_limits = (20, 100) # limit pwm2 to valid / proofen values
   
    #   run the loop setting a fan speed and reacting on temperature changes
    temperature = getCpuTemperature()
    loop_seconds = 5
    cooling_is_on = True

    while True:
        #   memorize start time to make every loop the same duration
        start_time = time.time()
        
        if cooling_is_on:

            # check if it can be safely turned off
            if temperature < 45:
                print ('Cooling is off')
                cooling_is_on = False
                setFanSpeed(0)
                continue

            #   compute new output from the PID according to the systems current temperature
            cycle = int(round(pid(temperature), 0))

            #   feed the PID output to the system and get its current temperature
            temperature = getCpuTemperature()
            #print ('Setpoint: 45 - Temp: ' + str(temperature) + ' - Fan Speed: ' + str(cycle) + '%')

            #   set the fan speed to the new output if it has changed
            if cycle != fan_speed:
                setFanSpeed(cycle)
        else:
            # check if it can be safely turned on
            if temperature > 58:
                print ('Cooling is on')
                cooling_is_on = True
                setFanSpeed(50)
                continue
            
        #   allow temperature to adjust based on changed fan speed
        processing_seconds = time.time() - start_time
        if processing_seconds < loop_seconds:
            time.sleep (loop_seconds - processing_seconds)
        
# start a thread to control the fan speed
thread = threading.Thread(target=fan_control)
thread.start()