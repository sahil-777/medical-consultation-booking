from flask import Flask,session, render_template, request, redirect, sessions,url_for, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail,Message
import hashlib

app=Flask('__name__')
app.secret_key='Secrey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pass@1234'
app.config['MYSQL_DB'] = 'onlinemedicalconsultation'

mysql=MySQL(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'testproject1080@gmail.com'
app.config['MAIL_PASSWORD'] = 'Pass@1234'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        # if request.form.get('home_button'):
        #     return render_template('home.html')

        if request.form.get('about_button'):
            return redirect(url_for('about'))

        elif request.form.get('contact_button'):
            return redirect(url_for('contact'))

        elif request.form.get('login_button'):
            return redirect(url_for('login'))
            #return render_template('login.html')

        elif request.form.get('signup_button'):
            return redirect(url_for('signup'))

        # elif request.form.get('bookappointment_button'):
        #     return render_template('bookappointment.html')
    elif request.method=='GET':
        return render_template('index.html')

@app.route('/home',methods=['POST','GET'])
def home():
    if isloggedin()==False:
        return redirect(url_for('index'))
    elif request.method=='POST':
        if request.form.get('profile_button'):
            return redirect(url_for('profile'))
        elif request.form.get('bookappointment_button'):
            return redirect(url_for('bookappointment'))
        elif request.form.get('logout_button'):
            return redirect(url_for('logout'))
    else:
        return render_template('home.html',session=session)

@app.route('/contact',methods=['POST','GET'])
def contact():
    message=''
    form_dict=request.form.to_dict()
    if request.method == 'POST' and 'fullname' in request.form and 'email' in request.form and 'msg' in request.form:
        fullname = request.form['fullname']
        if len(request.form['msg'])==0 :
            message = 'Please fill out the form !'
            return render_template('contact.html', message=message)
        email = request.form['email']
        msg = request.form['msg']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO contact_info VALUES (NULL,%s, %s,%s)',(fullname,email,msg))
        mysql.connection.commit()
        msg = Message(sender=app.config.get("MAIL_USERNAME"),recipients=[request.form['email']])
        msg.subject = "query received successfully!"
        msg.body = "Hello Sahil from TestProject!"
        msg.body="Hello "+fullname+" !\n\t"+"Your query is received\n will get back to you as soon as possible.!\n\nThank You,\nTeam Medico"
        mail.send(msg)
        message = 'Successfull! You will receive confirmation mail';
    return render_template('contact.html',message = message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login',methods=['POST','GET'])
def login():
#    return render_template('login.html')
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password=md5(%s)', (username,password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return redirect(url_for('home'))
            #return render_template('home.html', msg=msg)
        else:
            msg = 'Incorrect username / password ! '
    return render_template('login.html', msg=msg)

@app.route('/signup',methods=['POST','GET'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        hashPass = hashlib.md5(password.encode('utf8')).hexdigest()
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not username and not password and not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username,email,hashPass))
            mysql.connection.commit()
            msg = 'You have successfully signedup !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg)

@app.route('/home/profile', methods=['POST','GET'])
def profile():
    if isloggedin()==False:
        return redirect(url_for('index'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    cursor.execute('SELECT * FROM accounts WHERE id = %s',(session['id'],))
    user = cursor.fetchone()
    cursor.execute('SELECT * FROM bookappointment WHERE user_id = %s', (session['id'],))
    data = cursor.fetchall()
    return render_template('profile.html', user=user , data=data) 
    

@app.route('/home/bookappointment', methods=['POST','GET'])
def bookappointment():
    if isloggedin()==False:
        return redirect(url_for('index'))
    msg=''
    form_dict=request.form.to_dict()
    if request.method == 'POST':
    #if request.method == 'POST' and request.form.validate():
        fullname = request.form['firstname']
        if len(request.form['appointmentdate'])==0 :
        #if 'age' not in request.form:
            msg = 'Please fill out the form !'
            return render_template('bookappointment.html', msg=msg)
        phone = request.form['phone']
        symptoms = request.form['symptoms']
        gender = request.form['gender']
        reportfile = request.files['reportfile']
        date = request.form['appointmentdate']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO bookappointment VALUES (NULL,%s, %s, %s,%s,%s,%s,%s)',(session['id'],fullname,gender,date,phone,symptoms,reportfile))
        mysql.connection.commit()
        cursor.execute('SELECT * FROM accounts WHERE id = %s',(session['id'],))
        user = cursor.fetchone()
        msg = Message(sender=app.config.get("MAIL_USERNAME"),recipients=[session['email']])
        msg.subject = "Appointment booked successfully!"
        msg.body = "Hello Sahil from TestProject!"
        msg.body="Hello "+fullname+" !\n\t"+"Your appointment is booked successfully on \t" + date +"!\n\nThank You,\nTeam Medico"
        mail.send(msg)
        msg = 'Successfully booked! You will receive confirmation mail';
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('bookappointment.html',msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

def isloggedin():
    if not session.get('loggedin') is None:
        return True
    return False



if __name__ == '__main__':
    app.run(debug=True)