import random
from flask import Flask , render_template, url_for , redirect , request
import string
import db 

app = Flask(__name__)

from urllib.parse import urlparse

db.init_db() 

def normalize_url(raw):
    url = raw.strip()
    if not url or len(url) > 2048:
        return None

    if "://" not in url:
        url = "https://" + url

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return None
    if not parsed.netloc or "." not in parsed.netloc:
        return None
    return url

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = normalize_url(request.form.get('long_url', ''))
        if long_url is None:
            return render_template('index.html',
                                   error="Please enter a valid URL."), 400
        if not db.check_short(long_url):
            short_url = db.generate()
            while short_url in db.get_all_urls():
                short_url = db.generate()
            db.link_to_long(long_url, short_url)
        else:
            short_url = db.check_short(long_url)
        return render_template('index.html', short_url=request.url_root + short_url)
    return render_template('index.html')

@app.route('/<short_url>') 
def redirect_url(short_url):
    long_url = db.check_long(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

@app.route('/check-long', methods=['GET', 'POST'])
def check_long():
    long_url = None
    if request.method == 'POST':
        raw = request.form.get('short_url', '').strip()
        code = raw.rstrip('/').rsplit('/', 1)[-1]   # accepts full short URL or just the code
        long_url = db.check_long(code)
    return render_template('check_long.html', long_url=long_url)

@app.route('/check-short', methods=['GET', 'POST'])
def check_short():
    short_url = None
    if request.method == 'POST':
        long_url = normalize_url(request.form.get('short_url', ''))
        if long_url:
            short_url = db.check_short(long_url)
    return render_template('check_short.html', short_url=short_url)

if __name__ == '__main__':
    app.run(debug=True , port = 5005)

