demo = True
if demo:
    import daq_demo as daq
else:
    import daq
from alarms import alarm
from flask import Flask, render_template, jsonify, request
from threading import Thread, Event, Lock
from queue import Queue, Empty
from flask_socketio import SocketIO, emit
import json
from time import sleep
from datetime import datetime, timedelta
#import eventlet                # If using sockets. Otherwise sockets will use long polling (cross platform)
from waitress import serve      # Production server for windows applications
#import gunicorn                # Production server for linux applications
import auxiliary_calculations
import shed
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
# app.config['AQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
# db = SQLAlchemy(app)
#socketio = SocketIO(app)       # If using sockets. Binds SocketIO to app

#----------------- Load settings from config file, initiate daq -------------------------------------------------------

with open('config.json') as json_file:
    settings = json.load(json_file)

daq = daq.dataforth(settings)

#----------------- Build variables dictionary - Can also have scales, eng units etc -----------------------------------

daq_channels = []
for key in settings["channel_map_inputs"]:
    daq_channels.append(key)
for key in settings["channel_map_outputs"]:
    daq_channels.append(key)
vars_raw = {}
for channel in daq_channels:
    vars_raw[channel] = channel
vars_eng = {}
for channel in vars_raw.keys():
    vars_eng[channel] = 0 #vars_raw[channel]
vars_sys = {}
for channel in settings['system_variables'].keys():
    vars_sys[channel] = settings['system_variables'][channel]
calibration = settings["calibration"]
all_off = settings["all_off"]



#------------------- Initialize alarms ---------------------------------------------------------------------------------
alarm = {}
for key in settings["alarm"]:
    alarm[key] = shed.alarm(key,settings["alarm"][key])



#-------------------Initialize SHED class ------------------------------------------------------------------------------
shed_status = {}

for key in settings["system_variables"]:
    shed_status[key] = shed.shed(key, settings["system_variables"][key])
#------------------- Route Functions - Perform task when browser directs to link (serves html etc) ---------------------

#------------------- Html routes ---------------------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('permeation.html')

@app.route('/maq20_overview.html')
def maq20_overview():
    return render_template('maq20_overview.html')

@app.route('/permeation.html')
def permeation():
    return render_template('permeation.html')

@app.route('/health')
def all_health():
    return render_template('all_health.html')
    
@app.route('/all_control')
def all_control():
    print("Page reload")
    print(alarm["Gas_analyzer_shed2"].limit_low)
    return render_template('all_control.html', vars_eng = vars_eng, limits = alarm, shed=shed_status)

#------------------- Data routes used by JQuery ------------------------------------------------------------------------

@app.route('/_update_page_variables')                            #Accepts variables list from js and returns current values. 
def update_page_data():
    variables_requested = list(request.args.to_dict().keys())
    data = {}
    for variable in variables_requested:
        if variable in vars_eng.keys():
            data[variable] = vars_eng[variable]
    #print(variables_requested)
    return jsonify(ajax_data=data)

@app.route('/_set_variable_value')                                 #Accepts requested control variable from user and sends values to background task.
def set_variable_value():
    variable_to_set = request.args.to_dict()
    variable = list(request.args.to_dict().keys())
    variable_name = variable[0]
    print("Received request to update setting: " + variable_name + " to new value: " + variable_to_set[variable_name])
    if "SHED" in variable_name:
        queue.put({"update_shed_request": variable_to_set})
    elif "high_" in variable_name or "low_" in variable_name:
        queue.put({"limit_set_request": variable_to_set})
    else:
        queue.put({"write_channels": variable_to_set})

    return jsonify(ajax_response="Received variable -> value: " + str(variable_name) + " -> " + str(variable_to_set[variable_name]))

@app.route('/_maq20_fetch_data')                            #Used for maq20_overview.html - not super useful outside of an overview
def maq20_fetch_data():
    data = daq.read_modules(daq.modules)
    return jsonify(ajax_data=data)

#--------------------- Regular functions - Can be used by routes, background thread etc. --------------------------------------------------------

def read_daq():                                             # get current channel values from list in vars_raw
    channels = daq_channels
    data = daq.read_channels(channels)
    #print(data)
    update_variables(data)

def update_variables(data):                                 # updates the variables dictionary with new values
    for key in data.keys():
        vars_raw[key] = data[key]
    temp = auxiliary_calculations.raw_to_eng(vars_raw, calibration)
    for key in temp.keys():
        vars_eng[key] = temp[key]
#--------------------- Background Task - This Parallel function to the Flask functions. Used for managing daq, calling threads with control functions etc. Will run without client connected.

def background_tasks(queue=Queue): 
    print("Background thread started")
    t_now = datetime.now()
    t_next = t_now + timedelta(seconds=1)
    while True:
        while t_now < t_next:                               # runs at higher frequency (Event based execution using queue etc.)
            if not queue.empty(): # process queue
                task = queue.get()
                for key in task.keys():
                    if key == "write_channels":
                        daq.write_channels(task[key])
                        #vars_raw = task[key]
                    elif key == "update_shed_request":
                        update_shed_request(task[key])
                    elif key == "limit_set_request":
                        update_alarm_limit(task[key])
                    else:
                        print("Background task error: The task does not exist")
            t_now = datetime.now()
            sleep(0.01)
        t_next = t_next + timedelta(seconds=1)              # runs every 1 second (Slower tasks, reading daq etc)
        t_now = datetime.now()
        read_daq()
        update_calculated_variables()

        alarm_monitor()

#---------------------- Update SHED operation functions ----------------------------------------------------------------

def update_shed_request(request): # update shed request from webpage
    for key, value in request.items():
        shed_status[key].change_state(value)
        daq.write_channels(shed_status[key].new_state_output())
    if shed_status["SHED1"].state == shed_status["SHED2"].state == shed_status["SHED3"].state == "off":
        daq.write_channels(all_off)


def update_alarm_limit(request):
    for key, value in request.items():
        if key.startswith("low_"):
            key2 = key[4:]
            alarm[key2].change_limit("low",request[key])
            print("change alarm success!")
        if key.startswith("high_"):
            key2 = key[5:]
            alarm[key2].change_limit("high",request[key])
            print("change alarm success!")



def alarm_monitor():
    for key in alarm:
        alarm[key].update_state(vars_eng[key])

def shed_pid(shed_label): #shed_label should be SHED2 or 3 depending which is active
    pid_output = {}
    pid_output[shed_status[shed_label].pid_valve] = shed_status[shed_label].pid_func(vars_eng[shed_status[shed_label].pid_control])


def update_calculated_variables():
    vars_eng["T_shed2"] = str(round((vars_eng["T_shed2_l"] + vars_eng["T_shed2_r"] / 2), 2)) 
    vars_eng["T_shed3"] = str(round((vars_eng["T_shed3_l"] + vars_eng["T_shed3_r"] / 2), 2))

def deadhead_protection():
    pass
    # get position of valve and if position is less than a value in config, pump shuts off


#--------------------- Initialize background thread --------------------------------------------------------------------
daq.write_channels(all_off)
queue = Queue()
background = Thread(target=background_tasks, args=(queue,))
background.daemon = True
background.start()

#-------------------- Start flask app on wsgi server -------------------------------------------------------------------

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0')  # used for eventlet with socketio
    serve(app, port=5000)               # used for waitress, without sockets