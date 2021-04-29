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
import db_save
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shedDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
db = SQLAlchemy(app)

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
vars_disp = vars_eng
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

@app.route('/SHED3')
def SHED3():
    return render_template('SHED3_nosettings.html', vars_eng = vars_disp, limits = alarm, shed=shed_status)
    
@app.route('/all_control')
def all_control():
    print("Page reload")
    #print(alarm["Gas_analyzer_shed2"].limit_low)
    return render_template('all_control.html', vars_eng = vars_disp, limits = alarm, shed=shed_status)



#------------------- Data routes used by JQuery ------------------------------------------------------------------------

@app.route('/_update_page_variables')                            #Accepts variables list from js and returns current values. 
def update_page_data():
    variables_requested = list(request.args.to_dict().keys())
    data = {}
    for variable in variables_requested:
        if variable in vars_disp.keys():
            data[variable] = vars_disp[variable]
        elif "SHED_request" in variable:
            print(variable, shed_status[variable].request)
            data[variable] = shed_status[variable].request
        elif "alarm_" in variable:
            temp_var = variable[6:]
            data[variable] = alarm[temp_var].state
        elif "warning_" in variable:
            temp_var = variable[8:]
            data[variable] = alarm[temp_var].state
        elif "pid_" in variable:
            temp_shedvar = variable[4:].upper()
            data[variable] = shed_status[temp_shedvar].pid_state
            #print(data)
        elif "trafficlight_" in variable:
            temp_statevar = variable[13:].upper()
            data[variable]= shed_status[temp_statevar].state
        elif "timer_shed3" in variable:
            data[variable] = shed_status["SHED3"].timer()
        elif "timer_status_shed3" in variable:
            data[variable] = shed_status["SHED3"].timer_state
    return jsonify(ajax_data=data)

@app.route("/_alarm_reset")
def alarm_reset():
    alarm_to_reset_dict = request.args
    alarm_to_reset = list(alarm_to_reset_dict.keys())[0]
    alarm[alarm_to_reset].reset

    print(str(alarm_to_reset) + ": Reset to state = " + str(alarm[alarm_to_reset].state))
    return jsonify(ajax_response="Reset Alarm: " + str(alarm_to_reset) + ". state is now 0")


@app.route('/_set_variable_value')                                 #Accepts requested control variable from user and sends values to background task.
def set_variable_value():
    variable_to_set = request.args.to_dict()
    variable = list(request.args.to_dict().keys())
    variable_name = variable[0]
    print("Received request to update setting: " + variable_name + " to new value: " + variable_to_set[variable_name])
    if "_request" in variable_name:
        queue.put({"update_shed_request": variable_to_set})
    elif "high_" in variable_name or "low_" in variable_name:
        queue.put({"limit_set_request": variable_to_set})
    elif "pid" in variable_name:
        queue.put({"PID_change_request" : variable_to_set})
    elif "setpoint_" in variable_name:
        queue.put({"SHED_setpoint_request" : variable_to_set})
    elif "timer_status" in variable_name:
        queue.put({"update_timer_state" : variable_to_set})
    else:
        queue.put({"write_channels": variable_to_set})

    db_save.save_data(vars_raw, vars_eng) # saves to dataset whenever a button is pressed.
    return jsonify(ajax_response="Received variable -> value: " + str(variable_name) + " -> " + str(variable_to_set[variable_name]))

@app.route('/_maq20_fetch_data')                            #Used for maq20_overview.html - not super useful outside of an overview
def maq20_fetch_data():
    data = daq.read_modules(daq.modules)
    print(data)
    return jsonify(ajax_data=data)

@app.route('/_initialize_data') # initialize data on page reload for each plot. 
def initialize_data(): ## Made to work, needs to be updated with appropriate values if 
    records = db_save.EngData.query.order_by(db_save.EngData.timestamp.desc()).limit(100).all()
    #print(records)

    
    T_shed2 = []
    T_shed3 = []
    Valve_shed3_hot = []
    Valve_shed2_cold = []
    Valve_shed2_hot = []
    time = []

    for entry in records:
        time.append(entry.chart_time)   
        Valve_shed3_hot.append(entry.Valve_shed3_hot)
        Valve_shed2_hot.append(entry.Valve_shed2_hot)
        Valve_shed2_cold.append(entry.Valve_shed2_cold)
        T_shed2.append(entry.T_shed2)
        T_shed3.append(entry.T_shed3)
    print(type(records))
    T_shed3.reverse()
    time.reverse()
    T_shed2.reverse()
    Valve_shed3_hot.reverse()
    Valve_shed2_cold.reverse()
    Valve_shed2_hot.reverse()

    Valve_shed3_hot.reverse()
    print("time values are: ",time)
    return jsonify(time=time, T_shed2=T_shed2,T_shed3=T_shed3, Valve_shed3_hot=Valve_shed3_hot, Valve_shed2_hot=Valve_shed2_hot, Valve_shed2_cold=Valve_shed2_cold)

