from flask import Flask,render_template,redirect,request,jsonify,session
import datetime,sqlite3
import random
from datetime import datetime


app = Flask(__name__)
app.secret_key="ruban"



Insertquery='INSERT INTO DATA(Model,HwVersion,SWVersion,Id,DeviceName) VALUES("%s","%s","%s","%s","%s")';
Fetchquery='SELECT * from data WHERE _id !=?'
sql_delete_query = """DELETE FROM DATA WHERE _id = ?"""
dbfilename = "IOTgateway.db"
particular_id = 'SELECT * FROM data WHERE _id = ?'
Insertquery_for_user_data='INSERT INTO users(Username,Email,Password,Terms) VALUES("%s","%s","%d","%s")';
Insertquery_Output='INSERT INTO dataOutput(Date,Time,DeviceID,Output) VALUES("%s","%s","%s","%s")';
particular_id_output='SELECT * FROM dataOutput WHERE DeviceId=? ORDER BY _id DESC;'

Insertquery_send='INSERT INTO datas_output(Date,Time,Data,Device_id) VALUES("%s","%s","%s","%s")';

#update_output = 'UPDATE datas_output SET  WHERE Device_id = ?'

Device_id=0
user_name=""



def Createusertabler():
    Createtablequery_for_user="""CREATE TABLE IF NOT EXISTS "users" (
                "Username" TEXT NOT NULL,
                "Email" TEXT NOT NULL,
                "Password" INTEGER NOT NULL,
                "Terms" TEXT NOT NULL,
                "_id" INTEGER NOT NULL, PRIMARY KEY("_id" AUTOINCREMENT)
                );"""
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(Createtablequery_for_user)
    conn.commit()
    conn.close()

@app.route("/register")
def signup():
     return render_template("register.html")

@app.route("/store_inputs",methods=['POST'])
def storeuser():
    username = request.form["username"]
    email= request.form["email"]
    Password= int(request.form["password"])
    Terms= request.form["terms"]
    print(username,email,Password,Terms)
    if Check_if_exists(email):
        return("Erorr")
    else:
        conn=sqlite3.connect(dbfilename)
        cursor=conn.cursor()
        cursor.execute(Insertquery_for_user_data%(username,email,Password,Terms))
        conn.commit()
        conn.close()
        return("success")
    
def Check_if_exists(email):
    try:
        user_email_query='SELECT username,password FROM users WHERE Email = ?'
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute(user_email_query, (email,))
        password = cursor.fetchone()
        print(password)
        conn.close()
        if password:
            return True
        else:
            return None
    except Exception as e:
        return False

def welcome_msg():
    return "Flask Working fine -- welcome"

def find_matching(email):
     try:
        user_email_query='SELECT username,password FROM users WHERE Email = ?'
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute(user_email_query, (email,))
        password = cursor.fetchone()
        print(password)
        conn.close()
        if password:
            return (password)
        else:
            return None
     except Exception as e:
        return (e)

@app.route("/")
@app.route('/login',methods=['POST','GET'])
def login():
    
    if(request.method == 'POST'):
        username = request.form.get("email")
        password = request.form.get("password")
        user_info=find_matching(username)
        db_password=str(user_info[1])
        global user_name
        user_name=user_info[0]
        print("2",db_password) 
        if db_password and password == db_password:
               session['user'] = username
               return redirect('/index3.html')
        Error="Wrong Password"
        return render_template("login.html",value=Error)    

    return render_template("login.html")


@app.route("/index3.html")
def dashboard():
    if 'user' in session:  # Check if user is logged in
        username = session['user']
        conn=sqlite3.connect(dbfilename)
        cursor=conn.cursor()
        cursor.execute(Fetchquery,(51,))
        receivedData=cursor.fetchall()
        global user_name
        print("username",user_name)
        return render_template("index3.html",Result=receivedData,username=user_name)
    
    Error="You Are Not Login"
    return render_template("login.html",value=Error)

@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect("/login")


@app.route("/formEdited.html")
def form_input():
    global user_name
    return render_template("formEdited.html",username=user_name)


