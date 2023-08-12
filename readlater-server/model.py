from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



#region Data classes
class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary id 
    url = db.Column(db.String(200), nullable=False) # url data
    date = db.Column(db.DateTime, nullable=False)
    read_status = db.Column(db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return '<Url %s>' % self.url 

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary id 
    last_modified = db.Column(db.DateTime, nullable=False)
#endregion