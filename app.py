from flask import Flask # imported it into your file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app =  Flask(__name__) #creating the instance of flask 

# @app.route('/') # function decorator thats taking in the path, function that your running, and method is GET by default 
# def hello():
#     return 'Hey Flask'
# also could do  
# @app.route('/'):# you would make a templates folder for flask 
#     def home():
#         return render_template('index.html') #now you can run html in your python code 
 
    
    #making the sql lite database. Look at it as a high level overview of it 
    # sql lite is a lightweight database, its not as invtesive as others
    # define the schema
    #each row is a record, each column is the data, and the table is the record and data as a whole
    
basedir = os.path.abspath(os.path.dirname(__file__)) #setting up the base directory
    #performing a lookup in the sql database , and the structure is the same with other databses like mongo etc
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'  + os.path.join(basedir, 'app.sqlite')     
db = SQLAlchemy(app)
ma = Marshmallow(app)
    
class Guide(db.Model):
        #primary key will make sure its always unique, id will auto increment
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), unique=False)
        content = db.Column(db.String(144), unique=False)
        # we did it this way so that the database is structured first then building up the custom data for each instance
        def __init__(self, title, content):
            self.title = title
            self.content = content
            
class GuideSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')
            
guide_schema = GuideSchema()  #if have to query for one guide then i would use this 
guides_schema = GuideSchema(many=True) # if i have to query many guides then this 








if __name__ == "__main__": # name is a protected variable thats always gonna equal __main__ 
    app.run(debug=True)
    # run the app and debug it will be equal to True you can also set the port byt port=4000 ,
    #if you want to , but just let flask decide that unless it needs to be specifically specified
    # if you take out debug=True it will turn into production mode, and warn you that its production mode git