@app.route("/individualdashboard.html",methods=['GET'])
def inner_device():
    try: 
        id = request.args["id"]
        global Device_id
        Device_id=id
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute(particular_id, (id,))
        receivedData = cursor.fetchall()
        conn.close()
        receivedData2=fetch_output(id)
        global user_name
        return render_template("individualdashboard.html", Result=receivedData, Result2=receivedData2,username=user_name)

    except Exception as e:
        print("An error occurred:", e)
        return "An error occurred. Please try again later.", 500

def Createtable():
    Createtablequery="""CREATE TABLE IF NOT EXISTS "data" (
                "Model" TEXT NOT NULL,
                "HwVersion" TEXT NOT NULL,
                "SWVersion" TEXT NOT NULL,
                "Id" TEXT NOT NULL,
                "DeviceName" TEXT NOT NULL,
                "_id" INTEGER NOT NULL, PRIMARY KEY("_id" AUTOINCREMENT)
                );
                """
   
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(Createtablequery)
    conn.commit()
    conn.close()
    


def Createtable2():
    Createtablequery="""CREATE TABLE IF NOT EXISTS "dataOutput" (
                "Date" TEXT NOT NULL,
                "Time" TEXT NOT NULL,
                "DeviceId" TEXT NOT NULL,
                "Output" TEXT NOT NULL,
                "_id" INTEGER NOT NULL, PRIMARY KEY("_id" AUTOINCREMENT)
                );
                """
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(Createtablequery)
    conn.commit()
    conn.close()

def Createtable3():
    Createtablequery="""CREATE TABLE IF NOT EXISTS "datas_output" (
                "Date" TEXT NOT NULL,
                "Time" TEXT NOT NULL,
                "DeviceId" TEXT NOT NULL,
                "Output" TEXT NOT NULL,
                "_id" INTEGER NOT NULL, PRIMARY KEY("_id" AUTOINCREMENT)
                );
                """
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(Createtablequery)
    conn.commit()
    conn.close()

def insertdata_for_input(Device_id,input):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    date=datetime.now().strftime('%d-%m-%y')
    time=datetime.now().strftime('%H:%M:%S')
    cursor.execute(Insertquery_Output%(date,time,Device_id,input))
    conn.commit()
    conn.close()
    
def insertdata_for_output(Device_id):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    date=datetime.now().strftime('%d-%m-%y')
    time=datetime.now().strftime('%H:%M:%S')
    cursor.execute(Insertquery_send%(date,time,0,Device_id))
    conn.commit()
    conn.close()


def update_for_output(Device_id,decimal_value):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    date=str(datetime.now().strftime('%d-%m-%y'))
    time=str(datetime.now().strftime('%H:%M:%S'))
    queryString = "UPDATE datas_output SET Date ='"+date+"',Time='"+time+"',Data="+str(decimal_value)+" WHERE Device_id ="+str(Device_id)+""
    print (queryString)
    cursor.execute(queryString)
    conn.commit()
    conn.close()


def fetch_output(DeviceID):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(particular_id_output, (DeviceID,))
    receivedData=cursor.fetchall()
    conn.close()
    return (receivedData)


@app.route("/insertdata",methods=['POST'])
def insert():
    Model = request.form["Model"]
    HwVersion= request.form["HwVersion"]
    SWVersion= request.form["SwVersion"]
    Id= request.form["Id"]
    DeviceName=request.form["DeviceName"]
    try:
       
        conn=sqlite3.connect(dbfilename)
        cursor=conn.cursor()
        cursor.execute(Insertquery%(Model,HwVersion,SWVersion,Id,DeviceName))
        conn.commit()
        conn.close()
        Device_id=getLastId()
        insertdata_for_output(Device_id)
    except Exception as e:
        print (e)
    
    print(DeviceName)
    return "Succesfully Added"

def getLastId():
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute("SELECT MAX(_id) FROM data")
    last_id=cursor.fetchone()[0]
    conn.close()
    return last_id




