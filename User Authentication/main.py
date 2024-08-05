from flask import *
from database import UserClass
from hash import Pass_hashing
import sqlite3
import random
import smtplib
from datetime import datetime, timedelta
from flask_session import Session

app = Flask(__name__)
db = UserClass()
hp = Pass_hashing()
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'index' 

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# ------------------------------------------------------------------------
def generate_otp():
    otp_user = random.randint(100000, 999999)
    session["otp"] = otp_user
    return otp_user

def send_email(to_email, otp):
    from_email = 'nandhithamadhavan2004@gmail.com'
    from_password = 'haritha@1'
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, from_password)
        subject = 'Your OTP Code'
        body = f'Your OTP code is {otp}'
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(from_email, to_email, message)


@app.route('/request-otp', methods=['POST'])
def request_otp():
    email = session.get('email')
    # Generate OTP and expiry time
    otp = generate_otp()
    expiry = datetime.now() + timedelta(minutes=10)
    send_email(email, otp)



# -------------------------------------------------------------------------------


@app.route('/')  #login page
def index():
    return render_template("index.html", name ="Sign in")


@app.route('/get', methods=['POST']) #login verification and admin or user 
def get():
    email = request.form['email']
    password = request.form['Password']
    hashed = db.get_user(email)
    if hashed != None:
        if hp.verify_pass(hashed,password):
            session["name"] = email
            session["user_type"] = db.get_user_type(email)
            return redirect(url_for("profile"))   
    return render_template("index.html", name ="Email or Password is not a match")

@app.route("/profile")
def profile():
    if "name" in session:
        email = session.get("name")
        user_type = session.get("user_type")
        if user_type:
            userDetails = db.get_user_details(email)
            if user_type == "Admin":
                return render_template("admin.html",first = userDetails[1])
            else:
                return render_template("user.html",first = userDetails[1])
    return redirect(url_for("index"))
    

@app.route("/signup") #signup page
def signup():
    return render_template("index.html", name="signup")

    
@app.route('/verify', methods=['POST']) #signup page string data in database
def verify():
    if request.method == "POST":
        first = request.form["FirstName"]
        last = request.form["LastName"]
        phone = request.form["PhoneNumber"]
        email = request.form["email"]
        password = hp.hashing_pass(request.form["Password"])
        
        if not db.existing_User(email):
            db.insert_user(first,last,phone,email,password,"User")
            return render_template("user_Exist.html",name = "Account Successfully Created",page = "login")
        else:
            return render_template("user_Exist.html",name = "User Already Exists",page = "login")
    return render_template("index.html",name ="Sign in")




@app.route("/create_admin")
def create_admin():
    if session.get("user_type") == "Admin":
        return render_template("admin.html",name = "create_admin")
    return redirect(url_for("index"))
#     msg = Message('OTP', sender='nandhithamadhavan2004@gmail.com', recipients=[email])
#     msg.body = str(otp)
#     mail.send(msg)

@app.route("/user_admin_profile")
def admin_profile():
    email = session.get("name")
    userDetails = db.get_user_details(email)
    if session.get("user_tpye") == "Admin":
        return render_template("admin.html",name = "profile",first = userDetails[0],last = userDetails[1],phone = userDetails[2],email = userDetails[3],user_type = userDetails[5])
    else:
        return render_template("user.html",name = "profile",first = userDetails[0],last = userDetails[1],phone = userDetails[2],email = userDetails[3],user_type = userDetails[5])


@app.route("/home")
def home():
    if session.get("user_type") == "Admin":
        return render_template("admin.html",name = "home")
    else:
        return render_template("user.html",name = "home")


@app.route('/get_create_admin', methods=['POST']) #signup page for admin Account creation to store in database
def get_create_admin():
    if request.method == "POST":
        first = request.form["FirstName"]
        last = request.form["LastName"]
        phone = request.form["PhoneNumber"]
        email = request.form["email"]
        password = hp.hashing_pass(request.form["Password"])
        User_type = request.form["User-Type"]
        if not db.existing_User(email):
            db.insert_user(first,last,phone,email,password,User_type)
    return redirect(url_for("home"))

@app.route('/current_users')
def current_users():
    result = db.all_user()
    print(result)
    return render_template("admin.html",name = "Current_Users",users = result[0],leng = result[1])



@app.route("/delete")
def delete():
    db.delete_User(session.get("name"))
    return render_template("user_Exist.html",name = "Account Successfully Deleted !",page = "Signup")

@app.route("/admin_delete", methods=['POST'])
def admin_delete():
    email = request.form['email']
    db.delete_User(email)
    return redirect("/current_users")
    

@app.route("/logout")
def logout():
    session.pop('name', None)
    session.pop('user_type', None)
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug = True)
