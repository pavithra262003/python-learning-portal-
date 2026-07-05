from flask import Flask, render_template, request, redirect, url_for,send_file,session
from google import genai
import sqlite3

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

client = genai.Client(api_key=os.getenv("GEMIMI_API_KEY"))

app = Flask(__name__)
app.secret_key = "pythonportal123"


@app.route("/")
def home():
    return render_template("index.html")


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

        return "Registration Successful!"

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    username=session.get("username","user")
    score=session.get("score",0)
    return render_template("dashboard.html",username=username,score=score)


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

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    score = None

    if request.method == "POST":
        score = 0

        answers = {
          "q1": "Guido van Rossum",
          "q2": "def",
          "q3": ".py",
          "q4": "#",
          "q5": "print()",
          "q6": "[]",
          "q7": "{}",
          "q8": "for",
          "q9": "Programming Language",
          "q10": "()"
        }

        for question, answer in answers.items():
           if request.form.get(question) == answer:
              score += 1

           if score is not None:
               session["score"]=score

    return render_template("quiz.html", score=score)


@app.route("/logout")
def logout():
    return redirect(url_for("home"))


@app.route("/certificate")
def certificate():
    username = session.get("username", "User")
    score = session.get("score", 0)

    doc = SimpleDocTemplate("certificate.pdf")
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Python Learning Portal</b>", styles["Title"]))
    story.append(Paragraph("Certificate of Completion", styles["Heading1"]))
    story.append(Paragraph(f"This certificate is proudly awarded to <b>{username}</b>", styles["Normal"]))
    story.append(Paragraph(f"Quiz Score: <b>{score}/10</b>", styles["Normal"]))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%d-%m-%Y')}", styles["Normal"]))

    doc.build(story)

    return send_file("certificate.pdf", as_attachment=True)
    

if __name__ == "__main__":
    app.run(debug=True)