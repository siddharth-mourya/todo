import os
from datetime import datetime,timedelta
from validate_email import  validate_email       #for email validation
from flask import Flask, render_template, jsonify, request, flash, session, url_for
from flask_mysqldb import MySQL
import bcrypt                                    #for hashing
from werkzeug.utils import redirect


app = Flask(__name__)
app.secret_key = '1234567890'


app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todo'
mysql=MySQL(app)

''' -------------------------- file upload directory config ------------------------------------'''

app.config['UPLOAD_PATH']= 'static\\img\\taskImage'


#routes which render html==============================================================================
@app.route("/")
def indexOrLogin():
    if 'user' in session:
        return redirect('/home')
    return render_template('login.html')

@app.route("/home")
def home():
    if 'user' in session:                       #added this line now
        query = "select * from task where email=%s"
        data= (session['user'],)
        result = getDataWithPara(query,data)
        categories = []
        for row in result:
            if row[3]in categories:
                pass
            else:
                categories.append(row[3])
        #category wise data fitting in slider
        catData =[]
        for category in categories:             # making list of list of in which inner list will be list of tuple of specific category
            list=[]
            catData.append(list)                #[[category1],[category2],[category3]]
        for category in categories:
            for row in result:
                if category in row[3]:
                    # making data strucure like [ [ (task1,grocery),(task2,grocery),(task3,grocery)] , [(task4,Food) ]]
                    catindex = categories.index(category)
                    catData[catindex].append(row)
                else:
                    pass

        #adjacent day data gathering
        adjData = [[],[],[]]            #[0] is prev  .... [1] is today ..... [2] is tommorow
        todayDate = datetime.now()
        prevDate = datetime.now() - timedelta(days=1)
        nextDate = datetime.now() + timedelta(days=1)
        for row in result:
            if str(row[4]) == str(prevDate.strftime('%Y-%m-%d')):
                adjData[0].append(row)
            if str(row[4]) == str(todayDate.strftime('%Y-%m-%d')):
                adjData[1].append(row)
            if str(row[4]) == str(nextDate.strftime('%Y-%m-%d')):
                adjData[2].append(row)

        #getting categories registered in user table
        query="select category,name from users where email=%s"
        data=(session['user'],)
        result=getDataWithPara(query,data)
        userCatList = result[0][0].split("|")
        userCatList=userCatList[1:]
        name=result[0][1]
        print(userCatList)
        print(adjData)
        print(categories)
        print(catData)
        return render_template('index.html',name=name, userCatList=userCatList, adjData=adjData, categories=categories , catData=catData)
    else:
        return render_template("login.html")
#-----------------------------------------------login route---------------------------------------------
@app.route("/login" , methods=['GET','POST'])
def login():
    message=""
    if 'user' in session:
        return redirect('/home')
    if request.method == "POST":
        email = request.form.get("email")
        password=request.form.get("password").encode('UTF-8')           #unicode encoding is required here to use bcrypt
        query="select hashedpwd,salt from users where email=%s"
        data=(email,)
        result = getDataWithPara(query,data)
        if not result:                                          #if no entry for this email
            message="no such credentials, register first"
            flash(message,"danger")
            return render_template('login.html')
        else:                                                   #if some entry for this email
            hashedpwd=""
            for row in result:
                #first we have to encode value we got from db
                hashedpwd =row[0].encode('UTF-8')               #getting hashedpwd from result =>( (hashedpwd,salt,),)

            if bcrypt.checkpw(password, hashedpwd):
                session['user'] = email
                return redirect('/home')
            else:
                message="incorrect password"
                flash(message,"danger")
                return  render_template('login.html')
    return render_template('login.html')

#-----------------------------------------------logout route ----------------------------------------------
@app.route("/logout")
def logout():
    session.pop('user')
    print("logged out of session")
    return redirect('/')


