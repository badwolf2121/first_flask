from flask import Flask
from markupsafe import escape
import random

app=Flask(__name__)

global player1_score
global player2_score


def rock_paper(player1,player2):
    print("these are the values",player1,player2)
    if (player1 =="rock" and player2=="scissor") or (player1=="scissor" and player2=="paper" ) or ( player1=="paper" and player2=="rock"):
        print("player 1 won this round")
        score=1
    elif (player2 =="rock" and player1=="scissor") or ( player2=="scissor" and player1=="paper")or (player2=="paper" and player1=="rock"):
        print("player 2 won this round")
        score=-1
    else:
        score=0
    return score

@app.route('/restart')
def play_restart():
    global player1_score,player2_score
    player1_score=0
    player2_score=0
    return "Score has been reset"






@app.route('/')
def root():
    return 'WORKING'


dict_try={"0":"rock","1":"paper","2":"scissor"}

@app.route('/play/<val>')
def play_game(val):
    global player1_score,player2_score

    # player 1 is computer  
    # player 2 is human

    # hand of computer
    player1=random.choice(["rock","paper","scissor"])

    #hand of human
    player2=val
    player2=dict_try[player2]

    print(" Player 1(Computer) tried ",player1)
    print(" Player 2(Human) tried ",player2)

    score=rock_paper(player1,player2)
    if score==1:
        player1_score+=1
    elif score==-1:
        player2_score+=1

    result_string=""
    result_string+="Player 1(Computer) tried "+player1
    result_string+="</br>Player 2(Human) tried "+player2
    

    result_string+="</br>player1(computer score) = "+str(player1_score)
    result_string+="</br>player2(human score) = "+str(player2_score)
    if player1_score ==3 :
        result_string+="</br> congratualtion computer has won"
        player1_score=0
        player2_score=0
    elif player2_score ==3:
         player2_score=0
         player1_score=0
         result_string+="</br> congratualtion you have won"
        
    return result_string

    


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

    data="dummy for "+str(lat)+ " " +str(lon)

    #response = requests.get(url)
    #data = json.loads(response.text)
    print(lat,lon)

    print(data)
    return data


if __name__ == '__main__':
    global player1_score,player2_score
    player1_score=0
    player2_score=0
    print("score till now,", player1_score,player2_score)
    app.run(host="0.0.0.0",debug=True)
    
