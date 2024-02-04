from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId

client = MongoClient(os.getenv('MONGO_URI'))
db = client['mysite']
print(db.list_collection_names())
print(db.polls_question.find_one())

# db.polls_question.insert_one({ 
#     'question_text': 'What database do we use for Django?',
#     'pub_date': datetime.now()
# })

# TODO Search by question_text
# TODO Search a question by a certain text
# TODO Search all question by one date
# TODO Update a question (pub_date -> needs to be set to current date)
# TODO Delete a question

print('searched question', db.polls_question.find_one({ '_id': ObjectId('65bb3ca9bef1212d861d3b2d') }))

does_new_q_exist_in_db = False

# for q in db.polls_question.find():
#     if q['question_text'] == new_q['question_text']:
#         does_new_q_exist_in_db = True
#         break
# if not does_new_q_exist_in_db:
#     db.polls_question.insert_one(new_q)
#     print('New question added to the database!')
# else:
#     print('Question already exists in the database!')
# print('')


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
