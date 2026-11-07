import random
from flask import Flask , render_template, url_for , redirect , request
import string

app = Flask(__name__)
shortened = {}

def generate(length = 6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for i in range(length))
    return short_url

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_url = generate() 
        while short_url in shortened :
            short_url = generate()
        shortened[short_url] = long_url
        return f'Shortened URL : {request.url_root}{short_url}' 
    return render_template('index.html')

@app.route('/<short_url>') 
def redirect_url(short_url):
    long_url = shortened.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True , port = 5005)

