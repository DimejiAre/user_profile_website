from flask import Flask, render_template, request, redirect, url_for, session, json, make_response
from models.user import User
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "secret"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            user = User(request.form["name"], request.form["description"], request.form["password"], request.form["address"], request.form["email"],
                        request.form["phone"], request.form["skills"], request.form["interests"])
            user.create_user()
            return render_template("register.html", registered="{} has been created ".format(request.form["name"]))
        return render_template("register.html")
    except:
        return make_response("Registration Failed!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/login", methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form["email"].lower()
            password = request.form["password"]

            users = User.get_user()
            selected_user = ""
            for key, value in users.items():
                if value['email'] == email and check_password_hash(value['password'], password):
                    selected_user = value
            messages = json.dumps(selected_user)
            session['messages'] = messages
            return redirect(url_for('get_profile'))
        return render_template("login.html")
    except:
        return make_response("Login Failed!", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/logout", methods=['GET'])
def logout():
    try:
        if session['messages']:
            session.pop('messages')
            return redirect(url_for("index"))
    except:
        return make_response("Error Occurred", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route("/profile", methods=['GET', 'POST'])
def get_profile():
    try:
        messages = session.get('messages', None)  # counterpart for session
        user = json.loads(messages)
        return render_template("profile.html", name=user['name'], email=user['email'], address=user['address'],
                               description=user['description'], interests=user['interests'], phone=user['phone'],
                               skills=user['skills'])
    except:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True, port=4500)
