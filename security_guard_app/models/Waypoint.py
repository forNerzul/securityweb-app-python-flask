from security_guard_app.config import db
import secrets

class Waypoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    qr_value = db.Column(db.String(100), nullable=True)
    checkins = db.relationship('CheckIn', backref='waypoint', lazy=True)

    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.qr_value = secrets.token_urlsafe(16)

    @classmethod
    def get_waypoint_by_qr_value(cls, qr_value):
        return db.session.query(cls).filter_by(qr_value=qr_value).first()
    
    def add_waypoint_to_db(self):
        db.session.add(self)
        db.session.commit() 
        