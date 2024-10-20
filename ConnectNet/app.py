from flask import Flask,render_template,redirect,url_for, request, session, jsonify
from users_handler import User
from db_handler import DB
import requests
import json

import blogs_handler

import os


app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST','localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER','root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD','root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB','default')

app.config['SP1_URL'] = os.environ.get('SP1_URL','localhost:5001')



app.secret_key = 'tzjjoiu980'

@app.route('/')
def filter():
    
    if 'usersessionId' in session :
        return redirect(url_for('home'))

    return redirect(url_for('login'))

@app.route('/home')
def home():
    
    if 'usersessionId' not in session :
        return redirect(url_for('login'))

    
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])

def login():
    if request.method == 'GET':
        if 'usersessionId' in session :
            return redirect(url_for('home'))
        
        return render_template('login.html')
    
    if request.method == 'POST':
        
        data = request.json
        user = User()
        
        iscreated = user.create(data['username'],data['emailid'],data['password'])

        if iscreated :
            
            if 'usersessionId' not in session :
                session['usersessionId'] = data['emailid']
            
            data['code'] = 200
            data['redirect_url'] = '/home'
        else :
            data['code'] = 400
        return data
    

@app.route('/users',methods=['GET'])
def getAllusers():
    if request.method == 'GET' :

        user = User()
        users = user.getalluserswithFollowers(session.get('usersessionId'))
        return users

@app.route('/follow/<int:userid>', methods=['POST'])
def follow_user_route(userid):
    
    
    print("Debugger :P")
    data = request.json
    user = User()
    print("follow the user - ",userid)
    print("Email from session - ",session.get('usersessionId'))
    user.addFollower(userid,session.get('usersessionId'))
    data = {}
    data['success'] = True
    return data

@app.route('/unfollow/<int:userid>', methods=['DELETE'])
def unfollow_user_route(userid):
    
    
    print("Debugger unfollow :P")
    data = request.json
    user = User()
    print("follow the user - ",userid)
    print("Email from session - ",session.get('usersessionId'))
    user.removeFollower(userid,session.get('usersessionId'))
    data = {}
    data['success'] = True
    return data

@app.route('/blog', methods=['GET','POST'])
def blog_route():
    
    if request.method == 'GET':
        
        res = blogs_handler.fetchAllBlogs(session.get('usersessionId'))
        print(res)
        return jsonify(res),200
    
    
    if request.method == 'POST':
        
        data = request.json
        subject = data['subject']
        desc = data['desc']
        print(data)
        print(subject)
        print(desc)
        res = blogs_handler.createBlog(session.get('usersessionId'),subject,desc)
        print(res)
        return res

@app.route('/fetchexternal', methods=['GET'])
def fetchexternal_route():
    
    if request.method == 'GET':
        
        print("sp1URL - ",app.config['SP1_URL']) 
        print("/HelloFetchExternal")
        reqURL = app.config['SP1_URL']+"/api/info"
        print(reqURL)
        response = requests.get(reqURL)
        print("response - ",response.json())
        return response.json()


@app.route('/insights', methods=['GET'])
def fetchinsights_route():
    
    if request.method == 'GET':
        
        print("sp1URL - ",app.config['SP1_URL']) 
        print("/insights")
        reqURL = app.config['SP1_URL']+"/api/desc"
        
        blogs = blogs_handler.fetchAllBlogs(session.get('usersessionId'))
        #print(blogs)

        data = {}
        i = 1
        for blog in blogs:
            data["desc"+str(i)] = blog['description']
            i+=1

        print(data)    

        json_data = json.dumps(data)

        print(type(json_data))
        
        response = requests.post(reqURL,json=json_data)
        print("response - ",response)
        return response.json(),200    
    



@app.route('/init')
def initiate():
    
    db = DB()
    if db.initialsetup() :
        return redirect(url_for('login'))




if __name__ == '__main__' :
    app.run(host="0.0.0.0",port=5000,debug=True)