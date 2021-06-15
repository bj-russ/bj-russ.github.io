"""
The soak app is designed to read from a DB file on the network and
"""

import app
from app import db
from datetime import datetime, timedelta
import sqlite3
import random
from flask_sqlalchemy import SQLAlchemy

id_count = 0
conn = sqlite3.connect("soakDB.sqlite")
# cur = conn.cursor()
# cur.execute(
#     "CREATE TABLE  rawData (id INTEGER, timestamp DateTime, T_shed2_l FLOAT, T_shed2_r FLOAT)"
    
# )
conn.close()


from db_save import SoakData

def make_data():
    data = {}
    timestamp = datetime.now()
    data["chart_time"] = timestamp.strftime("%m/%d %H:%M")
    data["timestamp"] = timestamp
    data["year"] = timestamp.year
    data["month"] = timestamp.month
    data["day"] = timestamp.day
    data["time"] = timestamp.strftime("%H:%M:%S")
    data["T_soak1"] = random.uniform(20,24)
    data["T_soak2"] = random.uniform(20,24)
    data["T_soak3"] = random.uniform(20,24)
    data["T_soak4"] = random.uniform(20,24)
    data["T_soak5"] = random.uniform(20,24)
    data["T_soak6"] = random.uniform(20,24)
    data["T_soak7"] = random.uniform(20,24)
    data["T_soak8"] = random.uniform(20,24)
    
    return data

 


    
dict = make_data()
data = SoakData(**dict)
def save_data():
    dict = make_data()
    data = SoakData(**dict)

    db.create_all()
    db.session.add(data)

    try:
        db.session.commit()
        print('Data successfully commited to database_______________________SOAK TEMPS')

    except:
        db.session.rollback()
        print("Error recording data to database!")  

def initialize_from_db(self):
    self.last_100 = SoakData.query.order_by(SoakData.timestamp.desc()).limit(100).all()
    
    for entry in self.last_100:
        entry.reverse()