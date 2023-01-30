from recognition import app, db
import os
from flask import render_template, redirect, url_for
from flask_login import current_user, login_user, login_required
from recognition.models import Recognition
from recognition.forms import RecognitionForm
from recognition.recognizer import recognizer
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
            return redirect(url_for('recognize'))
    return render_template('recognize.html', form=form)


@app.route('/prediction',methods=['GET', 'POST'])
@login_required
def prediction():
    image_file = url_for(
        'static', filename='pictures/' + current_user.picture_name)
    classes = ["क-ka","ख-kha","ग-ga","घ-gha","ङ-Ṅa","च-cha","छ-chha","ज-ja","झ-jha","ञ-yna","ट-ta","ठ-tha","ड-da","ढ-dha","ण-ana","त-ta","थ-tha","द-da","ध-dha","न-na","प-pa","फ-pha","ब-ba","भ-bha","म-ma","य-ya","र-ra","ल-la","व-wa","श-sha","ष-shha","स-sa","ह-ha","क्ष-ksha","त्र-tra","ज्ञ-gya","०-0","१-1","२-2","३-3","४-4","५-5","६-6","७-7","८-8","९-9"]
    prediction = classes[current_user.picture_prediction]
    return render_template('prediction.html', image_file = image_file, prediction=prediction)