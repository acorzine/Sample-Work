import sqlite3 as db
from bottle import route, run, request, response, template

@route("/", method = "GET")
def index():
    return template("index")

@route("/login", method = "POST")
def login():
    user = request.forms.get("Username")
    pswd = request.forms.get("Password")

    conn = db.connect("movies5.db")
    cur = conn.cursor()
    sql = "SELECT year FROM users WHERE name = ? AND password = ?"
    cur.execute(sql, (user,pswd))
    result = cur.fetchone()
    cur.close
    
    
    if (result):
        response.set_cookie("year", result[0])
        welcome = {"Username": user}
        return template("menu", welcome)
    else:
        m = {"msg": "Login Failed"}
        return template("status", m)

@route("/showFilms", method = "GET")
def table():
    year = request.get_cookie("year")
    if not year:
        m = {"msg": "Not Logged In"}
        return template("status", m)
    sql = '''SELECT film_id, title, description, release_year, length, categories.name
            FROM films, categories
            WHERE films.category = categories.category and release_year = ?'''

    table_heading = '''<th>Film_ID</th><th>Title</th><th>Description</th>
        <th>Release Year</th><th>Length</th><th>Category</th>'''

    try:
        conn = db.connect("movies5.db")
        cur = conn.cursor()
        cur.execute(sql, (year,))
        result = cur.fetchall()

        if result:
            data = {"table_heading": table_heading, "result": result}
            return template("showFilms", data)
        else:
            return "<p>Your request was unable to complete.</p>"

    #except db.Error as er:
        #print("There has been an error. Please try again.")
        
    finally:
        cur.close

    

@route("/enterFilm", method = ["GET", "POST"])
def add_film():
    if request.method == "GET":
        year = request.get_cookie("year")
        if not year:
            m = {"msg": "Not Logged In"}
            return template("status", m)
        return template("enterFilm")

    else:
        if not request.get_cookie("year"):
            m = {"msg": "Not Logged In"}
            return template("status", m)
        else:
            year = request.get_cookie("year")
            record = []
            record.append(request.forms.get("film_id"))
            record.append(request.forms.get("title"))
            record.append(request.forms.get("description"))
            record.append(request.forms.get("release_year"))
            record.append(request.forms.get("length"))
            record.append(request.forms.get("category"))

            try:
                conn = db.connect("movies5.db")
                cur = conn.cursor()
                record[3] = year
                sql = "INSERT INTO films VALUES (?, ?, ?, ?, ?, ?)"
                cur.execute(sql, record)

                line1 = "<p>Successfully added records to database.</p>"
                #line2 = "<a href=/login>Click here to return to the main menu.</a>" COULD NOT GET THIS TO WORK
                #   Keeps producing Error:405 Method not Allowed
                #   I'm betting it's because /login isn't getting access to the login information from login()
                return line1
                        
            except db.Error as er:
                print(er)
            finally:
                conn.commit()
                conn.close

run(host = "localhost", port = 8080)
