from flask import flask, render_template, request, url_for,redirect, session
from flask_session import Session
from os import path
import datetime

from array import *

import random
import sqlite3
import jsonify

app = flask(__name__)

app.secret_key = 'any random string'
db_locale = 'quizquestion.db'
user = {}

app.config["Session_PERMENANT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
question = []
answer = []

if not path.exists(db_locale):
  db_locale = db_locale
  con = sqlite3.connect(db_locale)
  command = con.cursor()

  command.execute("""CREATE TABLE IF NOT EXSISTS user("userID" INTEGER, "username" TEXT, "password" TEXT, "User Name" TEXT, "yeargroupcode"	INTEGER,
	"newteacher"	TEXT PRIMARY KEY("UserID", AUTOINCREMENT)) ); """)
  con.commit()

  command.execute("""CREATE TABLE IF NOT EXSISTS answer("answerID" INTEGER, "answer" TEXT) PRIMARY KEY("answerID", AUTOINCREMENT) ); """)
  con.commit()

  command.execute("""CREATE TABLE IF NOT EXSISTS teacher(
	"teacherID"	INTEGER,
	"yeargroup"	INTEGER,
	"yeargroupID"	INTEGER,
	PRIMARY KEY("teacherID")
);""")
  con.commit()

  command.execute("""CREATE TABLE IF NOT EXSISTS quiz(
	"quizID"	INTEGER,
	"userID"	INTEGER,
	"date"	TEXT,
	PRIMARY KEY("quizID"));""")
  con.commit()

  command.execute("""CREATE TABLE IF NOT EXSISTS quizquestion(
	"quizID"	INTEGER,
	"questionID"	INTEGER,
	"score"	INTEGER,
	PRIMARY KEY("questionID","quizID")
);""")
  con.commit()

  command.execute("""CREATE TABLE IF NOT EXSISTS question(
	"questionID"	INTEGER,
	"question"	TEXT,
	"points"	BLOB,
	"answerID"	INTEGER,
	PRIMARY KEY("questionID" AUTOINCREMENT)
);""")
  con.commit()

@app.route('/', methods=['GET','POST'])
def index():
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  command.execute("""SELECT username, password, userID FROM user""")
  invaliduser = True
  errormessage = None

  for x in command.fetchall():
    user1=str(x[0])
    pass1=str(x[1])

    
    if request.method == 'POST':
      if request.form['username'] == user1 and request.form['password'] == pass1:
        test = request.form['username']
        invaliduser = False
        print(user1)
        print(test)
        con.close()
        return render_template('AddUser.html')

  if invaliduser == True:
    errormessage = "Invalid Data, please try again"
    return render_template('index.html', errormessage = errormessage)
    return render_template("index.html")

@app.route('/AddUser', methods=['GET', 'POST'])
def AddUser():
  if request.method == "GET":
    return render_template('AddUser.html',)
  else:
    userdetails = (request.form['User Name'], request.form['userID'], request.form['username'], request.form['password'])
    insert(userdetails)
  return redirect(url_for(Menu)

def LoadData:
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  command.execute("""SELECT userID,User Name,username, password FROM user""")
  data = command.fetchall()
  return data

def insert(userdetails):
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  print(userdetails)
  sqlstring = """INSERT INTO user(User Name, username, password) VALUES (?,?,?,?)"""
  command.execute(sqlstring, userdetails)
  con.commit()
  con.close()

@app.route('/update', methods=['GET', 'POST'])
def update():
  if request.method == "GET":
    passingdata = loaddata()
    return render_template('update.html', passingdata=passingdata)
  else:
   updateuserfirstname = (request.form['firstname'])
   updateuserlastname = (request.form['lastname'])
   updateuserID = (request.form['IDDropdown'])
   print(updateuserfirstname, updateuserlastname, updateuserID)
   return render_template('index.html')

def LoadQuestion():
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  command.execute("""SELECT COUNT(question) FROM question""")
  countquestions = command.fetchone()[0]
  print(countquestions)

  newquestion = random.randint(1,countquestions)
  Session["questionID"] = newquestion
  print("Ww" , newquestion)
  sqlstring = """SELECT question, answer.answer FROM question INNER JOIN answer on question.answerID where questionID = ?"""
  command.execute(sqlstring,newquestion)
  data = command.fetchall()
  print("Question", data)
  return data

def GetGameID():
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  command.execute("""SELECT COUNT(gameID) FROM game""")
  GetGameID = command.fetchone()[0]
  print(GetGameID)
  return GetGameID

def InsertGameData(GetGameID):
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  sqlstring = """INSERT INTO user(userID,username,password,User Name, yeargroupcode,newteacher) VALUES (?,?,?,?,?,?)"""
  command.execute(sqlstring, GetGameID,Session.get("userID"),0)
  con.commit()
  con.close()

def CreateQuiz():
  con=sqlite3.connect(db_locale)
  command = con.cursor()
  TodaysDate = datetime.today().strftime('%d-%m-%y')
  sqlstring = """INSERT INTO quiz (quizID,userID,date) VALUES (?,?,?) """
  QuizDetails = int(Session["userID"]), TodaysDate, 0

  command.execute(sqlstring,QuizDetails)
  Session["GetGameID"] = command.fetchone[0]

  con.commit()
  con.close()

def CheckAnswer():
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  command.execute ("""SELECT question, answer.answer, score FROM question INNER JOIN answer ON question.answerID = answer.answerID WHERE questionID = %d"""% Session.get("questionID"))

  for x in command.fetchall():
   if request.form['answer'] == x[1]:
     sqlstring = """INSERT INTO link (gameID, questionID, myanswer, point) VALUES (?,?,?,?)""
     QuestionAnswer = Session["GetGameID"], Session["questionID"], request.form['answer'], 0
     command.execute(sqlstring, QuestionAnswer)

     con.commit()
     con.close()
    
def LoadUserDetails():
  UserID1 = int(Session.get('UserID'))
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  sqlstring = """SELECT user.userID, user.UserName from user where user.userID = '%d'"""(UserID1)
  command.execute(sqlstring)
  data = command.fetchall()
  return data

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
  if request.method == 'GET':
    count = 0
    session["count"] = count
    while count != 10:
      LoadQuestion1 = LoadQuestion()
  
  return render_template('quiz.html', LoadQuestion1 = LoadQuestion1, count = str(Session.get("count")))

  con = sqlite3.connect(db_locale)
  command = con.cursor()

  command.execute("""SELECT DISTINCT question.question, link.myanswer, answer.answer, link.points from quiz 
  INNER JOIN link ON quiz.quizID = link.quizID 
  INNER JOIN
  INNER JOIN 
  """)
  scores = command.fetchall()
  print("Scores", scores)

  command.execute("""SELECT 
  
  
  """)
  for x in command.fetchall():
    totalscore = x[0]
    Score = x[1]

  command.execute("UPDATE ")

  return render_template

  

  if request.method == 'POST':
    count = session["count"]

    while count < 10:
      session["count"] = count + 1
      LoadQuestion1 = LoadQuestion()
      question.append(LoadQuestion1)
      answer.append(request.form["count"])
      return render_template('quiz.html', LoadQuestion1 = LoadQuestion1, count = str(session.get("count")))

  if count == 10:
    correct = []
    print("QQ", str(question))
    answer.append(request.form["answer"])

    print("A", answer)

    for i in range(0,count+1):
      print("B", answer[i])
      print("C", question[i][0][1])
      if answer[i] == question[i][0][1]:
        print("correct")
        answer = question[i][0][0]+ "," + question[i][0][1] + "," + answer[i] + "," + "Correct"
        correct.insert(i, answer)

      else:
        print("Incorrect")
        answer = question[i][0][0]+ "," + question[i][0][1] + "," + answer[i] + "," + "Incorrect"
        correct.insert(i,answer)
        print("Question!!!", answer[i], question[i][0][1])
        print("cc" + str(correct))
    return render_template('ShowScores.html', answer = answer, question = question, correct = correct)
    print("cc" + correct)

@app.route('/showscore', methods=['GET', 'POST'])
def showscore():
  if request.method == 'GET':
   return render_template('Showscore.html')
    
@app.route('/sorting', methods=['GET','POST'])
def sorting():
  passingdata= InsertionSort()
  return render_template('sorting.html', passingdata = passingdata)

@app.route('/UserMenu', methods=['GET', 'POST'])
def UserMenu():
  session['error'] = ""
  firstName = session["firstname"]
  return render_template('UserMenu.html', user = firstName)

@app.route('/AdminMenu', methods=['GET','POST'])
def AdminMenu():
  session['error'] = ""
  firstname = session["firstname"]
  return render_template('AdminMenu.html', user = firstname)

@app.route('/delete', methods=['GET','POST'])
def delete():
    deleteuserinfo = (request.form['userID'])
    deleteuserdata(deleteuserinfo)
    return redirect('https://replit.com/@2022-2024-CS/Final-Flask-Coursework-IzzyMorton1#templates/delete.html')

def deleteuserdata(deleteuserinfo):
  print(deleteuserinfo)
  con = sqlite3.connect(db_locale)
  command = con.cursor()
  sqlstring = """DELETE FROM user Where userID= """
  command.execute(sqlstring, deleteuserinfo)
  con.commit()
  con.close()

con = sqlite3.connect(db_locale)

if __name__ == "__main__":
  app.run(host='0.0.0.0' , port=random.randint(2000,9000))