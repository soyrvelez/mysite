
import os

from bson import ObjectId
from .models import Question
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client.polls
collection = db.polls_question

print('----Availiable Collections----')
for collection in db.list_collection_names():
    print('---> '+collection)
print('')
print('----Availiable Questions----')
all_questions = db.polls_question.find()
q_num = 1
for q in all_questions:
    print('Question number '+str(q_num)+': '+q['question_text']+' (Published on: '+str(q['pub_date'])+')')
    q_num += 1
print('')

new_q = {"question_text": "What's new?", "pub_date": datetime.now()}

does_new_q_exist_in_db = False

for q in db.polls_question.find():
    if q['question_text'] == new_q['question_text']:
        does_new_q_exist_in_db = True
        break
if not does_new_q_exist_in_db:
    db.polls_question.insert_one(new_q)
    print('New question added to the database!')
else:
    print('"'+new_q["question_text"]+'" already exists in the database!')
print('')

def update_question(question_id, new_question_text):
    db.polls_question.update_one({"_id": ObjectId(question_id)}, {"$set": {"question_text": new_question_text}})
    update_question_date(question_id, datetime.now())
    print('Question updated!')
    print('')

def delete_question(question_id):
    db.polls_question.delete_one({"_id": ObjectId(question_id)})
    print('Question deleted!')
    print('')

def search_question_by_complete_text(question_text):
    for q in db.polls_question.find():
        if q['question_text'] == question_text:
            print('Question found!')
            print('')
            return q
    print('Question not found!')
    print('')
    return None

def search_question_by_partial_text(question_text):
    for q in db.polls_question.find_all():
        if question_text in q['question_text']:
            print('Question found!')
            print('')
            return q
    print('Question not found!')
    print('')
    return None

def search_question_by_id(question_id):
    for q in db.polls_question.find():
        if str(q['_id']) == question_id:
            print('Question found!')
            print('')
            return q
    print('Question not found!')
    print('')
    return None

def search_question_by_date(pub_date):
    for q in db.polls_question.find():
        if q['pub_date'] == pub_date:
            print('Question found!')
            print('')
            return q
    print('Question not found!')
    print('')
    return None

def search_all_questions_in_date_range(start_date, end_date):
    for q in db.polls_question.find():
        if start_date <= q['pub_date'] <= end_date:
            print('Question found!')
            print('')
            return q
    print('Question not found!')
    print('')
    return None

def update_question_date(question_id, new_pub_date):
    db.polls_question.update_one({"_id": ObjectId(question_id)}, {"$set": {"pub_date": new_pub_date}})
    print('Question updated!')
    print('')














def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

