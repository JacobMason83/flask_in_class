from flask import Flask # imported it into your file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app =  Flask(__name__) #creating the instance of flask 

@app.route('/') # function decorator thats taking in the path, function that your running, and method is GET by default 
def hello():
    return 'Hey Flask'
# also could do  
# @app.route('/'):# you would make a templates folder for flask 
#     def home():
#         return render_template('index.html') #now you can run html in your python code 

if __name__ == "__main__": # name is a protected variable thats always gonna equal __main__ 
    app.run(debug=True) # run the app and debug it will be equal to True you can also set the port byt port=4000 ,
    #if you want to , but just let flask decide that unless it needs to be specifically specified
    # if you take out debug=True it will turn into production mode, and warn you that its production mode git