#-----------------------------------------------register route---------------------------------------------
@app.route("/register" , methods=['GET','POST'])
def register():
    message=""
    if request.method == "POST":
        phone = request.form.get("phone")                           #phone
        name = request.form.get("name")                             #name
        email = request.form.get("email")                           #email
        password = request.form.get("password").encode('UTF-8')
        salt = bcrypt.gensalt()                                     #salt
        hashedpwd = bcrypt.hashpw(password, salt)                   #hashedpwd
        category="|Groceries|Office|Home|Drugs|Others"               #category
        # inserting the data in users table
        data=(name,email,hashedpwd,salt,phone,category)
        query ="INSERT INTO users(name,email,hashedpwd,salt,phone,category) values( %s , %s ,%s , %s ,%s , %s)"
        message = "successfully registered"
        insert_data(query,data)
        flash(message,"success")
    return render_template('login.html')


#-----------------------------------------------addRoute route---------------------------------------------
@app.route("/addTask" , methods=['GET','POST'])
def addTask():
    if 'user' in session:                       #added this line now
        message="Task added successfully, we'll remind you on date."
        if request.method == "POST":
            task=request.form.get("title")
            category = request.form.get("category")
            date=request.form.get("date")
            description = request.form.get("description")
            if category=="Select Category":
                category = "Others"
            files = ""
            count=-1
            for f in request.files.getlist('files[]'):
                print("in saving file for")
                print(f.filename)
                if f.filename != "":
                    count=count+1
                    filename = datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + str(count)
                    f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                    files = files + "|" + filename
            status="no"
            email = session['user']                                        #data to insert here is done
            query="insert into task(email,task,category,date,description,files,status) values(%s,%s,%s,%s,%s,%s,%s)"
            data=(email,task,category,date,description,files,status)
            insert_data(query,data)
            print("task data inserted successfully")
            flash(message,"success")
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/searchTask")
def searchTask():
    if 'user' in session:                       #added this line now
        name = getName()
        query = "select * from task where email=%s "
        data = (session['user'],)
        result = getDataWithPara(query , data)
        categories = getCategories()
        return render_template("search.html", name=name, categories=categories , data = result)
    else:
        return render_template("login.html")

@app.route("/filter" ,methods=["POST","GET"])
def filterTask():
    if 'user' in session:                       #added this line now
        if request.method =="POST":
            query = "select * from task where email=%s "
            data = (session['user'],)
            category = request.form.get("category")
            startDate= request.form.get("startDate")
            endDate = request.form.get("endDate")
            search = request.form.get("search")
            if category == "Select Category":
                category=""
            if search:
                search = "%"+search+"%"
            #framing query now
            if category:
                query = query + "and category=%s "
                l=list(data)
                l.append(category)
                data = tuple(l)
            if startDate:
                query = query + "and date >= %s "
                l = list(data)
                l.append(startDate)
                data = tuple(l)
            if endDate:
                query = query + "and date <= %s "
                l = list(data)
                l.append(endDate)
                data = tuple(l)
            if search:
                query = query + "and ( task like %s or description like %s )"
                l = list(data)
                l.append(search)
                l.append(search)
                data = tuple(l)
            result = getDataWithPara(query,data)
            print(result)
            print(query)
            print(data)
            categories = getCategories()
            name = getName()
        return render_template("search.html",name=name ,categories=categories , data = result)
    else:
        return render_template("login.html")

@app.route("/settings")
def settings():
    if 'user' in session:                       #added this line now
        name = getName()
        categories =getCategories()
        return render_template("settings.html" , name=name, email=session['user'] ,categories=categories )
    else:
        return render_template("login.html")

@app.route("/addNewCategory" , methods = ['POST','GET'])
def addNewCategory():
    if 'user' in session:                           # added this line now
        message = ""
        if request.method =="POST":
            newCatNAme =request.form.get("newCatName")
            categories =getCategories()
            if newCatNAme in categories:
                message = "category already exist please add if not there"
                flash(message,"danger")
                return redirect("/settings")
            newCatNAme =newCatNAme.title()
            categories.append(newCatNAme)
            updatedCat = ""
            for x in categories:
                if x != "":
                    updatedCat = updatedCat + "|" + x
            print(updatedCat)
            query = "update users set category=%s where email=%s"
            data = (updatedCat, session['user'])
            update(query, data)
            message="category added successfully"
            flash(message,"success")
            return redirect("/settings")
    else:
        return render_template("login.html")

