import bacon_app
import input_check
from flask import Flask, render_template, redirect, request, session
import sqlite3

# Configure flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'skeleton_key'


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", answer=0)
    else:
        session["confirmed_star"] = None
        star1 = request.form.get("star1")
        star2 = request.form.get("star2")
        solution = bacon_app.main_query(star1, star2)

        # In case inputs return more than one film star each
        # First block is for only one of the input returning more than one name
        if solution[0] == 7:
            to_be_checked = input_check.over_two_names(solution[1])
            if len(to_be_checked[0]) > 0:
                session["confirmed_star"] = to_be_checked[0]  # remembers input that won't need to be checked with user
                to_be_checked = to_be_checked[1]
                return render_template("check.html", check_list1=to_be_checked, check_list2=0)

            # If both inputs returned more than one name then split into two separate lists
            else:
                to_be_checked = to_be_checked[1]
                to_be_checked2 = []
                for i in to_be_checked:
                    if i[0] == to_be_checked[0][0]:
                        to_be_checked2.append(i)
                for i in to_be_checked2:
                    if i in to_be_checked:
                        to_be_checked.remove(i)
                print("checked 2:", to_be_checked2)
                print("checked 1:", to_be_checked)
                return render_template("check.html", check_list1=to_be_checked, check_list2=to_be_checked2)

        try:
            return render_template("index.html", answer=solution)
        except:
            return render_template("error.html")


@app.route("/check", methods=["GET", "POST"])
def check():
    if request.method == "GET":
        return render_template("index.html")

    else:
        db = sqlite3.connect('movies.db', check_same_thread=False)
        cursor = db.cursor()

        star1 = request.form.get("sel1")  # Recreating list object from form selection
        star1 = star1.split(",")

        # checks if both inputs had to be confirmed with user, if not one input will have been stored in session
        if session["confirmed_star"] is None:
            star2 = request.form.get("sel2")
            star2 = star2.split(",")

            # if both inputs needed checking then re-pull data needed for bacon query from db for confirmed inputs
            for i in [star1, star2]:
                cursor.execute("""SELECT id FROM people WHERE people.name = ? AND people.birth = ?""",  (i[0], i[1],))
                person_id = cursor.fetchall()
                person_id = person_id[0][0]
                i.insert(1, person_id)

        # If only one input needed checking with user
        else:
            print(session["confirmed_star"])
            cursor.execute("""SELECT id FROM people WHERE people.name = ? AND people.birth = ?""", (star1[0], star1[1],))

            person_id = cursor.fetchall()
            person_id = person_id[0][0]
            star1.insert(1, person_id)
            star2 = session["confirmed_star"][0]
        print("star 1:", star1)
        print("star 2:", star2)
        solution = bacon_app.main_query(star1, star2, 1)

        # Emptying confirmed star cookie
        session["confirmed_star"] = None

        try:
            return render_template("index.html", answer=solution)
        except:
            return render_template("error.html")

