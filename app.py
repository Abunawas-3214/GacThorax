from flask import Flask, flash, request, redirect, url_for, render_template
import os
import shutil
from threading import Thread
from ProgramUtama import GAC

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def delete_files():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

class startProcess():
    def __init__(self, filename):
        self.filename = filename

    def segproc(self):
        GAC(self.filename)

    def run(self):
        self.segproc()

@app.route('/')
def home():
    delete_files()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        delete_files()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload.jpg'))
        t = Thread(target=startProcess(file.filename).run())
        t.start()
        # accuration = GAC(file.filename)
        # flash(accuration)
        flash('Nice Try')
        return render_template('index.html', filename='result.jpg')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/result')
def result():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()