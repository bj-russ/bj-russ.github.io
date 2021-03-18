import time
import json

with open('config.json') as json_file:
    settings = json.load(json_file)
calibration = settings["calibration"]


flow_count = {
        'Flowmeter_shed3_hot':  [0,time.time()],  # [previous pulse count, previous time]
        'Flowmeter_shed3_cold': [0,time.time()],  # [previous pulse count, previous time]
        'Flowmeter_shed2_hot':  [0,time.time()],  # [previous pulse count, previous time]
        'Flowmeter_shed2_cold': [0,time.time()],  # [previous pulse count, previous time]
        'Flowmeter_main_hot':   [0,time.time()],  # [previous pulse count, previous time]
        'Flowmeter_main_cold':  [0,time.time()],  # [previous pulse count, previous time]
        'Flowmeter_shed1_hot':  [0,time.time()],  # [previous pulse count, previous time]
        'Flowmeter_shed1_cold': [0,time.time()],  # [previous pulse count, previous time]
    }

def pulse_to_frequency(key, value):
    prev_count = flowcount[key][0]
    current_count = value
    prev_time = flowcount[key][1]
    current_time = time.time()
    sample_time = (current_time - prev_time)  ## sample time in seconds
    frequency = (current_count - prev_count) / (sample_time)
    return frequency

def frequency_to_flowrate(key, frequency):
    flowrate = round(frequency * 60 / calibration[key], 2)                    ## Hz / ppg = gal/min
    return flowrate
def raw_to_eng(data, calibration):
    """
    data is the dictionary passed from the daw during the input. 
    return: new_data dictionary with values changed from raw values to engineering values
    """
    new_data = {}
    for key, value in data.items():
        if key.endswith("_l", 7,9) or key.endswith("_r", 7,9):
            new_data[key] = value*calibration[key]
        #elif key.startswith("Flowmeter_"):
        #    print(key, value)
        #    new_data[key] = frequency_to_flowrate(key,value)
        else:
            new_data[key] = value
    return new_data

def alarm_limit_check(var_eng_dict,alarm_dict):
    """
    Input Upated Engineering Variables to compare to limits set in alarms dict
    Return: Alarm dict with updated alarm status in ["alarm_desctiption"][0] to be updated in main app.py
    """
    # alarm_dict[0]: if 0: no alarm, if 1: inital alarm trigger, if 2: alarm has been acknowledged but still active

    
    new_dict = alarm_dict
    for key in new_dict.keys():
        if new_dict[key][0] == 2:  ## Possible use of "alarm acknowleged but still active"
            pass  # check if has been reset then set to zero?
        elif new_dict[key][0] == 0 and var_eng_dict[key] < new_dict[key][1] or var_eng_dict[key] > new_dict[key][2]: # Alarm not previously triggered and eng_vals outside of alarm 
            new_dict[key][0] = 1  # change alarm to active
        elif new_dict[key][0] == 2 and var_eng_dict[key] > new_dict[key][1] and var_eng_dict[key] < new_dict[key][2]: # alarm acknowledged and eng_vals inside of limits
            new_dict[key][0] = 0
        else:
            new_dict[key][0] = 0
    return new_dict





