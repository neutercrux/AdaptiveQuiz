from flask import Flask,jsonify,request,session
import pymongo
from pprint import pprint
import json
from bson import json_util
from bson import ObjectId
from flask_cors import CORS, cross_origin
import chart 

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
        sess['total'] = 0
        sess['H'] = 10
        sess['D'] = 10
        sess['R'] = 0
        print(data)
        cursor = table.find(data)
        res = convertCursor(cursor)
        sess['id'] = res[0]['_id']
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
        data['total'] = 0
        data['correct'] = 0
        data['incorrect'] = 0
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
    total = sess['total']
    total = total+1
    sess['total'] = total
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

def nextDifficulty(x):
    global sess
    if x==1:
        d = sess['D']
        h = sess['H']
        r = sess['R']
        r = r+1
        sess['R'] = r
        l = sess['total']
        d = d + (2/l)
        sess['D'] = d
        sess['H'] = int(h+d)
        l = l+1 
        sess['total'] = l
        return "medium"
    else:
        d = sess['D']
        h = sess['H']
        l = sess['total']
        d = d - (2/l)
        sess['D'] = d
        sess['H'] = int(h+d)
        l = l+1 
        sess['total'] = l
        return "easy"

@app.route('/next',methods=['GET','POST'])
def next():
    global sess
    count = sess['total']
    uname = sess['username']
    subject = sess['subject']
    table = mongo_db[subject]
    if count<5:
        
        data = request.get_json()
        print(data)
        question = data['question']
        answer = data['answer']
        cursor = table.find({'question':question})
        db_question = convertCursor(cursor)
        # print(db_question)
        givenQues = sess['question']
        if answer==db_question[0]['correct_answer']:
            diff = nextDifficulty(1)
        else:
            diff = nextDifficulty(0)
        print('-----got difficulty as----',diff)
        ques = table.find({'difficulty':diff,'category':subject},{'_id':False})
        ques = convertCursor(ques)
        for q in ques:
            if q not in givenQues:
                resp = q
                givenQues.append(q)
                sess['question'] = givenQues
                break
        print('Found ques', resp)
        return jsonify(resp),200
    else:
        table = mongo_db['user']
        correct = sess['R']
        incorr = count-correct
        id = sess['id']
        print(correct,incorr,uname)
        x = table.update_one({'_id':ObjectId(id),'username':uname},{"$set":{'total':count,'correct':correct,'incorrect':incorr}})
        resp = {'message':'test over'}
        return jsonify(resp),204

if __name__ == "__main__":
    app.debug = True
    app.run()