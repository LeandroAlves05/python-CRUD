from flask import Flask, render_template, redirect, request, flash
import json
import ast

app = Flask(__name__)
app.config["SECRET_KEY"] = "LEO"

logged = False


@app.route("/")
def home():
    global logged
    logged = False

    return render_template('login.html')


@app.route("/adm")
def adm():
    if logged == True:
        with open("users.json") as usersTemp:
            users = json.load(usersTemp)
        return render_template("admin.html", users=users)
    if logged == False:
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    global logged

    name = request.form.get("name")
    password = request.form.get("password")

    with open("users.json") as usersTemp:
        users = json.load(usersTemp)
        count = 0

        for user in users:
            count += 1
            if name == "admin" and password == "000":
                logged = True
                return redirect("/adm")

            if user["name"] == name and user["password"] == password:
                return render_template("user.html")

            if count >= len(users):
                flash("Invalid User")
                return redirect("/")


@app.route("/registerUser", methods=["POST"])
def registerUser():
    global logged

    name = request.form.get("name")
    password = request.form.get("password")
    user = [
        {
            "name": name,
            "password": password
        }
    ]
    with open("users.json") as usersTemp:
        users = json.load(usersTemp)

    newUser = user + users

    with open("users.json", "w") as registerTemp:
        json.dump(newUser, registerTemp, indent=4)
    logged = True
    flash(F"User {name} Registered!")
    return redirect("/adm")


@app.route("/deleteUser", methods=["POST"])
def deleteUser():
    global logged
    logged = True

    user = request.form.get("delete_user")
    userDict = ast.literal_eval(user)
    name = userDict["name"]

    with open("users.json") as usersTemp:
        usersJSON = json.load(usersTemp)
        for c in usersJSON:
            if c == userDict:
                usersJSON.remove(userDict)
                with open("users.json", "w") as delete_user:
                    json.dump(usersJSON, delete_user, indent=4)

    flash(F"User {name} Deleted.")
    return redirect("/adm")


if __name__ == "__main__":
    app.run(debug=True)
