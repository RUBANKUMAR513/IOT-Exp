from flask import Flask,render_template,redirect,request,jsonify
import datetime,sqlite3
import random
from datetime import datetime
app = Flask(__name__)

Insertquery='INSERT INTO DATA(Model,HwVersion,SWVersion,Id,DeviceName) VALUES("%s","%s","%s","%s","%s")';
Fetchquery='SELECT * from data'
sql_delete_query = """DELETE FROM DATA WHERE _id = ?"""
dbfilename = "IOTgateway.db"
particular_id = 'SELECT * FROM data WHERE _id = ?'

Insertquery_Output='INSERT INTO dataOutput(Date,Time,DeviceID,Output) VALUES("%s","%s","%s","%s")';
particular_id_output='SELECT * FROM dataOutput WHERE DeviceId=? ORDER BY _id DESC;'

Device_id=0

def welcome_msg():
    return "Flask Working fine -- welcome"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login.html")
def logout():
    return render_template("login.html")

@app.route("/index3.html")
def dashboard():
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(Fetchquery)
    receivedData=cursor.fetchall()
    return render_template("index3.html",Result=receivedData)

@app.route("/formEdited.html")
def form_input():
    return render_template("formEdited.html")


@app.route("/individualdashboard.html",methods=['GET'])
def inner_device():
    try: 
        id = request.args["id"]
        global Device_id
        Device_id=id
        print(Device_id)
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute(particular_id, (id,))
        receivedData = cursor.fetchall()
        conn.close()
        receivedData2=fetch_output(id)
        return render_template("individualdashboard.html", Result=receivedData, Result2=receivedData2)

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

def insertdata(Device_id,input):
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    date=datetime.now().strftime('%d-%m-%y')
    time=datetime.now().strftime('%H:%M:%S')
    cursor.execute(Insertquery_Output%(date,time,Device_id,input))
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
    conn=sqlite3.connect(dbfilename)
    cursor=conn.cursor()
    cursor.execute(Insertquery%(Model,HwVersion,SWVersion,Id,DeviceName))
    conn.commit()
    conn.close()
    Device_id=getLastId()
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
    input=request.form["input"]
    deviceID=request.form["device_id"]
    insertdata(deviceID,input)
    return str(random.randint(0,255))    

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
        print("SQL Query:", sql_delete_query)
        cursor.execute(sql_delete_query, (ID,))
        conn.commit()
        cursor.close()
        conn.close()
        return "Successfully deleted"

    except Exception as e:
        print("Exception:", str(e))
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




if __name__ == "__main__":

    Createtable()
    Createtable2()
    #Createtable1()
    #insert1()  
    app.run(host="0.0.0.0",debug=True)