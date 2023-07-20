from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("froshims.db", check_same_thread=False) # creating a connection object of the database
cur = con.cursor() # creating a cursor

cur.execute("CREATE TABLE IF NOT EXISTS registrants(id INTEGER PRIMARY KEY, \
            name TEXT NOT NULL, sport TEXT NOT NULL)")

SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate frisbee"
    ]
@app.route("/")
def index():
    return render_template("index.html", sports = SPORTS)

@app.route("/register", methods=["POST"])
def register():
    
    name = request.form.get("name")
    sport = request.form.get("sport")
    
    # validate submission
    if not name or sport not in SPORTS:
        return render_template("failure.html")
    
    # Remember registrants
    #cur.executemany is used for example: to store multiple rows of data 
    # cur.execute("INSERT INTO registrants VALUES(?, ?)", (name, sport))
    cur.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", (name, sport))
    con.commit()

    # confirm registration
    return redirect("/registrants") # redirect() redirects anywhere on the internet

@app.route("/registrants")
def registrants():
    REGISTRANTS = (cur.execute("SELECT * FROM registrants")).fetchall()
    return render_template("registrants.html", registrants=REGISTRANTS)

@app.route("/deregister", methods=["POST"])
def deregister():

    # Forget registrant
    id = request.form.get("id")
    if id:
        cur.execute("DELETE FROM registrants WHERE id = ?", [id])
        con.commit()
    return redirect("/registrants")