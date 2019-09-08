import sqlite3 as sql
from flask import Flask, render_template, request, jsonify
from datetime import date
from datetime import time
from datetime import datetime
import aiml
import os


kernel = aiml.Kernel()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('welcome.html')


@app.route("/signup")
def signup():
    return render_template('register.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/admin")
def admin():
    return render_template('adminlogin.html')


@app.route('/admin_validate', methods=['POST', 'GET'])
def admin_validate():

    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']

        if email == "admin@gmail.com" and pwd == "admin@123":
            con = sql.connect("aidb.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select id,fname,lname,que_cnt from user_register1")
            rows = cur.fetchall();

            cur1 = con.cursor()
            cur1.execute("select fname from user_register1")
            rows1 = cur1.fetchall();

            cur2 = con.cursor()
            cur2.execute("select que_cnt from user_register1")
            rows2 = cur2.fetchall();



            return render_template("admin_dashboard.html", rows=rows,rows1=rows1,rows2=rows2)
        else:
            return render_template('adminlogin.html')


@app.route('/register_user', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        fn = request.form['fname']
        ln = request.form['lname']
        em = request.form['email']
        pa = request.form['pwd']
        qcnt=0
        with sql.connect("aidb.db") as con:
            cur = con.cursor()
            cur.execute("insert into user_register1(fname,lname,email,pwd,que_cnt) values(?,?,?,?,?)", (fn, ln, em, pa,qcnt))
            con.commit()

        return render_template("login.html")
    else:
        return render_template('register.html')


@app.route("/login_validate", methods=['POST', 'GET'])
def login_validate():
    if request.method == 'POST':
        file_session = open('current_user.txt', "w")
        em = request.form['email']
        pa = request.form['pwd']
        file_session.write(em)
        file_session.close()
        con = sql.connect("aidb.db")
        con.row_factory = sql.Row
        cur1 = con.cursor()
        cur1.execute('select que_cnt from user_register1 where email= ?', (em,))
        dbque_cnt = cur1.fetchone()
        cnt=int(dbque_cnt[0])
        cur = con.cursor()
        cur.execute('select * from user_register1 where email= ? and pwd = ?', (em, pa))
        rows = cur.fetchall();

        for row in rows:
            dbUser = row[3]
            dbPass = row[4]
            print(dbUser)
            print(dbPass)
            if dbUser == em and dbPass == pa:
                return render_template("chat.html",dbque_cnt=cnt)
            else:
                return render_template("login.html")
    return render_template("login.html")


def load_kern(forcereload):
    if os.path.isfile("bot_brain.brn") and not forcereload:
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"), commands="load aiml b")
        kernel.saveBrain("bot_brain.brn")


@app.route("/ask", methods=['POST', 'GET'])
def ask():
    file_session = open("current_user.txt", "r")
    current_email = file_session.readline()
    message = str(request.form['chatmessage'])
    totalquestion = int(request.form['totalquestion'])
    today = date.today();
    print(today)



    # with sql.connect("aidb.db") as con:
    #     cur1 = con.cursor()
    #     cur1.execute("select que_cnt from user_register1 where email= ?",(current_email,))
    #     row = cur1.fetchone()
    #     print(row)

    with sql.connect("aidb.db") as con:
        cur1 = con.cursor()
        cur1.execute("select que_cnt from user_register1 where email= ?", (current_email,))
        row = cur1.fetchone()
        totalquestion = (int(row[0]) + (totalquestion+(1-totalquestion)))
        cur = con.cursor()
        cur.execute("update user_register1 set que_cnt= ?,date= ? where email= ? ",(totalquestion,today,current_email))
        con.commit()
    print(totalquestion)
    if message == "save":
        kernel.saveBrain("bot_brain.brn")
        return jsonify({"status": "ok", "answer": "Brain Saved"})
    elif message == "reload":
        load_kern(True)
        return jsonify({"status": "ok", "answer": "Brain Reloaded"})
    elif message == "quit":
        exit()
        return jsonify({"status": "ok", "answer": "exit Thank You"})

    # kernel now ready for use
    else:
        # while True:
        bot_response = kernel.respond(message)
        print("hello")
        # print bot_response
        return jsonify({'status': 'OK', 'answer': bot_response})



@app.route('/list')
def list():
    con = sql.connect("aidb.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from user_register1")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


if __name__ == "__main__":
    load_kern(False)
    app.run(debug=True)
    # app.run(host='0.0.0.0')
