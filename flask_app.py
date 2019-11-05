# Python standard libraries
from nltk.chat.util import Chat, reflections
import json
import os, re
import requests
from fuzzywuzzy import fuzz
# Third party libraries
from flask import Flask, redirect, request, url_for, render_template,send_from_directory
app = Flask(__name__)

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today ?",]
    ],
    [
        r"(.*) fine, you ?",
        ["I am good.",]
    ],
     [
        r"(.*) your name ?",
        ["My name is Simba and I'm a chatbot",]
    ],
    [
        r"how are you ?",
        ["I'm doing good\nHow about You ?",]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind",]
    ],
    [
        r"i (.*) doing good",
        ["Nice to hear that","Alright :)",]
    ],
    [
        r"(.*) fine",
        ["Nice to hear that","Alright :)",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there",]
    ],
    [
        r"(.*) age?",
        ["I'm a computer program dude\nSeriously you are asking me this?",]
        
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]
        
    ],
    [
        r"(.*) created ?",
        ["Asad developed me. He is my boss.","top secret ;)",]
    ],
    [
        r"(.*) (location|city) ?",
        ['Dhaka, Bangladesh',]
    ],
    [
        r"where (.*) live ?",
        ['Dhaka, Bangladesh',]
    ],
    [
        r"what technology (.*) ?",
        ['I was developed using nltk chat library and flask.',]
    ],
    [
        r"(.*) (boss|asad) do ?",
        ['My boss is a data analyst. He is also expert in cyber security analysis.',]
    ],
    [
        r"how is weather in (.*)?",
        ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1"]
    ],
     [
        r"(.*) (asad|boss|asad's) experience ?",
        ["My boss have two years of experience on data science with python, web scraping, flask, php RESTful API and ajax"]
    ],
    [
        r"(.*) (asad|boss|asad's) (education|educational) ?",
        ["My boss is a computer science graduate from MIST, Bangladesh and pursuing M.Sc. in computer science in MIST."]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
[
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy ",]
    ],
    [
        r"(.*) (sports|game) ?",
        ["I'm a very big fan of Football",]
    ],
    [
        r"who (.*) sportsperson ?",
        ["Messy","Ronaldo","Roony"]
],
    [
        r"who (.*) (moviestar|actor)?",
        ["Brad Pitt"]
],
    [
        r"quit",
        ["BBye take care. See you soon :) ","It was nice talking to you. See you soon :)"]
],
]

with open('F:\Personal-site\simba\data\dictionary.txt') as f:
	lines = f.readlines()
f.close()
chat = Chat(pairs, reflections)


# def weather(msg):
# 	city=msg.split(',')[0]
# 	country=msg.split(',')[1]
# 	apikey="5eHASm1cPxSJvZG01nAWn3fIq4QXCtTs"
# 	url="http://dataservice.accuweather.com/locations/v1/regions?apikey="+apikey
# 	regions=json.loads(url.response)
# 	for region in regions:
# 		regId=region['ID']
# 		newurl="http://dataservice.accuweather.com/locations/v1/countries/"+str(regId)+"?apikey="+apikey
# 		countries=json.loads(newurl.response)
# 		for count in countries:
# 			if(country==count):
# 				countID= count["ID"]
# 				break
# 		cityurl="http://dataservice.accuweather.com/locations/v1/cities/"+str(countID)+"/search"

def casemaker(msg):
    return msg.lower()


def ans(msg):
    if ("what is" in msg ):
        msg=msg.replace("what is ","")
    elif("what's" in msg):
        msg= msg.replace("what's","")
    msg=msg.replace("?","")
    msg=msg.replace(" ","+")
	# terms= msg.split(" ")
	# if(terms[len(terms)-1]=="?"):
	# 	term=terms[len(terms)-2]
	# else:
	# 	term= terms[len(terms)-1]
    term=msg
    print "search term"+str(term)
    url="https://www.lexico.com/en/definition/"+str(term)
    resp=requests.get(url)
    cont= str(resp.content)
    print "Before an"
    an= re.search(r'<span class="ind">(.*?)?</span></p>', str(cont)).group(1)
    return str(an)



def reply(msg):
	maxm=0
	repl=""
	global lines
	for line in lines:
		parts=line.split(">>")
		rat= fuzz.ratio( parts[0], msg)
		if rat>maxm:
			maxm=rat
			repl=parts[1]


	return repl


def wiki(msg):
    typo=0
    if ("what is the" in msg ):
        typo=1
        msg=msg.replace("what is ","")
    elif("what's the" in msg):
        typo=2
        msg= msg.replace("what's ","")
    elif("who's" in msg):
        typo=3
        msg= msg.replace("who's ","")
    elif("who is" in msg):
        typo=4
        msg= msg.replace("who is ","")  

    msg=msg.replace("?","")
    msg= msg.strip()
    msg= " ".join(msg.split())
    words = msg.split(' ')
    whitelist = {'and', 'the', 'is', 'of'}
    capitalized = ' '.join([word.title() if word not in whitelist else word for word in words])
    capitalized=capitalized.replace(" ","_")
    print "link of capitalized"
    print capitalized
    wiki_url= "https://en.wikipedia.org/wiki/"+capitalized
    resp= requests.get(url)
    content= resp.content



def simba(msg):
    print "here"
    global chat
    print msg
    return chat.reply_modified(msg)

@app.route("/")
def index():
	return render_template('simba.html')

@app.route('/post',methods = ['POST', 'GET'])
def msg():
	try:
		message="null"
		if request.method == 'POST':
			 messagemix = str(request.form['msg'])
			 message=casemaker(messagemix)
			 msg=simba(message)
			 if ("what is" in message or "what's" in message) and (("your" not in message) and ("is the" not in message)):
			 	print "here going to ans"
			 	msg= ans(message)
             # elif("who is" in message or "who's" in message or "what is the" in message or "what's the" in message) and (("your" not in message)):
             #    print "wiki is going on"
             #    msg=wiki(message)


			 if msg==None:
			 	msg= reply(message)
			 return msg
	except:
		return "Sorry, that's beyond my knowledge"

if __name__ == "__main__":
    app.run(debug = True)