import pymysql
from app import app
from config import mysql
from flask import jsonify, render_template
from flask import flash, request, json, redirect, session


#######################################################################################################################
# LOGIN ROUTES
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['ID']
            session['username'] = account['username']
            # Redirect to home page
            return redirect('/GUI')
        else:
            msg = 'INCORRECT CREDENTIALS!'
    return render_template('index.html', msg=msg)


##LOGOUT ROUTE
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect('/')


########################################################################################################################
# GUI ROUTES

# CREATE
@app.route('/GUI/create_student', methods=['GET', 'POST'])
def GUIcreate():
    if request.method == 'GET':
        return render_template('create_student.html')

    if request.method == 'POST':
        try:
            _name = request.form['Name']
            _course = request.form['Course']
            _year = request.form['Year']
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO student_info(Name, Course, Year) VALUES(%s, %s, %s)"
            bindData = (_name, _course, _year)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            return redirect('/GUI')
        except Exception as e:
            print(e)
        finally:
            try:
                cursor.close()
                conn.close()
            except UnboundLocalError:
                return showMessage()

# READ
# READ ALL
@app.route('/GUI')
def GUIView():
    if 'loggedin' in session:
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT ID, Name, Course, Year, PRELIM, MIDTERM, FINALS, remarks FROM student_info")
            studentRows = cursor.fetchall()
            return render_template('list_students.html', students=studentRows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return redirect('/')


# READ SPECIFIC
@app.route('/GUI/<int:ID>')
def RetrieveSingleEmployee(ID):
    if 'loggedin' in session:
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT ID, Name, Course, Year, PRELIM, MIDTERM, FINALS, remarks FROM student_info WHERE ID =%s", ID)
            student = cursor.fetchall()
            if student:
                return render_template('list_student.html', student=student)
            return f"Student with id ={id} Doest exist"
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return redirect('/')


# UPDATE
@app.route('/GUI/update_student/<int:ID>', methods=['GET', 'POST'])
def update(ID):
    if 'loggedin' in session:
        if request.method == 'GET':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT ID, Name, Course, Year, PRELIM, MIDTERM, FINALS, remarks FROM student_info WHERE ID =%s", ID)
            student = cursor.fetchall()
            return render_template('update_student.html', student=student)

        try:
            if request.method == 'POST':
                _id = request.form['ID']
                _prelim = request.form['PRELIM']
                _midterm = request.form['MIDTERM']
                _finals = request.form['FINALS']

                if _prelim and _midterm and _finals and _id:
                    sqlQuery = "UPDATE student_info SET PRELIM=%s, MIDTERM=%s, FINALS=%s WHERE ID =%s"
                    bindData = (_prelim, _midterm, _finals, _id,)
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    cursor.execute(sqlQuery, bindData)
                    conn.commit()
                    return redirect('/GUI')
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return redirect('/')


# DELETE
@app.route('/GUI/delete_student/<int:ID>', methods=['GET'])
def GUIDelete(ID):
    if 'loggedin' in session:
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM student_info WHERE ID =%s", ID)
            conn.commit()
            return redirect('/GUI')
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return redirect('/')


########################################################################################################################
#### API REQUESTS
@app.route('/create_student', methods=['POST'])
def create_student():
    try:
        _json = request.json
        _name = request.form['Name']
        _course = request.form['Course']
        _year = request.form['Year']

        if _name and _course and _year and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO student_info(Name, Course, Year) VALUES(%s, %s, %s)"
            bindData = (_name, _course, _year)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Student ' + _name + ' added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        try:
            cursor.close()
            conn.close()
        except UnboundLocalError:
            return showMessage()


@app.route('/student_info')
def student_info():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID, Name, Course, Year, PRELIM, MIDTERM, FINALS, remarks FROM student_info")
        studentRows = cursor.fetchall()
        respone = jsonify(studentRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/student_info/<int:ID>')
def student_details(ID):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT ID, Name, Course, Year, PRELIM, MIDTERM, FINALS, remarks FROM student_info WHERE ID =%s", ID)
        # cursor.execute(statement)
        studentRow = cursor.fetchone()
        respone = jsonify(studentRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update_student', methods=['PUT'])
def update_student():
    try:
        _json = request.json
        _id = _json['ID']
        _name = request.form['Name']
        _course = request.form['Course']
        _year = request.form['Year']
        _prelim = request.form['PRELIM']
        _midterm = request.form['MIDTERM']
        _finals = request.form['FINALS']
        _remarks = request.form['remarks']

        if _name and _course and _year and _id and request.method == 'PUT':
            sqlQuery = "UPDATE student_info SET PRELIM=%s, MIDTERM=%s, FINALS=%s WHERE ID=%s"
            bindData = (_name, _course, _year, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Student #'+str(_id)+' updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        try:
            cursor.close()
            conn.close()
        except UnboundLocalError:
            return showMessage()


@app.route('/delete_student/<int:ID>', methods=['DELETE'])
def delete_student(ID):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student_info WHERE ID =%s", ID)
        conn.commit()
        respone = jsonify('Student deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


########################################################################################################################
@app.errorhandler(405)
def showMessage(error=None):
    message = {
        'status': 405,
        'message': 'Method not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 405
    app.logger.critical("Critical log info : " + str(respone))
    return respone


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Route not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    app.logger.critical("Critical log info : " + str(respone))
    return respone


@app.errorhandler(400)
def showMessage(error=None):
    message = {
        'status': 400,
        'message': 'Bad Request: ' + request.url,
    }
    respone = jsonify(message)
    app.logger.critical("Critical log info : " + str(respone))
    respone.status_code = 400
    return respone


@app.errorhandler(500)
def showMessage(error=None):
    message = {
        'status': 500,
        'message': 'URL not found: ' + request.url,
    }
    respone = jsonify(message)
    app.logger.critical("Critical log info : " + str(respone))
    respone.status_code = 500
    return respone


if __name__ == "__main__":
    # add "host" data to be able to access it on another PC
    # IP address should be your own IP
    app.run(debug=False, host="26.133.249.88")
