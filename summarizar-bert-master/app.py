from summarizer import Summarizer
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
  
# creating the flask app 
app = Flask(__name__) 
# creating an API object 
api = Api(app) 

model = Summarizer()
  
# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class Summarizer1(Resource):
	def post(self):
		text=request.get_json() 
		result = model(text['text'], min_length=60)
		full  = ''.join(result)
		#print(full)
		return jsonify({'title: ': full})
  
  

  
# adding the defined resources along with their corresponding urls 
api.add_resource(Summarizer1, '/text') 
#api.add_resource(square, '/square/<int:num>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 