@app.route('/_update_data') # update chart data
def update_data():
        # time = vars_eng["time"]
        # day = day
        
    return jsonify(data = vars_eng)



    
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
                    elif key == "update_shed_request":
                        update_shed_request(task[key])
                    elif key == "limit_set_request":
                        update_alarm_limit(task[key])
                    elif key == "PID_change_request":
                        pid_onoff(task[key])
                    elif key == "SHED_setpoint_request":
                        setpoint_change(task[key])
                    elif key == "update_timer_state":
                        shed_status["SHED3"].timer_toggle()
                    else:
                        print("Background task error: The task does not exist")
            t_now = datetime.now()
            sleep(0.01)
        t_next = t_next + timedelta(seconds=1)              # runs every 1 second (Slower tasks, reading daq etc)
        t_now = datetime.now()
        ##### Scheduled tasks for background ###
        read_daq()
        update_calculated_variables()
        alarm_monitor()  # Alarm monitor needs to be before update_display_variables() for some reason vars_eng is updated in that function?
        shed_pid()
        update_display_variables()
        
        
def dataHandler():
    ## Responsible for saving data to database and send data through the socket to be used in plots
    print("Background database save thread started -  Delay for population of Engineering Values")
    sleep(10) # allow for vars_eng population
    print("Background database save thread start recording")

    while True:
        ##### Scheduled tasks for background ###
        db_save.save_data(vars_raw, vars_eng)
        records = vars_eng #db_save.EngData.query.order_by(db_save.EngData.timestamp.desc()).limit(1).all()
        #print("Engineering Values saved to 'shedDB.db'")
        #---- Un-comment and edit below if socket to be used---------##
        #socketio.emit('newchartdata3', {'T_shed3':records['T_shed3'], 'Valve_shed3_hot': records['Valve_shed3_hot'], 'time':records['time']}, namespace='/test')
        #socketio.sleep(5)
        sleep(60) # comment if socket used

#---------------------- Update SHED operation functions ----------------------------------------------------------------

def update_shed_request(request): # update shed request from webpage input
    
    for key, value in request.items():
        key_fixed = key[:5]
        shed_status[key_fixed].change_request(value)
        shed_status[key_fixed].update_state()
        daq.write_channels(shed_status[key_fixed].new_state_output())
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
    active_alarm = []
    for key in alarm:
        if "Flowmeter_" in key:
            pump_temp = key.replace("Flowmeter_", "Pump_")
            pump_related = vars_eng[pump_temp]
        elif "T_" in key:
            pump_temp = key.replace("T_", "Pump_")
            pump_related = vars_eng[pump_temp]
        else:
            pump_related = "none"
        alarm[key].update_state(vars_eng[key], pump_related)
        
        if alarm[key].state == 1:
            active_alarm.append(key)
            #print(active_alarm)
    for key in shed_status:
        shed_status[key].state_monitor(active_alarm)

    
def shed_pid(): #shed_label should be SHED2 or 3 depending which is active
    pid_output = {}
    for shed_label in shed_status.keys():       
        pid_output = shed_status[shed_label].pid_func(float(vars_eng[shed_status[shed_label].pid_control]))

    if hasattr(pid_output, 'keys'):
        #print(pid_output)
        daq.write_channels(pid_output)
 


def pid_onoff(pid_shed):
    for key, value in pid_shed.items():
        temp_shedvar = key[4:].upper()
        shed_status[temp_shedvar].change_pid(value)

def setpoint_change(task):
    for key, value in task.items():
        temp_shedvar = key[-5:].upper()
        temp_change = key[-7].lower()
        #print(temp_shedvar, temp_change)
        if "_T_" in key:
            shed_status[temp_shedvar].set_temp = value
        else:
            shed_status[temp_shedvar].temp_change = value



def update_calculated_variables():
    vars_eng["T_shed2"] = round((vars_eng["T_shed2_l"] + vars_eng["T_shed2_r"] / 2), 2)
    vars_eng["T_shed3"] = round((vars_eng["T_shed3_l"] + vars_eng["T_shed3_r"] / 2), 2)

def update_display_variables():
    vars_disp = vars_eng
    # vars_disp["T_shed2"] = str(round(float(vars_eng["T_shed2"]), 1)) + u'\N{DEGREE SIGN}' + "C"
    # vars_disp["T_shed3"] = str(round(float(vars_eng["T_shed3"]),1)) + u'\N{DEGREE SIGN}' + "C"

    for key in vars_eng.keys():
        if "Flowmeter" in key:
            vars_disp[key] = str(round(float(vars_eng[key]),2))# + " GPM"
        if "T_" in key:
             vars_disp[key] = str(round(float(vars_eng[key]), 1))# + ' ' + u'\N{DEGREE SIGN}' + "C"

def deadhead_protection():
    pass
    # get position of valve and if position is less than a value in config, pump shuts off


#--------------------- Initialize background thread --------------------------------------------------------------------
daq.write_channels(all_off)
queue = Queue()
background = Thread(target=background_tasks, args=(queue,))
background2 =  Thread(target=dataHandler)
background.daemon = True
background2.daemon = True




#-------------------- Start flask app on wsgi server -------------------------------------------------------------------

if __name__ == '__main__':
    
    #socketio.run(app, host='0.0.0.0')  # used for eventlet with socketio
    background.start()
    background2.start()
    #socketio.run(app, host='0.0.0.0', use_reloader=False) #This requires chosing the correct http or https version of socket io in the .js.
    serve(app, port=5000)               # used for waitress, without sockets