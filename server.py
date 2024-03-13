from flask import Flask,render_template,redirect,request,jsonify,session,url_for
import datetime,sqlite3
import random
from datetime import datetime


app = Flask(__name__)
app.secret_key="ruban"



Insertquery='INSERT INTO device_details(Model,HwVersion,SWVersion,Id,User_Id,DeviceName) VALUES("%s","%s","%s","%s","%s","%s")';
Fetchquery='SELECT * from device_details WHERE User_id =?'
sql_delete_query = """DELETE FROM  WHERE device_details _id = ?"""
dbfilename = "IOTgateway.db"
particular_id = 'SELECT * FROM device_details WHERE _id = ?'
Insertquery_for_user_data='INSERT INTO users(Username,Email,Password,Terms) VALUES("%s","%s","%d","%s")';
Insertquery_Output='INSERT INTO Data_Inputs(Date,Time,DeviceID,Output) VALUES("%s","%s","%s","%s")';
particular_id_output='SELECT * FROM Data_Inputs WHERE DeviceId=? ORDER BY _id DESC;'

Insertquery_send='INSERT INTO datas_output(Date,Time,Data,Device_id) VALUES("%s","%s","%s","%s")';

#update_output = 'UPDATE datas_output SET  WHERE Device_id = ?'

Device_id=0
user_name=""
userID=0
decimal_value=0

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

def Check_if_exists(email):
    try:
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        print("Error:", e)
        return False

def getLast_Id():
    try:
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(_id) FROM users")
        last_id = cursor.fetchone()[0]
        conn.close()
        return last_id or 0
    except sqlite3.Error as e:
        print("Error:", e)
        return None

def insert_user(username, email, password, terms):
    try:
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password, terms) VALUES (?, ?, ?, ?)", (username, email, password, terms))
        last_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return last_id
    except sqlite3.Error as e:
        print("Error:", e)
        return None

def insert_static(model, hw_version, sw_version, device_id, user_id, device_name):
    try:
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO device_details (Model, HwVersion, SWVersion, Id, User_Id, DeviceName) VALUES (?, ?, ?, ?, ?, ?)",
                       (model, hw_version, sw_version, device_id, user_id, device_name))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error:", e)

@app.route("/store_inputs", methods=['POST'])
def storeuser():
    print("hiii")
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        terms = request.form.get("terms")
        print(username,email,password,terms)
        if not all((username, email, password, terms)):
            return "Missing required fields"

        if Check_if_exists(email):
            return "Email already exists"

        last_id = insert_user(username, email, password, terms)
        if last_id is None:
            return "Failed to insert user"

        insert_static("Unknown", "4.3.2", "2.3.4", "783218", last_id, "static")
        return "Success"
    except Exception as e:
        print("Error:", e)
        return "Something went wrong"

def welcome_msg():
    return "Flask Working fine -- welcome"

def find_matching(email):
     try:
        user_email_query='SELECT username,password,_id FROM users WHERE Email = ?'
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute(user_email_query, (email,))
        password = cursor.fetchone()
        conn.close()
        if password:
            return (password)
        else:
            return "none"
     except Exception as e:
        return (e)

@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get("email")
        password = request.form.get("password")
        user_info = find_matching(username)
        db_password = str(user_info[1])
        session["Username"] = user_info[0]
        User_id = user_info[2]
        session['user_id'] = User_id
        global userID
        userID=User_id
        if db_password and password == db_password:
            session['user'] = username
            return redirect(url_for('dashboard', user_id=User_id))
        error = "Wrong Password"
        return render_template("login.html", value=error)
    return render_template("login.html")


@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    if 'user' in session:
        user_name = session['user']
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute(Fetchquery, (user_id,))
        received_data = cursor.fetchall()
        received_data = [row for row in received_data if row[4] != "static"]
        print(received_data)
        print("dashboard",user_id)
        Username = session.get('Username')
        return render_template("index3.html", Result=received_data, username=Username,User_id=user_id)
    else:
        Error="You Are Not Login"
        return render_template("login.html",value=Error)

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect("/login")


@app.route("/formEdited.html")
def form_input():
    User_Id = session.get('user_id')
    user_name=session.get('Username')
    return render_template("formEdited.html",username=user_name,user_id=User_Id)


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
        User_Id = session.get('user_id')
        user_name=session.get('Username')
        return render_template("individualdashboard.html", Result=receivedData, Result2=receivedData2,username=user_name,user_id=User_Id)

    except Exception as e:
        id = request.args["User_id"]
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM device_details WHERE User_Id = ? AND DeviceName="static"', (id,))
        receivedData = cursor.fetchall()
        print(receivedData)
        conn.close()
        deviceid=str(id)+" static"
        
        Device_id = deviceid
        print("ins",Device_id)
        receivedData2=fetch_output(deviceid)
        User_Id = session.get('user_id')
        user_name=session.get('Username')
        User=str(User_Id)+" static"
        return render_template("individualdashboard.html", Result=receivedData, Result2=receivedData2,username=user_name,user_id=User_Id,user=User)

    

def Createtable():
    create_table_query = """CREATE TABLE IF NOT EXISTS "device_details" (
        "Model" TEXT NOT NULL,
        "HwVersion" TEXT NOT NULL,
        "SWVersion" TEXT NOT NULL,
        "Id" TEXT NOT NULL UNIQUE,
        "DeviceName" TEXT NOT NULL,
        "User_Id" TEXT NOT NULL,
        "_id" INTEGER NOT NULL, PRIMARY KEY("_id" AUTOINCREMENT)
        );
    """
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()
    


