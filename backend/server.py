from flask import Flask, request, abort, jsonify, send_from_directory, make_response
import mariadb
import os
import pathlib
from pathlib import Path
from flask_cors import CORS 
from random import *
from PIL import Image
from io import BytesIO
import base64
import cv2

def check_path(path):
    if not os.path.exists(path):
        os.makedirs('backend/'+path)

def count_path(path):
    initial_count = 0
    for path in pathlib.Path(".").iterdir():
        if path.is_file():
            initial_count += 1
    return initial_count
    
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'facycle'
}

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = 'uploads/'
CORS(app)


@app.route('/api/getUsers', methods=['GET'])
def get_users():
    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute("select * from usuario")
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)


@app.route('/api/addUser/<email>/<user>/<pwd>', methods=['GET'])
def add_user(email,user,pwd):
    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    try: 
        cur.execute("INSERT INTO usuario (email,user_name,user_pws) VALUES (?,?,?)", (email,user,pwd))
    except mariadb.Error as e: 
        print(f"Error: {e}")
    # execute a SQL statement
    
    conn.commit() 
    return jsonify({'result': 'success'})

@app.route('/api/upload/<email>', methods=['POST'])
def uploadImage(email):
    path_save="uploads/"+email
    check_path(path_save)
    n_photos=count_path(path_save)
    if request.method == 'POST':
        base64_png =  request.form['image']
        code = base64.b64decode(base64_png.split(',')[1]) 
        image_decoded = Image.open(BytesIO(code))
        name = 'image'+str(n_photos+1)+'.png'
        image_decoded.save(Path(app.config[path_save]) / name )
        return make_response(jsonify({'result': 'success'}))
    return make_response(jsonify({'result': 'error in upload'}), 400)

app.run()