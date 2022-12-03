from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt


class RegisterForm(Form):

    name = StringField("İsim Soyisim :",validators=[validators.length(min=3,max=15),validators.DataRequired("Kullanıcı Adı giriniz")])
    username = StringField("Kullanıcı Adı :",validators=[validators.length(min=3,max=10),validators.DataRequired()])
    email = StringField("Email :",validators=[validators.email(message="Email doğru yazınız"),validators.DataRequired()])
    password = PasswordField("Parola : ",validators=[
        validators.length(min=3,max=10),
        validators.DataRequired(),
        validators.equal_to(fieldname="confirm",message="Parola eşleşmiyor.")

    ])
    confirm = PasswordField("Parola doğrula :",validators=[validators.DataRequired()])




app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "eren"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")

def about():
    return render_template("about.html")

@app.route("/destek")

def destek():
    return render_template("destek.html")

@app.route("/login")

def login():
    return render_template("login.html")

@app.route("/register",methods = ["GET","POST"])

def register():

    form = RegisterForm(request.form)
    
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.confirm.data) #sha256 = Parola şifreleme methodudur.
        
        cursor = mysql.connection.cursor()
        
        sorgu = "Insert into users(name,email,username,password) VALUES(%s ,%s ,%s ,%s)"

        cursor.execute(sorgu,(name,email,username,password))

        mysql.connection.commit()

        cursor.close()


        return redirect(url_for("about"))

    else:
        return render_template("register.html",form = form)

if __name__ == "__main__":

    app.run(debug=True)