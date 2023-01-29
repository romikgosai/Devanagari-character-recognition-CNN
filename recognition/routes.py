from recognition import app
import os
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, login_required
from recognition.models import Recognition
from recognition.forms import RecognitionForm
from recognition.recognizer import recognizer
from recognition import db
from PIL import Image
import secrets
import numpy as np



def save_recognition_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(
        app.root_path, 'static\\pictures\\', picture_fn)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/', methods=['GET','POST'])
@app.route('/recognize', methods=['GET','POST'])
def recognize():
    form = RecognitionForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_recognition_picture(form.picture.data)
            recognition = Recognition(picture_name=picture_file,picture_prediction=recognizer(os.path.dirname(__file__)+'\\static\\pictures\\'+picture_file))
            db.session.add(recognition)
            db.session.commit()
            login_user(recognition)
            return redirect(url_for('prediction')) 
        else:
            return redirect(url_for('prediction'))
    return render_template('recognize.html', form=form)


@app.route('/prediction',methods=['GET', 'POST'])
@login_required
def prediction():
    image_file = url_for(
        'static', filename='pictures/' + current_user.picture_name)
    classes = ["क","ख","ग","घ","ङ","च","छ","ज","झ","ञ","ट","ठ","ड","ढ","ण","त","थ","द","ध","न","प","फ","ब","भ","म","य","र","ल","व","श","ष","स","ह","क्ष","त्र","ज्ञ","०","१","२","३","४","५","६","७","८","९"]
    prediction = classes[current_user.picture_prediction]
    return render_template('prediction.html', image_file = image_file, prediction=prediction)