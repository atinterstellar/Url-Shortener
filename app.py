from flask import Flask , render_template, url_for 
import models as md
import alchemy as sq

app = Flask(__name__)

@app.route('/')
def smth() :
    pass