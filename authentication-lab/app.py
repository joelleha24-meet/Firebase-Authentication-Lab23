from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
Confing = {
  "apiKey": "AIzaSyAtAHeUetN4JoURWE11nvoglrd6_dX-Tyc",
  "authDomain": "joelle-example.firebaseapp.com",
  "projectId": "joelle-example",
  "storageBucket": "joelle-example.appspot.com",
  "messagingSenderId": "828567922002",
  "appId": "1:828567922002:web:9d61695ad2ee0c9adcc68b"
};
firebase = pyrebase.initialize_app(confing)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet.html'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)