from flask import Flask,render_template,redirect,request
import datetime,sqlite3
app = Flask(__name__)

#insertQuery='INSERT INTO datas(name,password,gender) VALUES("%s","%s","%s")'
#fetchQuery='SELECT * from datas'


def welcome_msg():
    return "Flask Working fine -- welcome"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/index3.html")
def dashboard():
    return render_template("index3.html")



def Create_table():
    createQuery="""
                    CREATE TABLE IF NOT EXISTS datas(
                        pid INTEGER PRIMARY KEY,
                        Name TEXT  NOT NULL,
                        Password TEXT NOT NULL,
                        Gender TEXT NOT NULL
                        )
                    """
    con=sqlite3.connect("database.db")
    c=con.cursor()
    c.execute(createQuery)
    con.commit()
    con.close()


def Fetch_all():
    con=sqlite3.connect("database.db")
    c=con.cursor()
    c.execute(fetchQuery)
    receivedData=c.fetchall()
    return render_template("view.html",results=receivedData)

        

       
if __name__ == "__main__":

    #Create_table() 
    app.run(host="0.0.0.0",debug=True)