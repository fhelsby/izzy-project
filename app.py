from flask import Flask, render_template, request, url_for,redirect,g, session, jsonify
#from flask_session import Session
from os import path
import datetime
from testdatabase import get_db_connection

from array import *

import random
import sqlite3
#import jsonify

app = Flask(__name__)

app.secret_key = 'any random string'
db_locale = 'quizquestion.db'
user = {}

app.config["Session_PERMENANT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
question = []
answer = []

def get_db():
  if 'db' not in g:
    g.db = get_db_connection()
  return g.db

if not path.exists(db_locale):
  db_locale = db_locale
  con = sqlite3.connect(db_locale)
  cursor = con.cursor()

  cursor.execute("""CREATE TABLE IF NOT EXISTS user (
                 userID INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT,
                 password TEXT,
                 yeargroupcode INTEGER,
                 newteacher TEXT
                 ); """)
  con.commit()

  cursor.execute("""CREATE TABLE IF NOT EXISTS answer (
                 answerID INTEGER PRIMARY KEY AUTOINCREMENT,
                 answer TEXT
                 ); """)
  con.commit()

  cursor.execute("""CREATE TABLE IF NOT EXISTS teacher (
                 teacherID	INTEGER PRIMARY KEY,
                 yeargroup	INTEGER,
                 yeargroupID INTEGER
                 );""")
  con.commit()

  cursor.execute("""CREATE TABLE IF NOT EXISTS quiz (
                 quizID	INTEGER PRIMARY KEY,
                 userID	INTEGER,
                 date TEXT
                 );""")
  con.commit()

  cursor.execute("""CREATE TABLE IF NOT EXISTS quizquestion (
                 quizID	INTEGER,
                 questionID	INTEGER,
                 score INTEGER,
                 PRIMARY KEY(questionID,quizID)
                 );""")
  con.commit()

  cursor.execute("""CREATE TABLE IF NOT EXISTS question (
                 questionID INTEGER PRIMARY KEY AUTOINCREMENT,
                 question TEXT,
                 points	BLOB,
                 answerID INTEGER
                 );""")
  con.commit()
  con.close()

@app.route('/', methods=['GET','POST'])
def index():
  #con = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  command.execute("""SELECT userID, username, password FROM user""")
  errormessage = None

  if request.method == 'POST':
    for row in command.fetchall():
      user=str(row[1])
      password=str(row[2])
      print(user)
      print(password)
      if request.form['username'] == user and request.form['password'] == password:
        #db.close() can't close connection when test database is used
        session['firstname'] = user
        return redirect(url_for('UserMenu'))
    errormessage = "Invalid Data, please try again"
    return render_template('index.html', errormessage = errormessage)
  else:
    return render_template("index.html")
  

@app.route('/AddUser', methods=['GET', 'POST'])
def AddUser():
  if request.method == "GET":
    return render_template('AddUser.html',)
  else:
    userdetails = (request.form['userID'], request.form['username'], request.form['password'])
    insert(userdetails)
    return redirect('/')

def LoadData():
  #db = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  command.execute("""SELECT userID,username, password FROM user""")
  data = command.fetchall()
  return data

def insert(userdetails):
  #con = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  print(userdetails)
  sqlstring = """INSERT INTO user(userID, username, password) VALUES (?,?,?)"""
  command.execute(sqlstring, userdetails)
  print(f'Number of rows inserted: {command.rowcount}')
  db.commit()
  #db.close()

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
  #db = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  command.execute("""SELECT COUNT(question) FROM question""")
  countquestions = command.fetchone()[0]
  print(countquestions)

  newquestion = random.randint(1,countquestions)
  session["questionID"] = newquestion
  print("Ww" , newquestion)
  sqlstring = """SELECT question, answer.answer FROM question INNER JOIN answer on question.answerID where questionID = ?"""
  command.execute(sqlstring,newquestion)
  data = command.fetchall()
  print("Question", data)
  return data

def GetGameID():
  #db = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  command.execute("""SELECT COUNT(gameID) FROM game""")
  GetGameID = command.fetchone()[0]
  print(GetGameID)
  return GetGameID

def InsertGameData(GetGameID):
  #db = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  sqlstring = """INSERT INTO user(userID,username,password,User Name, yeargroupcode,newteacher) VALUES (?,?,?,?,?,?)"""
  command.execute(sqlstring, GetGameID,session.get("userID"),0)
  db.commit()
  db.close()

def CreateQuiz():
  #db=sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  TodaysDate = datetime.today().strftime('%d-%m-%y')
  sqlstring = """INSERT INTO quiz (quizID,userID,date) VALUES (?,?,?) """
  QuizDetails = int(session["userID"]), TodaysDate, 0

  command.execute(sqlstring,QuizDetails)
  session["GetGameID"] = command.fetchone[0]

  db.commit()
  db.close()

def CheckAnswer():
  #db = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  command.execute ("""SELECT question, answer.answer, score FROM question INNER JOIN answer ON question.answerID = answer.answerID WHERE questionID = %d"""% Session.get("questionID"))

  for x in command.fetchall():
   if request.form['answer'] == x[1]:
     sqlstring = """INSERT INTO link (gameID, questionID, myanswer, point) VALUES (?,?,?,?)"""
     QuestionAnswer = session["GetGameID"], session["questionID"], request.form['answer'], 0
     command.execute(sqlstring, QuestionAnswer)

     db.commit()
     db.close()
    
def LoadUserDetails():
  UserID1 = int(session.get('UserID'))
  #con = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  sqlstring = """SELECT user.userID, user.UserName FROM user WHERE user.userID = '%d'""" % UserID1
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
  
  render_template('quiz.html', LoadQuestion1 = LoadQuestion1, count = str(session.get("count")))

  #con = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()

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

  #render_template

  

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
  #con = sqlite3.connect(db_locale)
  db = get_db()
  command = db.cursor()
  sqlstring = """DELETE FROM user Where userID= """
  command.execute(sqlstring, deleteuserinfo)
  db.commit()
  db.close()

#con = sqlite3.connect(db_locale)

if __name__ == "__main__":
  app.run(host='0.0.0.0' , port=random.randint(2000,9000))