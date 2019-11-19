from flask import Flask,jsonify,request,session
import pymongo
import json
from bson import json_util
from bson import ObjectId
from flask_cors import CORS, cross_origin
import plotly.graph_objects as go
import numpy as np         
import random
import math                

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
        sess['pre'] = 0
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
    sess['difficulty'] = ['easy']
    # medium = data.find({ 'difficulty' : "medium",'category':subject},{'_id': False}).limit(2)
    # hard = data.find({ 'difficulty' : "hard",'category':subject },{'_id': False}).limit(1)
    # json_data += convertCursor(medium)
    # json_data += convertCursor(hard)
    resp = jsonify(json_data)
    return resp,200

def nextDifficulty(x):
    global sess
    d = sess['D']
    pre = sess['pre']
    h = sess['H']
    l = sess['total']
    l = l+1
    sess['total'] = l
    if x==1: #correct answer
        r = sess['R']
        r = r+1
        sess['R'] = r
        d = d + (pre*10/l)
        if(d>=100):
            d = 99
        sess['D'] = d
        sess['H'] = int(h+d)
    else:
        d = d - (pre*10/l)
        if(d<0):
            d = 0
        sess['D'] = d
        sess['H'] = int(h+d)
    return getDifficulty(d)

def getDifficulty(x):
    global sess
    print("x is ",x)
    rng = int(random.uniform(0,100))
    print("rng is ",rng)
    x = int(x/10)*10
    if(x<50):
        if(rng<(100-(2*x))):
            sess['pre'] = 3
            return "easy"
        else:
            sess['pre'] = 6
            return "medium"
    else:
        if(rng<(100-(2*(x-50)))):
            sess['pre'] = 6
            return "medium"
        else:
            sess['pre'] = 9
            return "hard"

@app.route('/next',methods=['GET','POST'])
def next():
    global sess
    count = sess['total']
    uname = sess['username']
    subject = sess['subject']
    table = mongo_db[subject]
    if count<20:
        
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
        prevDiff = sess['difficulty']
        prevDiff.append(diff)
        sess['difficulty'] = prevDiff
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
        print('---here-----')
        table = mongo_db['user']
        correct = sess['R']
        incorr = count-correct
        id = sess['id']
        print(correct,incorr,uname)
        x = table.update_one({'_id':ObjectId(id),'username':uname},{"$set":{'total':count,'correct':correct,'incorrect':incorr}})
        resp = {'username':uname}
        return jsonify(resp),202

@app.route('/results/<username>')
def results(username):
    global sess
    user = mongo_db['user']
    data = user.find({},{'_id': False})
    data = convertCursor(data)
    bar1 = {}
    correct_y = []
    incorrect_y = []
    others_correct = 0
    others_incorrect = 0
    count = 0
    for i in data:
        if i['username']==username:
            bar1 = i
            correct_y.append(i['correct'])
            incorrect_y.append(i['incorrect'])
        else:
            count += 1
            others_correct += i['correct']
            others_incorrect += i['incorrect']
    others_correct /= count
    others_incorrect /= count
    print(others_correct,others_incorrect)
    correct_y.append(others_correct)
    incorrect_y.append(others_incorrect)
    print(correct_y)
    print(incorrect_y)
    users=['You', 'Others']

    fig = go.Figure(data=[
        go.Bar(name='Correct', x=users, y=correct_y,opacity=0.8),
        go.Bar(name='Incorrect', x=users, y=incorrect_y,opacity=0.8)
        ])
    # Change the bar mode
    fig.update_layout(barmode='stack',
                      width=500,
                      height=500,
                      xaxis=dict(showgrid=False, zeroline=False),
                      yaxis=go.layout.YAxis(
                        title_text="Questions",
                        tickvals=[2,4,6,8,10,12,14,16,18,20],
                        tickmode="array",
                        titlefont=dict(size=20),
                        showgrid = False,
                        zeroline = False,
    ))
    fig.write_image("../frontend/src/assets/fig1.png")

    x = np.arange(int(sess['total']))
    diff = sess['difficulty']
    y = []

    for i in diff:
        if i=='easy':
            y.append(1)
        elif i=='medium':
            y.append(2)
        else:
            y.append(3)
    
    layout = go.Layout(
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis = go.layout.YAxis(
        tickmode = 'array',
        tickvals = [1, 2, 3],
        ticktext = ['Easy', 'Medium', 'Hard'],
        showgrid = False,
        zeroline = False
        )
    )
    fig1 = go.Figure(data=go.Scatter(x=x, y=y,marker_color='rgba(255, 0, 0, .7)'),layout=layout,)
    fig1.update_layout(width=500,
                      height=500,
                    xaxis_title='Questions',
                   yaxis_title='Difficulty level')
    fig1.write_image("../frontend/src/assets/fig2.png")
    z = 0
    while(z<10000000):
        z += 1
    resp = [
        {'src' : 'assets/fig1.png'},
        {'src' : 'assets/fig2.png'}
    ]
    return jsonify(resp),200

if __name__ == "__main__":
    app.debug = True
    app.run()