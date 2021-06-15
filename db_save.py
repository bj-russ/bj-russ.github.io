import app
from app import db
from datetime import datetime, timedelta
import sqlite3

id_count = 0
conn = sqlite3.connect("new_DB.sqlite")
# cur = conn.cursor()
# cur.execute(
#     "CREATE TABLE  rawData (id INTEGER, timestamp DateTime, T_shed2_l FLOAT, T_shed2_r FLOAT)"
    
# )
conn.close()
class SoakData(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary key column if needed
    timestamp = db.Column(db.DateTime, index=True, primary_key=False, unique=True)  # timestamp
    chart_time = db.Column(db.String, index=True, unique=False)
    year = db.Column(db.Integer, index = True, unique = False)
    month = db.Column(db.Integer, index = True, unique = False)
    day = db.Column(db.Integer, index = True, unique = False)
    time = db.Column(db.String, index = True, unique = False)
    T_soak1 = db.Column(db.Float, index =True)
    T_soak2 = db.Column(db.Float, index =True)
    T_soak3 = db.Column(db.Float, index =True)
    T_soak4 = db.Column(db.Float, index =True)
    T_soak5 = db.Column(db.Float, index =True)
    T_soak6 = db.Column(db.Float, index =True)
    T_soak7 = db.Column(db.Float, index =True)
    T_soak8 = db.Column(db.Float, index =True)  
class RawData(db.Model):  # add columns for data model here
    id = db.Column(db.Integer, primary_key=True)  # primary key column if needed
    timestamp = db.Column(db.DateTime, index=True, primary_key=False, unique=True)  # timestamp
    chart_time = db.Column(db.String, index=True, unique=False)
    year = db.Column(db.Integer, index = True, unique = False)
    month = db.Column(db.Integer, index = True, unique = False)
    day = db.Column(db.Integer, index = True, unique = False)
    time = db.Column(db.String, index = True, unique = False)
    T_shed2_l = db.Column(db.Float, index=True)
    T_shed2_r = db.Column(db.Float, index=True)
    T_shed3_l = db.Column(db.Float, index=True)
    T_shed3_r = db.Column(db.Float, index=True)
    Gas_analyzer_shed2 = db.Column(db.Float, index=True)
    Gas_analyzer_shed3 = db.Column(db.Float, index=True)
    T_shed2_cold = db.Column(db.Float, index=True)
    T_shed2_hot = db.Column(db.Float, index=True)
    T_shed3_cold = db.Column(db.Float, index=True)
    T_shed3_hot = db.Column(db.Float, index=True)
    T_main_hot = db.Column(db.Float, index=True)
    T_main_cold = db.Column(db.Float, index=True)
    T_shed1_cold = db.Column(db.Float, index=True)
    T_shed1_hot = db.Column(db.Float, index=True)
    Flowmeter_shed3_hot = db.Column(db.Float, index=True)
    Request_shed3 = db.Column(db.Float, index=True)
    Flowmeter_shed3_cold = db.Column(db.Float, index=True)
    Flowmeter_shed2_hot = db.Column(db.Float, index=True)
    Request_shed2 = db.Column(db.Float, index=True)
    Flowmeter_shed2_cold = db.Column(db.Float, index=True)
    Flowmeter_main_hot = db.Column(db.Float, index=True)
    Exhaust_airflow_confirmed = db.Column(db.Float, index=True)
    Flowmeter_main_cold = db.Column(db.Float, index=True)
    Flowmeter_shed1_cold = db.Column(db.Float, index=True)
    Request_shed1 = db.Column(db.Float, index=True)
    Flowmeter_shed1_hot = db.Column(db.Float, index=True)
    Alarm_shed1 = db.Column(db.Float, index=True)
    Valve_shed3_hot = db.Column(db.Float, index=True)
    Valve_shed3_cold = db.Column(db.Float, index=True)
    Valve_shed2_hot = db.Column(db.Float, index=True)
    Valve_shed2_cold = db.Column(db.Float, index=True)
    Valve_main_hot = db.Column(db.Float, index=True)
    Valve_main_cold = db.Column(db.Float, index=True)
    Valve_shed1_cold = db.Column(db.Float, index=True)
    Valve_shed1_hot = db.Column(db.Float, index=True)
    Pump_shed3_hot = db.Column(db.Float, index=True)
    Pump_shed3_cold = db.Column(db.Float, index=True)
    Pump_shed2_hot = db.Column(db.Float, index=True)
    Pump_shed2_cold = db.Column(db.Float, index=True)
    Pump_main_hot = db.Column(db.Float, index=True)
    Pump_main_cold = db.Column(db.Float, index=True)
    Pump_shed1_cold = db.Column(db.Float, index=True)
    Pump_shed1_hot = db.Column(db.Float, index=True)
    Door_shed2_seal = db.Column(db.Float, index=True)
    Exhaust_shed2 = db.Column(db.Float, index=True)
    Request_good_shed1 = db.Column(db.Float, index=True)
    Request_good_shed2 = db.Column(db.Float, index=True)
    Request_good_shed3 = db.Column(db.Float, index=True)
    Door_shed3_seal = db.Column(db.Float, index=True)
    Exhaust_shed3 = db.Column(db.Float, index=True)
    Exhaust_damper = db.Column(db.Float, index=True)
    Exhaust_fan = db.Column(db.Float, index=True)

class EngData(db.Model):  # add columns for data model here
    id = db.Column(db.Integer, primary_key=True)  # primary key column if needed
    timestamp = db.Column(db.DateTime, index=True, primary_key=False, unique=True)  # timestamp
    chart_time = db.Column(db.String, index=True, unique=False)
    year = db.Column(db.Integer, index = True, unique = False)
    month = db.Column(db.Integer, index = True, unique = False)
    day = db.Column(db.Integer, index = True, unique = False)
    time = db.Column(db.String, index = True, unique = False)
    T_shed2 = db.Column(db.Float, index=True)
    T_shed3 = db.Column(db.Float, index=True)
    T_shed2_l = db.Column(db.Float, index=True)
    T_shed2_r = db.Column(db.Float, index=True)
    T_shed3_l = db.Column(db.Float, index=True)
    T_shed3_r = db.Column(db.Float, index=True)
    Gas_analyzer_shed2 = db.Column(db.Float, index=True)
    Gas_analyzer_shed3 = db.Column(db.Float, index=True)
    T_shed2_cold = db.Column(db.Float, index=True)
    T_shed2_hot = db.Column(db.Float, index=True)
    T_shed3_cold = db.Column(db.Float, index=True)
    T_shed3_hot = db.Column(db.Float, index=True)
    T_main_hot = db.Column(db.Float, index=True)
    T_main_cold = db.Column(db.Float, index=True)
    T_shed1_cold = db.Column(db.Float, index=True)
    T_shed1_hot = db.Column(db.Float, index=True)
    Flowmeter_shed3_hot = db.Column(db.Float, index=True)
    Request_shed3 = db.Column(db.Float, index=True)
    Flowmeter_shed3_cold = db.Column(db.Float, index=True)
    Flowmeter_shed2_hot = db.Column(db.Float, index=True)
    Request_shed2 = db.Column(db.Float, index=True)
    Flowmeter_shed2_cold = db.Column(db.Float, index=True)
    Flowmeter_main_hot = db.Column(db.Float, index=True)
    Exhaust_airflow_confirmed = db.Column(db.Float, index=True)
    Flowmeter_main_cold = db.Column(db.Float, index=True)
    Flowmeter_shed1_cold = db.Column(db.Float, index=True)
    Request_shed1 = db.Column(db.Float, index=True)
    Flowmeter_shed1_hot = db.Column(db.Float, index=True)
    Alarm_shed1 = db.Column(db.Float, index=True)
    Valve_shed3_hot = db.Column(db.Float, index=True)
    Valve_shed3_cold = db.Column(db.Float, index=True)
    Valve_shed2_hot = db.Column(db.Float, index=True)
    Valve_shed2_cold = db.Column(db.Float, index=True)
    Valve_main_hot = db.Column(db.Float, index=True)
    Valve_main_cold = db.Column(db.Float, index=True)
    Valve_shed1_cold = db.Column(db.Float, index=True)
    Valve_shed1_hot = db.Column(db.Float, index=True)
    Pump_shed3_hot = db.Column(db.Float, index=True)
    Pump_shed3_cold = db.Column(db.Float, index=True)
    Pump_shed2_hot = db.Column(db.Float, index=True)
    Pump_shed2_cold = db.Column(db.Float, index=True)
    Pump_main_hot = db.Column(db.Float, index=True)
    Pump_main_cold = db.Column(db.Float, index=True)
    Pump_shed1_cold = db.Column(db.Float, index=True)
    Pump_shed1_hot = db.Column(db.Float, index=True)
    Door_shed2_seal = db.Column(db.Float, index=True)
    Exhaust_shed2 = db.Column(db.Float, index=True)
    Request_good_shed1 = db.Column(db.Float, index=True)
    Request_good_shed2 = db.Column(db.Float, index=True)
    Request_good_shed3 = db.Column(db.Float, index=True)
    Door_shed3_seal = db.Column(db.Float, index=True)
    Exhaust_shed3 = db.Column(db.Float, index=True)
    Exhaust_damper = db.Column(db.Float, index=True)
    Exhaust_fan = db.Column(db.Float, index=True)




def save_data(raw_dictionary, eng_dictionary):
    raw_dict = {}
    eng_dict= {}

    for key, value in raw_dictionary.items():
        if "Placeholder" in key:
            pass
        else:
            raw_dict[key] = value
    for key,value in eng_dictionary.items():
        if "Placeholder" in key:
            pass
        else:
            eng_dict[key] = value

    

    print(eng_dict)
    data = RawData(**raw_dict )
    data2 = EngData(**eng_dict)
    data3 = SoakData()
    db.create_all()
    db.session.add(data)
    db.session.add(data2)
    db.session.add(data3)
  
    #print(db)
    db.session.commit()
    print('Data successfully commited to database')
    # try:
    #     db.session.commit()
    #     print('Data successfully commited to database')

    # except:
    #     db.session.rollback()
    #     print("Error recording data to database!")