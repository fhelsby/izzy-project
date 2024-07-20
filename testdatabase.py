
from flask import Flask, render_template, request, url_for,redirect,g, jsonify
from flask_session import Session
from os import path
import datetime

import sqlite3

db = sqlite3.connect(':memory:', check_same_thread= False)
cursor = db.cursor()
cursor.execute("""CREATE TABLE user (
               userID INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT,
               password TEXT,
               yeargroupcode INTEGER,
               newteacher TEXT
               ); """)
db.commit()

cursor.execute("""CREATE TABLE answer (
               answerID INTEGER PRIMARY KEY AUTOINCREMENT,
               answer TEXT
               ); """)
db.commit()

cursor.execute("""CREATE TABLE teacher (
               teacherID	INTEGER PRIMARY KEY,
               yeargroup	INTEGER,
               yeargroupID INTEGER
               );""")
db.commit()

cursor.execute("""CREATE TABLE quiz (
               quizID	INTEGER PRIMARY KEY,
               userID	INTEGER,
               date TEXT
               );""")
db.commit()

cursor.execute("""CREATE TABLE quizquestion (
               quizID	INTEGER,
               questionID	INTEGER,
               score INTEGER,
               PRIMARY KEY(questionID,quizID)
               );""")
db.commit()

cursor.execute("""CREATE TABLE question (
               questionID INTEGER PRIMARY KEY AUTOINCREMENT,
               question TEXT,
               points BLOB,
               answerID INTEGER
               );""")
db.commit()

def get_db_connection():
  return db
