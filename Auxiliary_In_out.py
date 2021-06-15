from maq20 import MAQ20
import random
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time


demo = 1
serial = 1
flowrate_pulse_method = True
update_all_io = True

def read(channel,channel_type):  # accepts channel name, returns dict of {channel name: value} and checks for enabled counters.
    channel_map = eval("channel_map_" + channel_type)
    if hasattr(eval(str(channel_map[channel])[:-3]),
               'read_special_function_2_pulse_frequency_counter_with_debounce'):  # check if module configured for DIOL
        if str(channel_map[channel])[-2] == '0':  # check if channel is counter input
            return \
            eval(str(channel_map[channel])[:-3]).read_special_function_2_pulse_frequency_counter_with_debounce(timer=0)[
                'Frequency']
        elif str(channel_map[channel])[-2] == '2':
            return \
            eval(str(channel_map[channel])[:-3]).read_special_function_2_pulse_frequency_counter_with_debounce(timer=1)[
                'Frequency']
        else:
            return eval(str(channel_map[channel]))
    else:
        if 'DIV20' in str(channel_map[channel]):
            return eval(str(channel_map[channel])[:-3]).read_data_counts(int(channel[-2]), number_of_channels=1)[0]
        else:
            return eval(str(channel_map[channel]))


def read_modbus_register(channel):  # used to read the state of DIO outputs.
    module = str(channel_map_outputs[channel])[:-3]
    channel_number = int(str(channel_map_outputs[channel])[-2]) + 1000
    register_value = eval(module).read_register(channel_number)
    return register_value


def read_channels(
        channels):  # accepts a list of requested channel names: eg ['T_shed2_cold': 'T_shed2_hot'] and returns dict of {channel name: values}
    data = {}
    for channel in channels:
        if channel in channel_map_inputs.keys():
            data[channel] = read(channel, "inputs")
        elif channel in channel_map_outputs.keys():
            if 'DIOL' in str(channel_map_outputs[channel]):
                data_cur = read_modbus_register(channel)
                if data_cur == 1:  # invert logic so 0 = 1, 1 = 0
                    data[channel] = 0
                else:
                    data[channel] = 1
                # data[channel] = read_modbus_register(channel)
            else:
                data[channel] = read(channel, "outputs")
        else:
            data[channel] = 'chan_name_error'
    # call scale/calibration function and correct values before returning
    return data


channel_configs = {
    "Exhaust_damper": "frequency_generator",
    'Flowmeter_shed1_hot': 'counter',
    'Flowmeter_shed1_cold': 'counter',
    'Flowmeter_shed2_hot': 'counter',
    'Flowmeter_shed2_cold': 'counter',
    'Flowmeter_shed3_hot': 'counter',
    'Flowmeter_shed3_cold': 'counter',
    'Flowmeter_main_hot': 'counter',
    'Flowmeter_main_cold': 'counter',
}
display_values = {
    'T_shed2':  'null',
    'T_shed3' : 'null',
    'Flowmeter_shed3_hot' : 'null',
    'Flowmeter_shed3_cold' : 'null',
    'Flowmeter_shed2_hot' : 'null',
    'Flowmeter_shed2_cold' : 'null',
    'Flowmeter_main_hot' : 'null',
    'Flowmeter_main_cold' : 'null',
    'Flowmeter_shed1_hot' : 'null',
    'Flowmeter_shed1_cold' : 'null',
    'T_shed3_hot' : 'null',
    'T_shed3_cold' : 'null',
    'T_shed2_hot' : 'null',
    'T_shed2_cold' : 'null',
    'T_main_hot' : 'null',
    'T_main_cold' : 'null',
    'T_shed1_hot' : 'null',
    'T_shed1_cold' : 'null'
}
status_check = {
    'Exhaust_fan': 'null'
}
if demo != 1:
    maq20 = MAQ20(ip_address=ip, port=502)  # Set communication with MAQ20
    #initialize values from MAQ20
    mod1_AI_MVDN = (maq20[1].read_data(0, number_of_channels=maq20[1].get_number_of_channels()))
    mod2_AI_TTC = (maq20[2].read_data(0, number_of_channels=maq20[2].get_number_of_channels()))
    mod3_AO_VO = maq20[3].read_data(0, number_of_channels=maq20[2].get_number_of_channels())
    mod4_DI_DIV20 = (maq20[4].read_data_counts(0, number_of_channels=maq20[4].get_number_of_channels()))
    mod5_DI_DIOL = (maq20[5].read_data_counts(0, number_of_channels=maq20[5].get_number_of_channels()))
    mod6_DI_DIOL = (maq20[6].read_data_counts(0, number_of_channels=maq20[6].get_number_of_channels()))
    mod7_DI_DIOL = (maq20[7].read_data_counts(0, number_of_channels=maq20[7].get_number_of_channels()))
    mod8_DI_DIOL = (maq20[8].read_data_counts(0, number_of_channels=maq20[8].get_number_of_channels()))


