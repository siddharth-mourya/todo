from twilio.rest import Client
import mysql.connector
from mysql.connector import Error
from datetime import datetime,timedelta


account_sid = "*****************************"
auth_token = "********************************"

def sendSMS(smsdata):
    client = Client(account_sid, auth_token)

    for user in smsdata:
        numberTo = "+91"+user[0]
        tasks = user[1]
        print(tasks)
        try:
            client.messages.create(from_="+12023504850",
                                to=numberTo,
                                body=tasks)
        except:
            print("exception occured while msging")


def connect():
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='todo',
                                       user='root',
                                       password='')
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)

    finally:
        print("done everything in connection")
   

def getData(query,data=""):
    conn=connect()
    cursor = conn.cursor()
    if data!="":
        cursor.execute(query,data)
    else:    
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
        
def getPhoneData():
    result=getData("SELECT phone,email FROM users")
    phone=[]
    for row in result:
        l=[]
        l.append(row[0])
        l.append(row[1])
        phone.append(l)
    return phone
    
def getTaskDetail():
    todayDate = datetime.now()
    date = str(todayDate.strftime('%Y-%m-%d'))
    status='no'
    data = (status , date)
    result=getData("SELECT task,email FROM task where status=%s and date=%s ", data)
    taskDetail=[]
    for row in result:
        l=[]
        l.append(row[0])
        l.append(row[1])
        taskDetail.append(l)
    return taskDetail
    
if __name__ == '__main__':
    phoneData = getPhoneData()
    taskDetail = getTaskDetail()
    SMSData = []
    for user in phoneData:
        temp=["","Your todays Task are"]
        count=0
        for task in taskDetail:             #matching email
            if user[1] == task[1]:        
                count = count + 1
                temp[0]=user[0]
                temp[1]=temp[1]+" Task " + str(count) + " : " + task[0] + ", "     
        SMSData.append(temp)
    #got complete sms data
    print(SMSData)
    sendSMS(SMSData)
    print("msg send")
