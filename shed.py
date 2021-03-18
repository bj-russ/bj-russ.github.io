from simple_pid import PID

class shed():

    def __init__(self, name, settings):
        self.settings = settings
        self.request = "false"
        self.name = name
        self.state = "off"
        self.configs = settings['state_settings'] # ['on'], ['off'], ['alarm']
        self.set_temp = settings['set_temp']
        self.set_temp_high = self.set_temp + 3
        self.set_temp_low = self.set_temp - 3
        self.pid_state = "off"  
        if "PID" in settings:
            self.p = settings["PID"]["p"]
            self.i = settings["PID"]["i"]
            self.d = settings["PID"]["d"]
            self.pid = PID(self.p, self.i, self.d, self.set_temp)
            self.pid_valve = settings["PID"]["valve_control"]
            self.pid_control = settings["PID"]["control"]
            self.pid_state = False

    def change_request(self, value):
        self.request = value
        self.update_state()


    def update_state(self):
        if self.state != "alarm":
            if self.request == "true":
                self.state = "on"
            if self.request == "false":
                self.state = "off"          
        if self.state == "alarm":
            pass # possibly add in fuction to bring up pop up window to clear alarms?

    def new_state_output(self):
        return self.configs[self.state]

    def change_set_temp(self, temp_set):
        self.set_temp = temp_set
    
    def change_pid(self, newset):
        self.pid_state = newset
        

    def pid_func(self, SHED_temp_current):
        self.pid.setpoint = self.set_temp
        return self.pid(SHED_temp_current)
class alarm():
    def __init__(self, name, settings):
        self.settings = settings
        self.name = name
        self.state = settings["state"]
        self.type = settings["limit_type"]
        self.limit_high = settings["limits"]["high"]
        self.limit_low = settings["limits"]["low"]
        self.active_config = settings["active_config"]

    def update_state(self, reading):
        if "Gas" in self.name:
            if self.state == 0: 
                if self.type == "inside":
                    if float(reading) > float(self.limit_high) or float(reading) < float(self.limit_low):
                        self.state = 1
            elif self.state == 1: 
                pass # Alarm will not automatically reset!
        
        else:
            if self.state == 0: 
                if self.type == "inside":
                    if float(reading) < float(self.limit_high) and float(reading) > float(self.limit_low):
                        self.state = 0
                    else:
                        self.state = 1
            elif self.state == 1: ## change this if disabling alarm is required
                if self.type == "inside":
                    if float(reading) < float(self.limit_high) and float(reading) > float(self.limit_low):
                        self.state = 0
                    else:
                        self.state = 1
        
    def reset(self):
        self.state = 0

    def alarm_output(self):
        return self.active_config

    def change_limit(self, limit, lim_set):
        """
        lim name: name from javascript including "high_" or "low_" as the prefix
        lim_set: set limit value entered in web interface
        """
        if limit == "low" and lim_set.isnumeric():
            self.limit_low = lim_set
            #print("Change alarm great success!")
        if limit == "high" and lim_set.isnumeric():
            self.limit_high = lim_set
    
