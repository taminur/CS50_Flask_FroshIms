from flask import Flask, request, render_template

app = Flask(__name__)

REGISTRANTS = {} # this variable will collect all the info those who are registered
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
    if not name: # this if added to avoid getting hacked
        return render_template("failure.html")
    sport = request.form.get("sport")
    if sport not in SPORTS: # this if added to avoid getting hacked
        return render_template("failure.html")
    REGISTRANTS[name] = sport
    return render_template("success.html")

@app.route("/registrants")
def registrants():
    return render_template("registrants.html", registrants=REGISTRANTS)
