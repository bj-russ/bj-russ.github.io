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
    # raw_dictionary = raw_dictionary
    # timestamp = datetime.now()
    # year = timestamp.year
    # month = timestamp.month
    # day = timestamp.day
    # time = timestamp.strftime("%H:%M:%S")
    # chart_time = timestamp.strftime("%m/%d %H:%M")
    # raw_dictionary = raw_dictionary
    # eng_dictionary = eng_dictionary
    # raw_dictionary["chart_time"] = chart_time
    # raw_dictionary["timestamp"] = timestamp
    # raw_dictionary["year"] = year
    # raw_dictionary["month"] = month
    # raw_dictionary["day"] = day
    # raw_dictionary["time"] = time
    # eng_dictionary["chart_time"] = chart_time
    # eng_dictionary["timestamp"] = timestamp
    # eng_dictionary["year"] = year
    # eng_dictionary["month"] = month
    # eng_dictionary["day"] = day
    # eng_dictionary["time"] = time
    # raw_dict = {raw_ + str(key):val for key,val in raw_dictionary.items()} #add prefix "raw_" to dictionary to separate from other dicts
    raw_dict = {}
    eng_dict= {}
    for k,v in raw_dictionary.items():
        if "Placeholder" in k:
            pass
        else:
            raw_dict[k] = v
    for k,v in eng_dictionary.items():
        if "Placeholder" in k:
            pass
        else:
            eng_dict[k] = v



    
    data = RawData(**raw_dict )
    data2 = EngData(**eng_dict)
    db.create_all()
    db.session.add(data)
    db.session.add(data2)
    #print(db)

    try:
        db.session.commit()
        print('Data successfully commited to database')

    except:
        db.session.rollback()
        print("Error recording data to database!")