from flask import Flask, flash, request, redirect, url_for, render_template
import ProgramUtama

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()