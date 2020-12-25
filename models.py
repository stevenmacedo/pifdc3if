from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sensor(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    temperature = db.Column(db.String(100)) 
    humidity = db.Column(db.String(100)) 
    pressure = db.Column(db.String(100)) 
    light = db.Column(db.String(100))  