@app.route("/iopins",methods=['POST'])
def io_pins():
    try:
       input=request.form["input"]
    except Exception as e:
       return "Give some data"
    try:
        deviceID=request.form["device_id"]
    except Exception as e:
        deviceID="51"
    insertdata_for_input(deviceID,input)
    selectDeviceQuery = "SELECT * FROM datas_output WHERE Device_id = " + deviceID
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(selectDeviceQuery)
    device=cursor.fetchall()[0]
    conn.close()
    return str(device[3])

@app.route("/deleteuser",methods=['GET'])
def delete_user():
    try:
        email_id = request.args["email_id"]
        print(email_id)
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()

        cursor.execute("SELECT * from users where Email = '%s'"%email_id)
        
        user = cursor.fetchall()
        
        print (len(user))
        if len(user) == 0:
            return "Email not found"
        
        sql_delete_query_for_user = "DELETE FROM users WHERE Email = '%s'"%email_id
        cursor.execute(sql_delete_query_for_user)
        # cursor.close()
        conn.commit()
        conn.close()

        return "Successfully deleted"
    
    except Exception as e:
        print("Exception:", str(e))
        return "An error occurred", 500

@app.route("/refresh_table")
def refresh_table():
    global Device_id
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(particular_id_output, (Device_id,))
    print(Device_id)
    receivedData=cursor.fetchall()
    #print(receivedData)
    data=[]
    for rows in receivedData:
        data.append({
        'Date':rows[0],
        'Time':rows[1],
        'Output':rows[3],
        })
    #data=Reverse(data)
    return jsonify(data)    

def Reverse(lst):
   new_lst = lst[::-1]
   return new_lst

@app.route("/deletedata", methods=['POST'])
def delete_record():
    try:
        ID = request.form["ID"]
        
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        

        sql_delete_query = "DELETE FROM data WHERE _id = ?"
        cursor.execute(sql_delete_query, (ID,))
     
        delete_input(conn, cursor, ID)
        delete_output(conn, cursor, ID)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return "Successfully deleted"
    except Exception as e:
        print("Exception:", str(e))
        return "An error occurred", 500

def delete_input(conn, cursor, deviceId):
    try:
        print("input")
        datas_input_delete_query = "DELETE FROM dataOutput WHERE DeviceId = ?"
        cursor.execute(datas_input_delete_query, (deviceId,))
        conn.commit()
    except Exception as e:
        print("An error occurred:", str(e))
        return "An error occurred", 500

def delete_output(conn, cursor, deviceId):
    try:
        print("output")
        datas_output_delete_query = "DELETE FROM datas_output WHERE Device_id = ?"
        cursor.execute(datas_output_delete_query, (deviceId,))
        conn.commit()
    except Exception as e:
        print("An error occurred:", str(e))
        return "An error occurred", 500

@app.route("/refresh")
def refresh():
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(Fetchquery)
    receivedData=cursor.fetchall()
    #print(receivedData)
    data=[]
    for rows in receivedData:
        data.append({
        'Model':rows[0],
        'HwVersion':rows[1],
        'SWVersion':rows[2],
        'Id':rows[3],
        'DeviceName':rows[4],
        '_Id':rows[5],
        })
    
    return jsonify(data)


@app.route("/decimal", methods=['POST'])
def decimal():
    try:
        data = request.json
        if data and 'value' in data:
            first_data = data['value']
            print("Received data:", first_data)
            global Device_id
            update_for_output(Device_id,first_data)
            global decimal_value
            decimal_value=first_data
            return "Successfully received data"
        else:
            return "Error: Data format is incorrect", 400  
    except Exception as e:
        print("Error:", e)
        return "Error: Internal Server Error", 500


@app.route("/show_output", methods=['POST'])
def show():
    #global Device_id
    #print(Device_id)
    #print("hlo",Device_id)
    selectDeviceQuery = "SELECT * FROM datas_output WHERE Device_id = " + str(Device_id)
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(selectDeviceQuery)
    devices=cursor.fetchall()[0]
    conn.close()
    return str(devices[3])
    
      

if __name__ == "__main__":
    
    Createusertabler()
    Createtable()
    Createtable2()
    Createtable3() 
    app.run(host="0.0.0.0",debug=True)