from flask import Flask
import pymongo
from pprint import pprint
import json
from bson import json_util

app = Flask(__name__)

@app.route('/questions/<subject>')
def questions(e,m,h):
    easy = list(data.find({'difficulty' : "easy" }).limit(e))
	medium = data.find({ 'difficulty' : "medium" }).limit(m)
	hard = data.find({ 'difficulty' : "hard" }).limit(h)
	
	json_data = [json.dumps(doc,default=json_util.default) for doc in easy]
	json_data += [json.dumps(doc,default=json_util.default) for doc in medium]
	json_data += [json.dumps(doc,default=json_util.default) for doc in hard]
	print(json_data)
    return json_data


if __name__ == "__main__":
    app.debug = False
    app.run()