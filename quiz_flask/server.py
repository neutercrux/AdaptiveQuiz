from flask import Flask,jsonify,request,session
import pymongo
from pprint import pprint
import json
from bson import json_util
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'
cors = CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

mongo_client = pymongo.MongoClient('localhost', 27017)
mongo_db = mongo_client['WT']

sess = {}

def convertCursor(info):
    data = []
    for x in info:
        data.append(x)
    return data	

@app.route('/login',methods=['GET','POST'])
def login():
    global sess
    if request.method=='POST':
        table = mongo_db['user']
        data = request.get_json()
        sess['username'] = data['username']
        print(data)
        cursor = table.find(data)
        res = convertCursor(cursor)
        if len(res)>0:
            resp = {'message' : 'Valid User'}
            resp = jsonify(resp)
            return resp,200
        else:
            resp = {'message' : 'Invalid User'}
            print(resp)
            return jsonify(resp),400
    else:
        resp = {'message' : 'method not allowed'}
        return resp,405


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        # uname = data['username']
        # pwd = data['password']
        email = data['email']
        table = mongo_db['user']
        cursor = table.find({'email':email})
        res = convertCursor(cursor)
        if(len(res)==0):
            val = table.insert(data)
            if(val):
                resp = {'message' : 'user registered successfully'}
                resp = jsonify(resp)
                return resp,200
            else:
                resp = {'message' : 'user registeration failed'}
                return jsonify(resp),400
        else:
            resp = {'message' : 'user exists'}
            return jsonify(resp),200
        
    if request.method == 'GET':
        resp = {'message' : 'method not allowed'}
        return jsonify(resp),405


@app.route('/questions/<subject>')
def questions(subject):
    global sess
    data = mongo_db[subject]
    sess['subject'] = subject
    # print(session['subject'])
    easy = data.find({'difficulty' : "easy" ,'category':subject},{'_id': False}).limit(1)
    json_data = convertCursor(easy)
    sess['question'] = json_data
    # medium = data.find({ 'difficulty' : "medium",'category':subject},{'_id': False}).limit(2)
    # hard = data.find({ 'difficulty' : "hard",'category':subject },{'_id': False}).limit(1)
    # json_data += convertCursor(medium)
    # json_data += convertCursor(hard)
    resp = jsonify(json_data)
    return resp,200

@app.route('/next',methods=['GET','POST'])
def next():
    global sess
    subject = sess['subject']
    table = mongo_db[subject]
    data = request.get_json()
    print(data)
    question = data['question']
    answer = data['answer']
    cursor = table.find({'question':question})
    db_question = convertCursor(cursor)
    print(db_question)
    if answer==db_question[0]['correct_answer']:
        resp = {'correct':True}
        return jsonify(resp),200
    else:
        resp = {'correct':False}
        return jsonify(resp),200

if __name__ == "__main__":
    app.debug = True
    app.run()