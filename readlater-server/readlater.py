from blueprints import *
from flask import Flask
from flask_cors import CORS
from model import *
from waitress import serve

class ReadLater(Flask):
    def __init__(self):
        super(ReadLater,self).__init__(__name__, static_folder='static') 
        CORS(self)
        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
        db.init_app(self)
        
        self.register_blueprint(fetchers)
        self.register_blueprint(modifiers)
        
        # Get app context and create table schema defined above 
        with self.app_context():
            db.create_all()
            after_request(self.do_auth)
   
    def do_auth(self):
        # TODO: check auth
        pass
    
app = ReadLater()

if __name__ == '__main__':
    app = ReadLater()
    app.run(host="192.168.0.2",debug=True)
