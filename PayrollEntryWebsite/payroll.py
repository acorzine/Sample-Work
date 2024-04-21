import sqlite3 as db
from bottle import route, run, request, template

# Home Page
@route("/", method = "GET")
def index():
    return template("login")

# View By Department Tab
@route("/getDepartment", method=["GET", "POST"])
def department():
    
    
    if request.method == "GET":
        return template("dept_form")

    else:
        dept = request.forms.get("dept")
        conn = db.connect("payroll.db")
        cur = conn.cursor()

        try:
            # Select and merge information from database
            sql = '''SELECT pay_data.emp_id, emp_name, wage, hrs_worked FROM employees
                JOIN pay_data
                WHERE pay_data.emp_id = employees.emp_id AND employees.department = ?'''

            cur.execute(sql, (dept,))
            results = cur.fetchall()

            if results:
                dataList = []
                for row in results:
                    eid, name, wage, hrs = row
                    if hrs <= 40:
                        payout = wage * hrs
                    else:
                        ot_pay = (hrs - 40) * 1.5 * wage
                        payout = (wage * 40) + ot_pay

                    emp = (eid, name, wage, hrs, payout)
                    dataList.append(emp)

                # Redirect to the department page to display the updated data
                data = {"rows": dataList, "dept": dept}
                return template("show_department", data)
            
            else:
                # Return a message if no data is found for the given department
                return "No data found for the selected department."

        except db.Error as e:
            # Handle database errors
            return f"Database Error Occurred. Error: {e}"

        finally:
            cur.close()
            conn.close()


# Edit Employee Data Tab
@route("/editHours", method = ["GET", "POST"])
def edit_hrs():
    if request.method == "GET":
        return template("edit_hours")
    else:
        hrs = request.forms.get("hrs")
        eid = request.forms.get("eid")
        name = request.forms.get("name")
        dept = request.forms.get("dept")

        try:
            conn = db.connect("payroll.db")
            cur = conn.cursor()

            
            
            # Update the hours worked for the employee
            sql = '''UPDATE pay_data 
                    SET hrs_worked = ? 
                    WHERE emp_id = ?'''
            cur.execute(sql, (hrs, eid))
            conn.commit()

            cur.execute("SELECT emp_name, department FROM employees WHERE emp_id = ?", (eid,))
            row = cur.fetchone()
            name = row[0]
            dept = row[1]

            # Redirect to the status page to display a confirmation for the user
            data = {"eid": eid, "hrs": hrs, "name": name, "dept": dept}
            return template("status", data)

        # Error Handling
        except db.Error as e:
            return f"Database Error Occurred. Error: {e}"

        finally:
            cur.close()
            conn.close()
    

run(host = "localhost", port = 8080)
