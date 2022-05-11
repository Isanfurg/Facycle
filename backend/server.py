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
import numpy

def check_path(path):
    if not os.path.exists('backend/'+path):
        os.makedirs('backend/'+path)

def count_path(path):
    initial_count = 0
    for path in pathlib.Path(".").iterdir():
        if path.is_file():
            initial_count += 1
    return initial_count


def read_images(path, image_size):
    names = []
    training_images, training_labels = [], []
    label = 0
    for dirname, subdirnames, filenames in os.walk(path):
        for subdirname in subdirnames:
            names.append(subdirname)
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                img = cv2.imread(os.path.join(subject_path, filename),
                                 cv2.IMREAD_GRAYSCALE)
                if img is None:
                    # El archivo no puede ser cargado como imagen.
                    # Saltarlo.
                    continue
                img = cv2.resize(img, image_size)
                training_images.append(img)
                training_labels.append(label)
            label += 1
    training_images = numpy.asarray(training_images, numpy.uint8)
    training_labels = numpy.asarray(training_labels, numpy.int32)
    return names, training_images, training_labels    
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'facycle'
}

app = Flask(__name__)
app.config["DEBUG"] = True

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

@app.route('/api/upload/<email>/<i>', methods=['POST'])
def uploadImage(email,i):
    path_save="uploads/"+email
    check_path(path_save)
    if request.method == 'POST':
        app.config['UPLOAD_FOLDER'] = path_save
        base64_png =  request.form['image']
        code = base64.b64decode(base64_png.split(',')[1]) 
        image_decoded = Image.open(BytesIO(code))
        name = 'backend/'+path_save+'/image'+str(int(i)+1)+'.png'
        image_decoded.save(name )
        return jsonify({'result': 'success'})
    return jsonify({'result': 'error in upload'})
@app.route('/api/recognize', methods=['POST'])
def checkFace():
    path_save="backend/uploads/"
    if request.method == 'POST':
        app.config['UPLOAD_FOLDER'] = 'backend/data'
        base64_png =  request.form['image']
        code = base64.b64decode(base64_png.split(',')[1]) 
        image_decoded = Image.open(BytesIO(code))
        name = 'backend/data/image.png'
        
        image_decoded.save(name)
    
        training_image_size = (400, 300)
        names, training_images, training_labels = read_images(
            path_save, training_image_size)

        model = cv2.face.EigenFaceRecognizer_create()
        model.train(training_images, training_labels)

        face_cascade = cv2.CascadeClassifier(
            'backend/cascadas/haarcascade_frontalface_default.xml')
        camera = cv2.imread('backend/data/image.png')
        gray = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(camera, (x, y), (x+w, y+h), (255, 0, 0), 2)
            gray = cv2.cvtColor(camera, cv2.COLOR_BGR2GRAY)
            roi_gray = gray[x:x+w, y:y+h]
            if roi_gray.size == 0:
                        # La ROI esta vacia o la imagen en un borde.
                        # Saltarla.
                continue
            roi_gray = cv2.resize(roi_gray, training_image_size)
            label, confidence = model.predict(roi_gray)
            text = '%s, confianza=%.2f' % (names[label], confidence)
            cv2.putText(camera, text, (x, y - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imwrite('backend/data/final.jpg', camera)
            
            return jsonify({'confidence': confidence, 'response': 'ok'})
            
    return jsonify({'No encontrado'})
app.run()