@app.route("/deleteAllTask" , methods = ['POST','GET'])
def deleteAllTask():
    if 'user' in session:
        message = ""
        if request.method =="POST":
            userReq =request.form.get("deleteAllTask")
            userReq =userReq.lower()
            query = "select * from task where email=%s"     #query to check if any task exist or not
            data = (session['user'],)
            result = getDataWithPara(query, data)
            if result :
                if userReq == "yes":
                    query = "delete from task where email=%s"
                    data = (session['user'],)
                    deleteTask(query, data)
                    message="All the task you added are deleted"
                    flash(message,"warning")
                message = "You didn't write 'YES' so your tasks are not deleted"
                flash(message, "success")
            else:
                message = "There are no task in your list add some new task."
                flash(message, "warning")
        return redirect("/settings")
    else:
        return render_template("login.html")

@app.route("/changeEmail" , methods = ['POST','GET'])
def changeEmail():
    if 'user' in session:
        message = ""
        if request.method =="POST":
            newEmail =request.form.get("changeEmail")
            if validate_email(newEmail,verify=True):
                query = "update task set email=%s where email=%s"
                data = (newEmail, session['user'])
                update(query, data)
                query = "update users set email=%s where email=%s"
                data = (newEmail, session['user'])
                update(query, data)
                message="email successfully changed.... have fun"
                flash(message,"success")
                session['user'] = newEmail
                print(session['user'])
            else:
                message = "email cannot be changed check if email is correct"
                flash(message, "danger")
        return redirect("/settings")
    else:
        return render_template("login.html")

@app.route("/changePassword" , methods = ['POST','GET'])
def changePassword():
    if 'user' in session:
        message = ""
        if request.method =="POST":
            oldPassword =request.form.get("oldPassword").encode('UTF-8')
            newPassword = request.form.get("newPassword").encode('UTF-8')
            query = "select hashedpwd from users where email=%s"
            data = (session['user'],)
            result = getDataWithPara(query, data)
            hashedpwd = result[0][0].encode('UTF-8')  # getting hashedpwd from result =>( (hashedpwd,salt,),)

            if bcrypt.checkpw(oldPassword, hashedpwd):
                if oldPassword.lower()!=newPassword.lower() :
                    salt = bcrypt.gensalt()  # salt
                    hashedpwd = bcrypt.hashpw(newPassword, salt)
                    query = "update users set password=%s, salt=%s where email=%s"
                    data = (newPassword ,salt , session['user'])
                    update(query, data)
                    message="password changed successfully"
                    flash(message,"success")
                else:
                    message = "old and new password can't be same"
                    flash(message, "danger")
            else:
                message = "oldpassword didn't match to your account password"
                flash(message, "danger")
        return redirect('/settings')
    else:
        return render_template("login.html")

#routes which return only data==============================================================================
@app.route("/checkEmailExist/<string:reqemail>")
def checkEmail(reqemail):
    print("here in email exist")
    data = getData("select email from users")
    reqemail=reqemail.lower()
    email=[]
    status={}
    for row in data:
        email.append(row[0].lower())
    if reqemail in email:
        status['exist']='yes'
    else:
        status['exist'] = 'no'
    if  validate_email(reqemail):
        status['EmailServerExist'] = 'yes'
    else:
        status['EmailServerExist'] = 'no'
    print(status)
    return jsonify(status)




# route which only performs some update on db==========================================================
@app.route("/taskDone/<string:taskId>")
def taskDone(taskId):
    print(taskId)
    query="update task set status=%s where id=%s"
    data=("yes",taskId)
    update(query,data)
    status = {"updated":"yes"}
    return jsonify(status)


@app.route("/taskNotDone/<string:taskId>")
def taskNotDone(taskId):
    print(taskId)
    query = "update task set status=%s where id=%s"
    data = ("no", taskId)
    update(query, data)
    status = {"updated": "yes"}
    return jsonify(status)


@app.route("/taskDelete/<string:taskId>")
def taskDelete(taskId):
    print(taskId)
    query = "delete from task where id=%s"
    data = (int(taskId),)
    deleteTask(query, data)
    status = {"deleted": "yes"}
    return jsonify(status)