def Createtable2():
    Createtablequery="""CREATE TABLE IF NOT EXISTS "Data_Inputs" (
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
                "Data" TEXT NOT NULL,
                "Device_id" TEXT NOT NULL,
                "_id" INTEGER NOT NULL, PRIMARY KEY("_id" AUTOINCREMENT)
                );
                """
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(Createtablequery)
    conn.commit()
    conn.close()



def update_for_output(Device_id,decimal_value):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    date=str(datetime.now().strftime('%d-%m-%y'))
    time=str(datetime.now().strftime('%H:%M:%S'))
    queryString = "UPDATE datas_output SET Date =?,Time=?,Data=? WHERE Device_id =?"
    values=(date,time,decimal_value,Device_id)
    print (queryString)
    cursor.execute(queryString,values)
    conn.commit()
    conn.close()


def fetch_output(DeviceID):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(particular_id_output, (DeviceID,))
    receivedData=cursor.fetchall()
    conn.commit()
    conn.close()
    return (receivedData)


@app.route("/insertdata", methods=['POST'])
def insert():
    
    Model = request.form["Model"]
    HwVersion = request.form["HwVersion"]
    SWVersion = request.form["SwVersion"]
    Id = request.form["Id"]
    DeviceName = request.form["DeviceName"]
    User_Id = session.get('user_id')
    print("User_Id:", User_Id)  
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    
    try:
        cursor.execute(Insertquery % (Model, HwVersion, SWVersion, Id, User_Id, DeviceName))
        conn.commit()
        conn.close()
        Device_id = getLastId()
        insertdata_for_output(Device_id)
        print("Successfully added data for Device:", DeviceName)
        user_id=str(User_Id)
        return user_id
    except Exception as e:
        conn.commit()
        conn.close()
        print("Error:", e)
        return str(e)  
    

def getLastId():
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute("SELECT MAX(_id) FROM device_details")
    last_id=cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return last_id

def insertdata_for_input(Device_id,input):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    date=str(datetime.now().strftime('%d-%m-%y'))
    time=str(datetime.now().strftime('%H:%M:%S'))
    cursor.execute(Insertquery_Output%(date,time,Device_id,input))
    conn.commit()
    conn.close()
    
def insertdata_for_output(Device_id):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    date=str(datetime.now().strftime('%d-%m-%y'))
    time=str(datetime.now().strftime('%H:%M:%S'))
    Data=0
    cursor.execute(Insertquery_send%(date,time,Data,Device_id,))
    conn.commit()
    conn.close()

def create_static_output(deviceID):
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    date = datetime.now().strftime('%d-%m-%y')
    time = datetime.now().strftime('%H:%M:%S')
    Data = 0
    cursor.execute("INSERT INTO datas_output (Date, Time, Data, Device_id) VALUES (?, ?, ?, ?)", (date, time, Data, deviceID))
    conn.commit()
    conn.close()
    print("success create")

@app.route("/iopins", methods=['POST'])
def io_pins():
    try:
        input_data = request.form["input"]
    except KeyError:
        return "Input data not provided", 400

    try:
        deviceID = request.form["device_id"]
    except KeyError:
        global userID
        User_Id = userID
        print(User_Id)
        user=request.form["user"]
        print(user)
        deviceID = str(User_Id) + " static"
        print(deviceID)
        create_static_output(deviceID)

    insertdata_for_input(deviceID, input_data)

    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datas_output WHERE Device_id = ?", (deviceID,))
    device = cursor.fetchone()
    conn.close()

    if device:
        return str(device[2]), 200
    else:
        return "Device not found", 404

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
    User_id=session['user_id']
    print(User_id)
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
        

        sql_delete_query = "DELETE FROM device_details WHERE _id = ?"
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
        datas_input_delete_query = "DELETE FROM Data_inputs WHERE DeviceId = ?"
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
    User_Id = session.get('user_id')
    cursor.execute(Fetchquery, (User_Id,))
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
        '_Id':rows[6],
        })
    
    return jsonify(data)
@app.route("/checkID",methods=['POST'])
def isnow():
    try:
        id = request.form["Id"]
        searchquery='SELECT * FROM device_details WHERE Id = ?'
        conn=sqlite3.connect(dbfilename)
        cursor=conn.cursor()
        cursor.execute(searchquery,(id,))
        device = cursor.fetchone()
        print("device:",device)
        if device == None:
            device = 'None'
            print("fdff")
        conn.close()
        return str(device)
    except Exception as e:
        return "False"

@app.route("/decimal", methods=['POST'])
def decimal():
    try:
        data = request.json
        if data and 'value' in data:
            first_data = data['value']
            print("Received data:",first_data)
            global Device_id
            print("dec",Device_id)
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
    global Device_id
    print(Device_id)
    print("hlo",Device_id)
    selectDeviceQuery = "SELECT * FROM datas_output WHERE Device_id = ?"
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(selectDeviceQuery,(Device_id,))
    devices=cursor.fetchall()[0]
    conn.close()
    print("sgjgdsjf",devices[2])
    return str(devices[2])
    
      

if __name__ == "__main__":
    
    Createusertabler()
    Createtable()
    Createtable2()
    Createtable3() 
    app.run(host="0.0.0.0",debug=True)