from flask import Flask, request, session, redirect, url_for
from markupsafe import escape
import random
import requests
from flask import render_template
import json

app=Flask(__name__)
app.secret_key = "key2"



def rock_paper(player1,player2):
    print("these are the values",player1,player2)
    if (player1 =="rock" and player2=="scissor") or (player1=="scissor" and player2=="paper" ) or ( player1=="paper" and player2=="rock"):
        print("player 1 won this round")
        score=1
    elif (player2 =="rock" and player1=="scissor") or ( player2=="scissor" and player1=="paper") or (player2=="paper" and player1=="rock"):
        print("player 2 won this round")
        score=-1
    else:
        score=0
    return score



dict_try={"0":"rock","1":"paper","2":"scissor"}

@app.route('/play/<val>')
def play_game(val):    
    print("Call for a try")
    if 'user_name' not in session:
        return redirect(url_for("login"))
    # player 1 is computer  
    # player 2 is human

    # hand of computer

    player1=random.choice(["rock","paper","scissor"])

    #hand of human
    player2=val
    player2=dict_try[player2]
    session["play_per_play"]["player1"].append(player1)
    session["play_per_play"]["player2"].append(player2)
    print(" Player 1(Computer) tried ",player1)
    print(" Player 2(Human) tried ",player2)
    print(session["play_per_play"]["player2"],session["play_per_play"]["player1"])

    result_string=""
    result_string+="player1       player2"
    for i in range (len(session["play_per_play"]["player1"])):
        prev_player1=session["play_per_play"]["player1"][i]
        prev_player2=session["play_per_play"]["player2"][i]  
        result_string+="</br>"+prev_player1+"      "+prev_player2
    result_string+="</br>____________________</br>"
    result_string+="Player 1(Computer) tried "+player1
    result_string+="</br>Player 2(Human) tried "+player2


    loc_score=rock_paper(player1,player2)
    print("score for ",player1,player2 ,"is ",str(loc_score))

    if loc_score==1:
        session["player1_score"]+=1
    elif loc_score==-1:
        session["player2_score"]+=1

    print("Current score for player 1",str(session["player1_score"]))
    print("Current score for player 2",str(session["player2_score"]))


    

    result_string+="</br>player1(computer score) = "+str(session["player1_score"])
    result_string+="</br>player2(human score) = "+str(session["player2_score"])
    if session["player1_score"] ==3 :
        result_string+="</br> congratualtion computer has won"
        session["player1_score"]=0
        session["player2_score"]=0
    elif session["player2_score"] ==3:
         session["player2_score"]=0
         session["player1_score"]=0
         result_string+="</br> congratualtion you have won"
        
    return result_string



@app.route('/restart')
def new_game():
    print("Restarting")     
    session.pop('player1_score',None)
    session.pop('player2_score',None)
    session.pop('play_per_play',None)
    session["player1_score"]=0
    session["player2_score"]=0
    session["play_per_play"]={}
    session["play_per_play"]["player1"]=[]
    session["play_per_play"]["player2"]=[]
    print("Scores are ",session["player1_score"],session["player2_score"])
    return "Score has been reset"






@app.route('/')
def root():
    return render_template("index.html")

@app.route('/login')
def login():
    if 'user_name' in session:
        return str(session["user_name"])+" Logged in already"
    else:
        return render_template("login.html")  
    # return 'WORKING'

@app.route('/logout')
def logout():
    session.pop('user_name',None)
    session.pop('player1_score',None)
    session.pop('player2_score',None)
    session.pop("play_per_play",None)
    return redirect(url_for("login"))

@app.route('/postlogin',methods=['POST'])
def postlogin():
    print("At logging in",request)
    user_name=request.form['username']
    session["user_name"] = user_name
    session['player1_score']=0 
    session['player2_score']=0 
    session["play_per_play"]={}
    session["play_per_play"]["player1"]=[]
    session["play_per_play"]["player2"]=[]
    print("Got username ",user_name)


    return str(session["user_name"])+" Logged in succesfully"





@app.route('/user/<username>')
def show_user(username):
    return "Hello "+str(username)


@app.route('/reverse/<word>')
def reverse_a(word):
    new_word=""
    for i in range (len(word)):
        index=(len(word)-1-i)
        print(index)
        new_word=new_word+(word[index])

    #new_word=str(new_word)
    print(new_word)        
    return new_word

@app.route('/weather/<lat>/<lon>')
def get_weather(lat,lon):
    api_key="55566d956a0f278fa9d74b1e7ab4d355"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

    # data="dummy for "+str(lat)+ " " +str(lon)

    response = requests.get(url)
    data = json.loads(response.text)
    print(lat,lon)
    results_string="Temperature is"
    results_string+= " "+str(data['current']['temp'])+"</br>"
    results_string+="Humidity is  "+ str(data['current']['humidity'])
    print(data['current']['temp'])
    print(data['current']['humidity'])
    return  results_string


if __name__ == '__main__':
    global player1_score,player2_score
    player1_score=0
    player2_score=0
    print("score till now,", player1_score,player2_score)
    app.run(host="0.0.0.0",debug=True)
    
