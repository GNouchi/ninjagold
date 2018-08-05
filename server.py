from flask import Flask, render_template, request, redirect, session
app=Flask(__name__)
app.secret_key = "AD555C03B3B8892327A7D8E58F5BD133734A67CDEDDFAF600E86C7A3EBD2EBCC"
import random 
from datetime import datetime

@app.route('/')
def index():
# let randnum reset to nothing every redirect also prevents errors
    randnum = ''
# arr is actually not used much though it could auto generate buttons
    if 'arr' not in session:
        session['arr'] =[
            ["Farm","farm","(earns 10-20 gold)" ],
            ["Cave","cave","(earns 5-10 gold)" ],
            ["House","house", "(earns 2-5 gold)" ],
            ["Casino","casino","(lose/win -100/+50 gold)" ]
        ]
# if session does not have logged vars, init them here
    if 'gold' not in session:
        session['gold'] = 0
        session['broken']= 0
        session['log'] =[]
        session['loglen'] = 0

# return different text at header based on game
    if session['gold'] < -50:
        score = "<span class='score small small-only-expanded'> You lost! <i class='large material-icons'>announcement</i> Score less than -50</span>"
        session['broken'] = 1 
    else:
        score = "<span class='score small small-only-expanded'> Your gold is " + str(session['gold']) + "</span>"
        if 'randnum' in session: 
            randnum = "<span class='randnum small small-only-expanded'> Gold +" + str(session['randnum']) + "</span>"
    return render_template("index.html", score=score, randnum=randnum)

@app.route('/process_money', methods = ['POST'] )
def trees():
# let game break itself if negative
    if session['broken'] == 1:
        return redirect ('/')
    # print("************print request received and randnum************")
# roll logic
    for k in request.form:
        if k == 'farm':
            randnum = random.randrange(10,20)
            session['gold'] +=randnum            
        if k == 'cave':
            randnum = random.randrange(5,10)
            session['gold'] +=randnum            
        if k == 'house':
            randnum = random.randrange(2,5)
            session['gold'] +=randnum            
# allowing for a 50-50 chance of positive or negative numbers
        if k == 'casino':
            randnum = random.randrange(-50,50)
            session['gold'] +=randnum
    session['randnum'] = randnum
    if randnum >= 0:
        session['log'].append("<p class ='positive'>+"+str(randnum)+" gold from "+str(k)+ "  [ " + str(datetime.now())+ " ]</p>")
    elif randnum < 0:
        session['log'].append("<p class ='negative'> "+str(randnum)+" gold from "+str(k)+ "  [ " + str(datetime.now())+ " ]</p>")
    print("**********************************************************")
    return redirect('/')
@app.route('/reset', methods = ['POST'])
def reset():
    session.clear()
    print("******************Session Reset***************************")
    return redirect ('/')

if __name__=="__main__":
    app.run(debug=True)