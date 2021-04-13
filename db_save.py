from app import db
from datetime import datetime
import sqlite3

id_count = 0
conn = sqlite3.connect("new_DB.sqlite")
# cur = conn.cursor()
# cur.execute(
#     "CREATE TABLE  rawData (id INTEGER, timestamp DateTime, T_shed2_l FLOAT, T_shed2_r FLOAT)"
    
# )
conn.close()


class RawData(db.Model):  # add columns for data model here
    # id = db.Column(db.Integer, primary_key=True)  # primary key column if needed
    timestamp = db.Column(db.DateTime, index=True, primary_key=True, unique=True)  # timestamp
    T_shed2_l = db.Column(db.Float)
    T_shed2_r = db.Column(db.Float)
    T_shed3_l = db.Column(db.Float)
    T_shed3_r = db.Column(db.Float)
    Gas_analyzer_shed2 = db.Column(db.Float)
    Gas_analyzer_shed3 = db.Column(db.Float)
    # MVDN_Placeholder_7 = db.Column(db.Float)
    # MVDN_Placeholder_8 = db.Column(db.Float)
    T_shed2_cold = db.Column(db.Float)
    T_shed2_hot = db.Column(db.Float)
    T_shed3_cold = db.Column(db.Float)
    T_shed3_hot = db.Column(db.Float)
    T_main_hot = db.Column(db.Float)
    T_main_cold = db.Column(db.Float)
    T_shed1_cold = db.Column(db.Float)
    T_shed1_hot = db.Column(db.Float)
    Flowmeter_shed3_hot = db.Column(db.Float)
    Request_shed3 = db.Column(db.Float)
    Flowmeter_shed3_cold = db.Column(db.Float)
    Flowmeter_shed2_hot = db.Column(db.Float)
    Request_shed2 = db.Column(db.Float)
    Flowmeter_shed2_cold = db.Column(db.Float)
    Flowmeter_main_hot = db.Column(db.Float)
    Exhaust_airflow_confirmed = db.Column(db.Float)
    Flowmeter_main_cold = db.Column(db.Float)
    Flowmeter_shed1_cold = db.Column(db.Float)
    Request_shed1 = db.Column(db.Float)
    Flowmeter_shed1_hot = db.Column(db.Float)
    Alarm_shed1 = db.Column(db.Float)
    Valve_shed3_hot = db.Column(db.Float)
    Valve_shed3_cold = db.Column(db.Float)
    Valve_shed2_hot = db.Column(db.Float)
    Valve_shed2_cold = db.Column(db.Float)
    Valve_main_hot = db.Column(db.Float)
    Valve_main_cold = db.Column(db.Float)
    Valve_shed1_cold = db.Column(db.Float)
    Valve_shed1_hot = db.Column(db.Float)
    Pump_shed3_hot = db.Column(db.Float)
    Pump_shed3_cold = db.Column(db.Float)
    Pump_shed2_hot = db.Column(db.Float)
    Pump_shed2_cold = db.Column(db.Float)
    Pump_main_hot = db.Column(db.Float)
    Pump_main_cold = db.Column(db.Float)
    Pump_shed1_cold = db.Column(db.Float)
    Pump_shed1_hot = db.Column(db.Float)
    Door_shed2_seal = db.Column(db.Float)
    Exhaust_shed2 = db.Column(db.Float)
    Request_good_shed1 = db.Column(db.Float)
    Request_good_shed2 = db.Column(db.Float)
    Request_good_shed3 = db.Column(db.Float)
    Door_shed3_seal = db.Column(db.Float)
    Exhaust_shed3 = db.Column(db.Float)
    Exhaust_damper = db.Column(db.Float)
    Exhaust_fan = db.Column(db.Float)



def save_data(raw_dictionary):
    # raw_dictionary = raw_dictionary
    time = datetime.now()
    raw_dictionary = raw_dictionary
    raw_dictionary["timestamp"] = time
    # raw_dict = {raw_ + str(key):val for key,val in raw_dictionary.items()} #add prefix "raw_" to dictionary to separate from other dicts
    raw_dict = {}
    for k,v in raw_dictionary.items():
        if "Placeholder" in k:
            pass
        else:
            raw_dict[k] = v
        #  globals()[k]=v
        #  raw_klist.append(k)
        #  raw_vlist.append(str(v))
    print (raw_dict) 


    
    data = RawData(**raw_dict )
    db.create_all()
    db.session.add(data)
    print(db)

    try:
        db.session.commit()
        print('committed!')

    except:
        db.session.rollback()
        print("rollback!")