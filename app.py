from flask import Flask , render_template , url_for , request , redirect , jsonify , session
from werkzeug.utils import secure_filename
import sqlite3
from flaskext.mysql import MySQL
# from flaskext.mysql import MySQL
from authlib.integrations.flask_client import OAuth
import os


app = Flask(__name__)
app.debug = True

app.secret_key = "jwhiwu98we9232kj3hk"
oauth = OAuth(app)
gluu = oauth.register(
    name='gluu',
    client_id='69164f39-5de4-48c8-88f5-2838d8b47d66',
    client_secret='mqNpGNxkM3joidQxUaIL0rdPtZTgK7L2CvcQiQMv',
    access_token_url='https://elkgluustage.abraxasint.com/oxauth/restv1/token',
    access_token_params=None,
    authorize_url='https://elkgluustage.abraxasint.com/oxauth/restv1/authorize',
    authorize_params=None,
    api_base_url='https://elkgluustage.abraxasint.com/oxauth/restv1/authorize',
    userinfo_endpoint='https://elkgluustage.abraxasint.com/oxauth/restv1/clientinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid phone profile email permission role'},    
)


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'espa_new'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
# https://elkgluustage.abraxasint.com/oxauth/restv1/authorize?response_type=code&client_id=69164f39-5de4-48c8-88f5-2838d8b47d66&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fredirect_login&scope=openid+email+profile&state=zytVay1p7C4rRMeYYE1oIFyhrNb99s&nonce=Kqc8eBLr2gGMbmpv1Php
def getConn():
    try:
        return sqlite3.connect("fdb.sqlite")
        # return mysql.connect()
    except e:
        print(e)
    return None
       



@app.route('/login_gluu',methods=['POST','GET'])
def loginGluu():
    gluu = oauth.create_client('gluu')  # create the google oauth client
    redirect_uri = url_for('loginRedirectGluu', _external=True)
    return gluu.authorize_redirect(redirect_uri)

@app.route('/redirect_login',methods=['POST','GET'])
def loginRedirectGluu():
        gluu = oauth.create_client('gluu')  # create the gluu oauth client
        token = gluu.authorize_access_token()  # Access token from gluu (needed to get user info)
        resp = gluu.get('userinfo')  # userinfo contains stuff u specificed in the scrope
        user_info = resp.json()
        return user_info
        user = oauth.gluu.userinfo()  # uses openid endpoint to fetch user info
        return user
        # Here you use the profile/user data that you got and query your database find/register the user
        # and set ur own data in the session not the profile from google
        session['profile'] = user_info
        session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
        return redirect('/')


@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/contact")
def contactUs(username):
    return "<h1> Hello World </h1>"+username

@app.route("/login",methods=['POST'])
def login():
    username = request.form['username']
    pwd = request.form['password']
    photo = request.files['photo']
    photo.save("static/"+secure_filename(photo.filename))
    return redirect(url_for('hello_world'))

@app.route("/register",methods=['GET','POST'])
def register():
    # return "sj"
    username = "dash"
    password = "123456"
    sql = 'INSERT INTO user (username,password) VALUES(?,?)'
    conn = getConn()
    cursor = conn.cursor()
    user =  cursor.execute(sql,(username,password))
    conn.commit()
    return "Insert User id " + str(user.lastrowid)

@app.route("/users",methods=['GET','POST'])
def users():
    sql = """
    SELECT * FROM tbl_gama
    """
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql)
    columns = cursor.description
    result = []
    for value in cursor.fetchall():
        tmp = {}
        for (index,column) in enumerate(value):
            tmp[columns[index][0]] = column
        result.append(tmp)
    return jsonify(result)
    # return result[0]

@app.route("/api_token")
def getToken():
    return {
        "token":"h38y3b4ugi34uy4y3jh34g4383489"
    }
