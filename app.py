from flask import Flask, request, jsonify # imported it into your file
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
   # after you create these go into  your shell and type py and from app import db          
guide_schema = GuideSchema()  #if have to query for one guide then i would use this 
guides_schema = GuideSchema(many=True) # if i have to query many guides then this 
#creating the api through an endpoint so that you can create a guide
# if you wanna create a new guide then in postman you put in /guide and youll be able to post with the https POST 
@app.route('/guide', methods=["POST"])
def add_guide():
    title = request.json['title']
    content = request.json['content']
    
    new_guide = Guide(title, content)  # instatiating a new guide in the new_guide variable 
    
    db.session.add(new_guide) # adding the log of the user logs into the server and logs out 
    db.session.commit() #opens a session and commited the data
    #create a variable to help query that table and get the new guide. id 
    guide = Guide.query.get(new_guide.id)
    # returns the guide schema on line 28 and returns it in json of the guide variable we just created
    return guide_schema.jsonify(guide)

# endpoint to query all guides

@app.route("/guides", methods=["GET"]) # get is the default value for methods
def get_guides():
    all_guides = Guide.query.all() # gets all the guides in the app
    result = guides_schema.dump(all_guides)
    return jsonify(result) # in earlier versions of flask you have to return jsonify(result.data), but they ahve updated that recently 

#endpoint for querying a single guide , gotta tell the guide which one to bring back 
@app.route("/guide/<id>", methods=["GET"])
def get_guide(id): # gets the guide by id and tells flask to look for <id>  and pull that all into the function
    # and in the function it grabs the gquery by id  and its called a slug aka url parameter and gets it and runs the guide schema and jsonifys it
    guide = Guide.query.get(id)
    return guide_schema.jsonify(guide)

#endpoint building a update action request in flask using the PUT request
@app.route("/guide/<id>", methods=["PUT"]) # same as the function above, but the methods Put means your gonna update it 
def guide_update(id):
    guide = Guide.query.get(id)
    title = request.json['title']
    content = request.json['content']
    #overriding the title and contents data
    guide.title = title
    guide.content = content
    #starting a new database session
    db.session.commit()
    
    return guide_schema.jsonify(guide)
#endpoint for deleting  records in the database
@app.route("/guide/<id>", methods=["DELETE"])
def guide_delete(id):
    guide = Guide.query.get(id)
    db.session.delete(guide)
    db.session.commit()
    # return guide_schema.jsonify(guide) this isnt reality you would just say and return a string to get back 
    return "The guide was succesfully deleted"








if __name__ == "__main__": # name is a protected variable thats always gonna equal __main__ 
    app.run(debug=True)
    # run the app and debug it will be equal to True you can also set the port byt port=4000 ,
    #if you want to , but just let flask decide that unless it needs to be specifically specified
    # if you take out debug=True it will turn into production mode, and warn you that its production mode git