from flask import Flask , render_template , url_for , request , redirect , jsonify
from werkzeug.utils import secure_filename
import sqlite3
from flaskext.mysql import MySQL
# from flaskext.mysql import MySQL



app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'espa_new'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def getConn():
    try:
        # return sqlite3.connect("fdb.sqlite")
        return mysql.connect()
    except e:
        print(e)
    return None
       

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
    username = "gurin2"
    password = "123456"
    sql = """
    INSERT INTO user (username,password) VALUES(?,?)
    """
    conn = getConn()
    cursor = conn.cursor()
    user =  cursor.execute(sql,(username,password))
    conn.commit()
    return f"Insert User id {user.lastrowid}"

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