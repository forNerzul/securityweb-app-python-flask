from security_guard_app.config import db

class CheckIn (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='checkin', lazy=True)
    date = db.Column(db.DateTime, nullable=False)
    waypoint_id = db.Column(db.Integer, db.ForeignKey('waypoint.id'))
    

    def __init__(self, user_id, date, waypoint_id):
        self.user_id = user_id
        self.date = date
        self.waypoint_id = waypoint_id

    def add_checkin_to_db(self):
        db.session.add(self)
        db.session.commit()