
import os
from datetime import datetime

from bson import ObjectId
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#imports for authentication
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from dotenv import load_dotenv
from pymongo import MongoClient

from .forms import ContactForm, NameForm
from .models import Choice, Question

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

""" def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question}) """

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = ["velez59@gmail.com"]
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect("/thanks/")
    else:
        form = ContactForm()

    return render(request, 'polls/contact.html', {'form': form})

def login_view(request):
    """How we login to our app"""
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username=u, password=p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(f'/user/{u}')
                else:
                    print(f'{u} - account has been disabled')
                    return HttpResponseRedirect('/login')
            else:
                print('The username and/or password is incorrect')
                return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/login')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', { 'form': form })
