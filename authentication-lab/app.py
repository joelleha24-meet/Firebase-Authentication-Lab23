from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
confing = {
  "apiKey": "AIzaSyAtAHeUetN4JoURWE11nvoglrd6_dX-Tyc",
  "authDomain": "joelle-example.firebaseapp.com",
  "projectId": "joelle-example",
  "storageBucket": "joelle-example.appspot.com",
  "messagingSenderId": "828567922002",
  "appId": "1:828567922002:web:9d61695ad2ee0c9adcc68b",
  "databaseURL":"https://joelle-example-default-rtdb.europe-west1.firebasedatabase.app/"}
firebase = pyrebase.initialize_app(confing)
auth = firebase.auth()
db=firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except Exception as e:
            return f"{e}"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        bio = request.form['bio']
        username = request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"name": fullname, "email": email,"bio": bio,"username":username}
            db.child("User").child(UID).set(user)

            return redirect(url_for('add_tweet'))
        except:
            return "Authentication failed"
    return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        firstname = request.form['firstname']
        title = request.form['title']
        text = request.form['text']
        try:
            UID = login_session['user']['localId']
            tweet = {"firstname": firstname, "title":title,"text": text}
            db.child("tweet").push(tweet)
            return redirect(url_for('all_tweets'))
        except: 
            error = "tweet failed"
    return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    tweets= db.child("tweet").get().val()
    return render_template("tweets.html",tweets=tweets)




if __name__ == '__main__':
    app.run(debug=True)