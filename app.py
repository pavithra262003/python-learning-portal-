from flask import Flask, render_template, request, redirect, url_for,session
from google import genai
import sqlite3
import os


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = "pythonportal123"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"]=username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":    
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
          "INSERT INTO users (username, password) VALUES (?, ?)",
          (username, password)
    )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    username=session.get("username","user")
    score=session.get("score",0)
    return render_template("dashboard.html",username=username,score=score)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/applications")
def applications():
    return render_template("applications.html")


    @app.route("/oop")
def oop():
    return render_template("oop.html")


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    answer = ""

    if request.method == "POST":
        question = request.form["question"]

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question
        )

        answer = response.text

    return render_template("chatbot.html", answer=answer)


@app.route("/logout")
def logout():
    return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run(debug=True)