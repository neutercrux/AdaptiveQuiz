import pymongo
from pprint import pprint
import json
from bson import json_util

mongo_client = pymongo.MongoClient('localhost', 27017)
mongo_db = mongo_client['WT']
collection_name = 'GK'
data = mongo_db[collection_name]

'''
Request containing category + factors ( answers + time(?) )
First response 5 easy questions
Next request has category and factors
Factors -> get score function -> returns 3 numbers
3 numbers -> subset questions -> send questions back
'''

def find_score(): #factors
	#calculate e,m,h
	questions = qsubset(e,m,h)
	return questions

'''
def run_quiz(questions):
	score = 0
	for question in questions:
		answer = input(question.prompt)
		if answer == question.answer:
			score += 1
	print("you got", score, "out of", len(questions))
'''

def qsubset(e,m,h):
	easy = list(data.find({'difficulty' : "easy" }).limit(e))
	medium = data.find({ 'difficulty' : "medium" }).limit(m)
	hard = data.find({ 'difficulty' : "hard" }).limit(h)
	
	json_data = [json.dumps(doc,default=json_util.default) for doc in easy]
	json_data += [json.dumps(doc,default=json_util.default) for doc in medium]
	json_data += [json.dumps(doc,default=json_util.default) for doc in hard]
	print(json_data)
	# return questions
qsubset(2,1,1)