class InputValues:
    calibration = {
        'T_shed2_l' :0.798*100,         # calibration of analog temperature sensor
        'T_shed2_r': 0.798*100,          # calibration of analog temperature sensor
        'T_shed3_l': 0.798*100,          # calibration of analog temperature sensor
        'T_shed3_r': 0.798*100,          # calibration of analog temperature sensor
        'Flowmeter_shed3_hot': 55,    # ppg
        'Flowmeter_shed3_cold': 55,   # ppg
        'Flowmeter_shed2_hot': 55,    # ppg
        'Flowmeter_shed2_cold': 55,   # ppg
        'Flowmeter_main_hot': 55,     # ppg
        'Flowmeter_main_cold': 55,    # ppg
        'Flowmeter_shed1_hot': 55,    # ppg
        'Flowmeter_shed1_cold': 55,   # ppg
    }
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
    channel_map = {
        'T_shed2_l': 'mod1_AI_MVDN[0]',
        'T_shed2_r': 'mod1_AI_MVDN[1]',
        'T_shed3_l': 'mod1_AI_MVDN[2]',
        'T_shed3_r': 'mod1_AI_MVDN[3]',
        'Gas_analyzer_shed2': 'mod1_AI_MVDN[4]',
        'Gas_analyzer_shed3': 'mod1_AI_MVDN[5]',
        'MVDN_Placeholder_7': 'mod1_AI_MVDN[6]',
        'MVDN_Placeholder_8': 'mod1_AI_MVDN[7]',
        'T_shed2_cold': 'mod2_AI_TTC[0]',
        'T_shed2_hot': 'mod2_AI_TTC[1]',
        'T_shed3_cold': 'mod2_AI_TTC[2]',
        'T_shed3_hot': 'mod2_AI_TTC[3]',
        'T_main_hot': 'mod2_AI_TTC[4]',
        'T_main_cold': 'mod2_AI_TTC[5]',
        'T_shed1_cold': 'mod2_AI_TTC[6]',
        'T_shed1_hot': 'mod2_AI_TTC[7]',
        'Valve_shed3_hot': 'mod3_AO_VO[0]',
        'Valve_shed3_cold': 'mod3_AO_VO[1]',
        'Valve_shed2_hot': 'mod3_AO_VO[2]',
        'Valve_shed2_cold': 'mod3_AO_VO[3]',
        'Valve_main_hot': 'mod3_AO_VO[4]',
        'Valve_main_cold': 'mod3_AO_VO[5]',
        'Valve_shed1_cold': 'mod3_AO_VO[6]',
        'Valve_shed1_hot': 'mod3_AO_VO[7]',
        'DIV20_Placeholder_1': 'mod4_DI_DIV20[0]',
        'DIV20_Placeholder_2': 'mod4_DI_DIV20[1]',
        'DIV20_Placeholder_3': 'mod4_DI_DIV20[2]',
        'DIV20_Placeholder_4': 'mod4_DI_DIV20[3]',
        'DIV20_Placeholder_5': 'mod4_DI_DIV20[4]',
        'DIV20_Placeholder_6': 'mod4_DI_DIV20[5]',
        'DIV20_Placeholder_7': 'mod4_DI_DIV20[6]',
        'DIV20_Placeholder_8': 'mod4_DI_DIV20[7]',
        'DIV20_Placeholder_9': 'mod4_DI_DIV20[8]',
        'DIV20_Placeholder_10': 'mod4_DI_DIV20[9]',
        'DIV20_Placeholder_11': 'mod4_DI_DIV20[1]',
        'DIV20_Placeholder_12': 'mod4_DI_DIV20[11]',
        'DIV20_Placeholder_13': 'mod4_DI_DIV20[12]',
        'DIV20_Placeholder_14': 'mod4_DI_DIV20[13]',
        'DIV20_Placeholder_15': 'mod4_DI_DIV20[14]',
        'DIV20_Placeholder_16': 'mod4_DI_DIV20[15]',
        'DIV20_Placeholder_17': 'mod4_DI_DIV20[16]',
        'DIV20_Placeholder_18': 'mod4_DI_DIV20[17]',
        'DIV20_Placeholder_19': 'mod4_DI_DIV20[18]',
        'DIV20_Placeholder_20': 'mod4_DI_DIV20[19]',
        'Pump_shed3_hot': 'mod5_DIO_DIOL[0]',
        'Pump_shed3_cold': 'mod5_DIO_DIOL[1]',
        'Pump_shed2_hot': 'mod5_DIO_DIOL[2]',
        'Pump_shed2_cold': 'mod5_DIO_DIOL[3]',
        'Pump_main_hot': 'mod5_DIO_DIOL[4]',
        'Flowmeter_shed3_hot': 'mod5_DIO_DIOL[5]',
        'Request_shed3': 'mod5_DIO_DIOL[6]',
        'Flowmeter_shed3_cold': 'mod5_DIO_DIOL[7]',
        'mod5_DIO_DIOL_Placeholder9': 'mod5_DIO_DIOL[8]',
        'mod5_DIO_DIOL_Placeholder10': 'mod5_DIO_DIOL[9]',
        'Pump_main_cold': 'mod6_DIO_DIOL[0]',
        'Pump_shed1_cold': 'mod6_DIO_DIOL[1]',
        'Pump_shed1_hot': 'mod6_DIO_DIOL[2]',
        'Door_shed2_seal': 'mod6_DIO_DIOL[3]',
        'Exhaust_shed2': 'mod6_DIO_DIOL[4]',
        'Flowmeter_shed2_hot': 'mod6_DIO_DIOL[5]',
        'Request_shed2': 'mod6_DIO_DIOL[6]',
        'Flowmeter_shed2_cold': 'mod6_DIO_DIOL[7]',
        'mod6_DIO_DIOL_Placeholder9': 'mod6_DIO_DIOL[8]',
        'mod6_DIO_DIOL_Placeholder10': 'mod6_DIO_DIOL[9]',
        'Request_good_shed1': 'mod7_DIO_DIOL[0]',
        'Request_good_shed2': 'mod7_DIO_DIOL[1]',
        'Request_good_shed3': 'mod7_DIO_DIOL[2]',
        'Door_shed3_seal': 'mod7_DIO_DIOL[3]',
        'Exhaust_shed3': 'mod7_DIO_DIOL[4]',
        'Flowmeter_main_hot': 'mod7_DIO_DIOL[5]',
        'Exhaust_airflow_confirmed': 'mod7_DIO_DIOL[6]',
        'Flowmeter_main_cold': 'mod7_DIO_DIOL[7]',
        'mod7_DIO_DIOL_Placeholder9': 'mod7_DIO_DIOL[8]',
        'mod7_DIO_DIOL_Placeholder10': 'mod7_DIO_DIOL[9]',
        'Exhaust_damper': 'mod8_DIO_DIOL[0]',
        'Exhaust_fan': 'mod8_DIO_DIOL[1]',
        'mod8_DIO_DIOL_Placeholder3': 'mod8_DIO_DIOL[2]',
        'mod8_DIO_DIOL_Placeholder4': 'mod8_DIO_DIOL[3]',
        'mod8_DIO_DIOL_Placeholder5': 'mod8_DIO_DIOL[4]',
        'Flowmeter_shed1_cold': 'mod8_DIO_DIOL[5]',
        'Request_shed1': 'mod8_DIO_DIOL[6]',
        'Flowmeter_shed1_hot': 'mod8_DIO_DIOL[7]',
        'mod8_DIO_DIOL_Placeholder9': 'mod8_DIO_DIOL[8]',
        'mod8_DIO_DIOL_Placeholder10': 'mod8_DIO_DIOL[9]'
    }
    input_raw = {
        'T_shed3_l':  0.0,
        'T_shed3_r' : 0.0,
        'T_shed2_l' : 0.0,
        'T_shed2_r' : 0.0,
        'Flowmeter_shed3_hot' : 0.0,
        'Flowmeter_shed3_cold' : 0.0,
        'Flowmeter_shed2_hot' : 0.0,
        'Flowmeter_shed2_cold' : 0.0,
        'Flowmeter_main_hot' : 0.0,
        'Flowmeter_main_cold': 0.0,
        'Flowmeter_shed1_hot' : 0.0,
        'Flowmeter_shed1_cold' : 0.0,
        'T_shed3_hot' : 0.0,
        'T_shed3_cold' : 0.0,
        'T_shed2_hot' : 0.0,
        'T_shed2_cold' : 0.0,
        'T_main_hot' : 0.0,
        'T_main_cold' : 0.0,
        'T_shed1_hot' : 0.0,
        'T_shed1_cold' : 0.0
    }
    input_eng = {
        'T_shed2' : 0.0,
        'T_shed3' : 0.0,
        'T_shed3_l':  0.0,
        'T_shed3_r' : 0.0,
        'T_shed2_l' : 0.0,
        'T_shed2_r' : 0.0,
        'Flowmeter_shed3_hot' : 0.0,
        'Flowmeter_shed3_cold' : 0.0,
        'Flowmeter_shed2_hot' : 0.0,
        'Flowmeter_shed2_cold' : 0.0,
        'Flowmeter_main_hot' : 0.0,
        'Flowmeter_main_cold': 0.0,
        'Flowmeter_shed1_hot' : 0.0,
        'Flowmeter_shed1_cold' : 0.0,
        'T_shed3_hot' : 0.0,
        'T_shed3_cold' : 0.0,
        'T_shed2_hot' : 0.0,
        'T_shed2_cold' : 0.0,
        'T_main_hot' : 0.0,
        'T_main_cold' : 0.0,
        'T_shed1_hot' : 0.0,
        'T_shed1_cold' : 0.0
    }
    display_values = {
        'T_shed2':  'null',
        'T_shed3' : 'null',
        'Flowmeter_shed3_hot' : 'null',
        'Flowmeter_shed3_cold' : 'null',
        'Flowmeter_shed2_hot' : 'null',
        'Flowmeter_shed2_cold' : 'null',
        'Flowmeter_main_hot' : 'null',
        'Flowmeter_main_cold' : 'null',
        'Flowmeter_shed1_hot' : 'null',
        'Flowmeter_shed1_cold' : 'null',
        'T_shed3_hot' : 'null',
        'T_shed3_cold' : 'null',
        'T_shed2_hot' : 'null',
        'T_shed2_cold' : 'null',
        'T_main_hot' : 'null',
        'T_main_cold' : 'null',
        'T_shed1_hot' : 'null',
        'T_shed1_cold' : 'null'
    }
    status_check = {
        'Exhaust_fan': 'null'
    }
    
    #@classmethod
    def update_raw(self, value):
        if demo == 1: # assigns random values to all inputs for the purpose of demonstration
            self.input_raw.update({'T_shed3_l': random.uniform(0.4, 0.5)})
            self.input_raw.update({'T_shed3_r': random.uniform(0.4, 0.5)})
            self.input_raw.update({'T_shed2_l': random.uniform(0.4, 0.5)})
            self.input_raw.update({'T_shed2_r': random.uniform(0.4, 0.5)})
            self.input_raw['Flowmeter_shed3_hot'] = random.uniform(4.5, 5)
            self.input_raw['Flowmeter_shed3_cold'] = random.uniform(4.5, 5)
            self.input_raw['Flowmeter_shed2_hot'] = random.uniform(4.5, 5)
            self.input_raw['Flowmeter_shed2_cold'] = random.uniform(4.5, 5)
            self.input_raw['Flowmeter_main_hot'] = random.uniform(4.5, 5)
            self.input_raw['Flowmeter_main_cold'] = random.uniform(4.5, 5)
            self.input_raw['Flowmeter_shed1_hot'] = random.uniform(4.5, 5)
            self.input_raw['Flowmeter_shed1_cold'] = random.uniform(4.5, 5)
            self.input_raw['T_shed3_hot'] =  random.uniform(10, 65)
            self.input_raw['T_shed3_cold'] = random.uniform(10, 65)
            self.input_raw['T_shed2_hot'] = random.uniform(10, 65)
            self.input_raw['T_shed2_cold'] = random.uniform(10, 65)
            self.input_raw['T_main_hot'] = random.uniform(10, 65)
            self.input_raw['T_main_cold'] = random.uniform(10, 65)
            self.input_raw['T_shed1_hot'] = random.uniform(10, 65)
            self.input_raw['T_shed1_cold'] = random.uniform(10, 65)

            if demo != 1: # Replace with read channels function if neccesary
                if "MVDN" in self.channel_map[value]:
                    self.input_raw[value] = eval(self.channel_map[value][:-3]).read_data(int(self.channel_map[value][-2]), number_of_channels=1)
                if "DIOL" in self.channel_map[value]:
                    self.input_raw[value] = eval(self.channel_map[value][:-3]).read_data(int(self.input_raw[value][-2]), number_of_channels=1)[0]
            #self.raw_to_eng(self,value)
            return self.input_raw[value]

    def raw_to_eng(self, value):
        if value.endswith("_l", 7, 9) or value.endswith("_r", 7, 9):  # checks to see if shed temperature key from position 7-9 -> will eliminate most other combos ending with _l or _r
            self.input_eng[value] = float(self.input_raw[value] * self.calibration[value])
        elif value.startswith("Flowmeter_"):
            if flowrate_pulse_method:  #if pulse is used to calculate frequency set value to true at top of file:
                prev_count = self.flow_count[value][0]
                prev_time = self.flow_count[value][1]
                current_count = self.input_raw[value]
                current_time = time.time()
                sample_time = prev_time - current_time
                #print(self.flow_count[value])
                #print(current_count, current_time)
                self.input_eng[value] = (self.input_raw[value] - self.flow_count[value][0]+1)*60 / (.1+time.time() - self.flow_count[value][1])
                self.flow_count[value][0] = current_count
                self.flow_count[value][1] = time.time()
            else:
                self.input_eng[value] = self.input_raw[value] / self.calibration[value] # self.calibration[value] is pulses per gallon        
        else:
            self.input_eng[value] = round(self.input_raw[value],2)
        return self.input_eng[value]
    
    def value_update(self,value):
        if value == 'T_shed2':
            a = self.update_raw(self,'T_shed2_l') 
            a = self.raw_to_eng(self, 'T_shed2_l')
            b = self.update_raw(self,'T_shed2_r')
            b = self.raw_to_eng(self, 'T_shed2_r')
            L2 = float(a)#.input_eng['T_shed2_l'])
            R2 = float(b)#.input_eng['T_shed2_r'])
            self.input_eng['T_shed2'] = (L2+R2)/20
            self.display_values.update({value : str(round(self.input_eng[value],2)) + u'\N{DEGREE SIGN}' + "C"})
        elif value == 'T_shed3':
            a = self.update_raw(self,'T_shed3_l')
            a = self.raw_to_eng(self, 'T_shed3_l')
            b = self.update_raw(self,'T_shed3_r')
            b = self.raw_to_eng(self, 'T_shed3_r')
            L3 = float(a)#.input_eng['T_shed2_l'])
            R3 = float(b)#.input_eng['T_shed2_r'])
            self.input_eng['T_shed3']= (L3+R3)/20
            self.display_values.update({value : str(round(self.input_eng[value],2)) + u'\N{DEGREE SIGN}' + "C"})
        elif "Flowmeter" in value:
            flowmeter_value_raw = self.update_raw(self,value)
            self.input_eng[value] = self.raw_to_eng(self,value)
            self.display_values[value] = "Flow rate \n" + str(self.input_eng[value]) + " GPM"
        else:
            self.input_eng[value] = self.raw_to_eng(self, value)
            self.display_values[value] = "Water Temp :" + str(self.input_eng[value])
    
    
    @classmethod
    def update(self, value):  
        if update_all_io is True:
            for key in self.display_values:
                self.value_update(self,key)
        else:
            self.value_update(self,value)

    def __init__(self, value):
        self.value = value
        self.update(value)

#InputValues('T_shed2')    
#a = InputValues('T_shed2')


#print(InputValues.input_eng)