@app.route("/getDataToEdit/<string:taskId>")
def getDataToEdit(taskId):
    query = "select * from task where email=%s and id=%s"
    data = (session['user'],taskId)
    result = getDataWithPara(query,data)
    print(result)
    return jsonify(result)

@app.route("/updateTask/<string:taskId>" , methods = ['POST','GET'])
def updateTask(taskId):
    if request.method == "POST":
        task = request.form.get("title")
        category = request.form.get("category")
        date = request.form.get("date")
        description = request.form.get("description")
        templist=[task,category]
        query = "update task set task=%s , category=%s"
        if date!= "":
            query = query + " , date=%s "
            templist.append(date)
        query = query + ", description=%s where id=%s"
        templist.append(description)
        templist.append(taskId)
        data = tuple(templist)
        print(query)
        print(data)
        update(query, data)
    return redirect("/searchTask")

@app.route("/deleteImage/<string:taskId>/<string:imageNo>")
def deleteImage(taskId,imageNo):
    imageNo=int(imageNo)
    print(imageNo)
    query = "select files from task where email=%s and id=%s"
    data = (session['user'], taskId)
    result = getDataWithPara(query, data)
    imageFileDb = result[0][0]
    print(imageFileDb)
    imageList = imageFileDb.split("|")
    imageList.pop(imageNo+1)
    print(imageList)
    imageFileDb=""
    print(imageFileDb)
    for x in imageList:
        if x != "":
            imageFileDb=imageFileDb+"|"+x
    print(imageFileDb)

    query = "update task set files=%s where id=%s"
    data = (imageFileDb, taskId)
    update(query, data)
    status = {"deleted": "yes"}
    return jsonify(status)

@app.route("/deleteCategory/<string:catName>")
def deleteCategory(catName):
    delStatus = {"status" : ""}
    catInDbList = getCategories()
    catInDbList.remove(catName)
    print(catInDbList)
    updatedCat=""
    for x in catInDbList:
        if x != "":
            updatedCat=updatedCat+"|"+x
    print(updatedCat)
    query = "update users set category=%s where email=%s"
    data = (updatedCat, session['user'])
    update(query, data)
    delStatus['status']="yes"
    return  jsonify(delStatus)


# simple function which return data ===================================================================
def getCategories():
    query = "select * from users where email=%s "
    data = (session['user'],)
    result = getDataWithPara(query, data)
    categories = result[0][6].split("|")
    categories=categories[1:]
    print("categories are")
    print(categories)
    return categories;

def getName():
    query = "select name from users where email=%s "
    nameData = (session['user'],)
    name = getDataWithPara(query, nameData)
    name = name[0][0]
    return  name

def getEmailList():
    query = "select email from users "
    result = getData(query)
    emailsList =[]
    for row in result:
        emailsList.append(row[0])
    return emailsList

#sql queries===========================================================================================
def getData(query):
    cur = mysql.connection.cursor()  # getting curser object similar to prepared statement
    cur.execute(query)
    data = cur.fetchall()            # getting list of users for comparing if users is present in db
    mysql.connection.commit()
    cur.close()                      # connectecion closed
    return data

def getDataWithPara(query,data):
    cur = mysql.connection.cursor()  # getting curser object similar to prepared statement
    cur.execute(query,data)
    data = cur.fetchall()            # getting list of users for comparing if users is present in db
    mysql.connection.commit()
    cur.close()                      # connectecion closed
    return data

def insert_data(query,data):
    cur = mysql.connection.cursor()  # getting curser object similar to prepared statement
    cur.execute(query,data)
    mysql.connection.commit()
    print('data successfully inserted')
    cur.close()

def update(query,data):
    cur = mysql.connection.cursor()  # getting curser object similar to prepared statement
    cur.execute(query,data)
    mysql.connection.commit()
    print('data updated inserted')
    cur.close()

def deleteTask(query,data):
    cur = mysql.connection.cursor()  # getting curser object similar to prepared statement
    cur.execute(query,data)
    mysql.connection.commit()
    print('data deleted successfully')
    cur.close()


app.run(debug=True)