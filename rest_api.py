from flask import Flask, request
import subprocess  # for command execution
import os

from modules.fancontroller import setFanSpeed, getCpuTemperature, getFanSpeed

def turn_off_monitor(display=":0.0", output="HDMI-A-1"):
    try:
        #command = f"DISPLAY={display} xrandr --output {output} --off"
        #command = f"xrandr -display {display} --output {output} --off"
        # wayland
        command = f"wlr-randr --output {output} --off"
        #print (command)
        subprocess.call(command, shell=True)
        return f"Monitor {output} turned off successfully on display {display}."
    except Exception as e:
        return f"An error occurred: {e}"

def turn_on_monitor(display=":0.0", output="HDMI-A-1", mode="1280x800 --rate 30"):
    try:
        #command = f"DISPLAY={display} xrandr --output {output} --mode {mode}"
        #command = f"xrandr -display {display} --output {output} --mode {mode}" # for X
        # wayland
        command = f"wlr-randr --output {output} --on"
        #print (command)
        subprocess.call(command, shell=True)
        return f"Monitor {output} turned on successfully on display {display}."
    except Exception as e:
        return f"An error occurred: {e}"

def create_app():
    print("Starting Snips Services")

    ################################################################
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "snipsservices-boom-!!123"

    # add a route to turn the display on or off
    @app.route('/display/<state>')
    def display(state):
        res = None
        if state == "on":
            res = turn_on_monitor()
        elif state == "off":
            res = turn_off_monitor()
        return res

    @app.route('/ping/<ip>')
    def ping(ip):
        response = os.system("ping -c 1 " + ip + " > /dev/null 2>&1")
        if response == 0:
            return {'ResponseCode': 'ONLINE'}
        else:
            return {'ResponseCode': 'OFFLINE'}

    # @app.route('/', methods=['GET', 'POST'])
    # def index():
    #     return render_template('index.html')

    @app.route('/fan/<speed>')
    def fan(speed):
        setFanSpeed(int(speed))
        return {"fan_speed": speed}

    @app.route('/temp')
    def temp():
        # global cur_temp, fan_speed
        # # use call to check temp and adjust fan speed
        # temp = getCpuTemperature()
        # cur_temp = temp
        # if temp > 57. and fan_speed < 100:
        #     setFanSpeed(100)
        # elif temp > 50. and fan_speed < 75:
        #     setFanSpeed(75)
        # elif temp > 45. and fan_speed == 0:
        #     setFanSpeed(50)
        # elif temp < 45. and fan_speed > 50:
        #     setFanSpeed(50)
        # elif temp < 40. and fan_speed > 25:
        #     setFanSpeed(25)
        # elif temp < 35. and fan_speed == 25:
        #     setFanSpeed(0)

        # print (f"Temperature: {temp}°C, Fan Speed: {fan_speed}%")

        # return the CPU temperature
        return {"temperature": getCpuTemperature(), "fan_speed": getFanSpeed()}

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8888)
