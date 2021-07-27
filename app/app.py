from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'citiesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Cities Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblcitiesImport1')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<City>', methods=['GET'])
def record_view(City):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblcitiesImport1 WHERE id=%s', City)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<City>', methods=['GET'])
def form_edit_get(City):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblcitiesImport1 WHERE id=%s', City)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:City>', methods=['POST'])
def form_update_post(City):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('latD'), request.form.get('latM'), request.form.get('latS'),
                 request.form.get('nS'), request.form.get('lonD'),
                 request.form.get('lonM'), request.form.get('lonS'),
                 request.form.get('eW'), request.form.get('city'), request.form.get('state'), City)
    sql_update_query = """UPDATE tblcitiesImport1 t SET t.latD = %s, t.latM = %s, t.latS = %s, t.nS = 
    %s, t.lonD = %s, t.lonM = %s, t.lonS = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New City Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'))
    sql_insert_query = """INSERT INTO tblcitiesImport1 (latD,latM,latS,nS, lonD,lonM,lons,eW,city,state) 
    VALUES (%s, %s,%s, %s,%s, %s,%s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:city>', methods=['POST'])
def form_delete_post(city):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblcitiesImport1 WHERE id = %s """
    cursor.execute(sql_delete_query, city)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblcitiesImport1')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city>', methods=['GET'])
def api_retrieve(city) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblcitiesImport1 WHERE id=%s', city)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/edit/<int:city>', methods=['GET'])
def form_edit_get(city):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblcitiesImport1 WHERE id=%s', city)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city>', methods=['POST'])
def form_update_post(city):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('LatD'), request.form.get('LatM'), request.form.get('LatS'),
                 request.form.get('NS'), request.form.get('LonD'),
                 request.form.get('LonM'), request.form.get('LonS'), request.form.get('EW'),
                 request.form.get('city'), request.form.get('State'), city)
    sql_update_query = """UPDATE tblcitiesImport1 t SET t.latD = %s, t.latM = %s, t.latS = %s, t.nS = 
    %s, t.lonD = %s, t.lonM = %s, t.lonS = %s WHERE t.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New city Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldName'), request.form.get('fldLat'), request.form.get('fldLong'),
                 request.form.get('fldCountry'), request.form.get('fldAbbreviation'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'))
    sql_insert_query = """INSERT INTO tblcitiesImport1 (latD,latM,latS,nS, lonD,lonM,lons,eW,city,state)
     VALUES (%s, %s,%s, %s,%s, %s,%s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:city>', methods=['POST'])
def form_delete_post(city):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblcitiesImport1 WHERE id = %s """
    cursor.execute(sql_delete_query, city)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblcitiesImport1')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city>', methods=['GET'])
def api_retrieve(city) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblcitiesImport1 WHERE id=%s', city)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city>', methods=['PUT'])
def api_edit(city) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/cities/<int:city>', methods=['DELETE'])
def api_delete(city) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

