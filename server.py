from flask import Flask,render_template,redirect,request,jsonify
import datetime,sqlite3
app = Flask(__name__)

Insertquery='INSERT INTO DATA(Model,HwVersion,SWVersion,Id,DeviceName) VALUES("%s","%s","%s","%s","%s")';
Fetchquery='SELECT * from data'
sql_delete_query = """DELETE FROM DATA WHERE _id = ?"""
dbfilename = "DeviceDetails.db"
particular_id = 'SELECT * FROM data WHERE _id = ?'

def welcome_msg():
    return "Flask Working fine -- welcome"

@app.route("/")
def login():
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
        print ("ID is ",id)
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        cursor.execute(particular_id, (id,))
        receivedData = cursor.fetchall()
        conn.close()
        print("done.....")
        return render_template("individualdashboard.html", Result=receivedData)
    
    except Exception as e:
        print("An error occurred:", e)
        return "An error occurred. Please try again later.", 500

def Createtable():
    print("table")
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
    return "Succesfully Added"

@app.route("/insertdata",methods=['POST'])
def Fetch_all():
    con=sqlite3.connect(dbfilename)
    c=con.cursor()
    c.execute(fetchQuery)
    receivedData=c.fetchall()
    return render_template("index3.html",results=receivedData)

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
    print("hii python")
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
    app.run(host="0.0.0.0",debug=True)