from token_storage import *
from flask import *
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CDN_ROUTE = 'cdn'

CLIENT_ID = '875289893188816946'
CLIENT_SECRET = client_secret
REDIRECT_URI = 'https://automodsolutions.ru/auth/callback'
API_BASE_URL = 'https://discord.com/api/v10'
OAUTH2_URL = f'{API_BASE_URL}/oauth2/authorize'
TOKEN_URL = f'{API_BASE_URL}/oauth2/token'
USER_URL = f'{API_BASE_URL}/users/@me'


@app.route("/")
def home():
    user = session.get('user')
    return render_template("home.html", user=user)


@app.route('/<filename>')
def serve_image(filename):
    try:
        return send_from_directory(CDN_ROUTE, filename)
    except FileNotFoundError:
        abort(404)


@app.route('/cdn/add')
def redirect_example():
    return redirect('https://youtu.be/dQw4w9WgXcQ?si=j8BRGXXxEKTwCZ75')


@app.route('/auth')
def authorize():
    return render_template('authorize.html')


@app.route('/alt')
def alternative_site():
    return render_template('alt_site.html')


@app.route('/auth/login')
def login():
    return redirect(f'{OAUTH2_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify')


@app.route('/auth/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # По идее здесь токен нада вытащить
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    token = response.json().get('access_token')

    # Вытаскиваем инфу
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(USER_URL, headers=headers)
    response.raise_for_status()
    user_info = response.json()

    session['user'] = {
        'id': user_info['id'],
        'username': user_info['username'],
        'avatar': user_info['avatar']
    }

    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('auth'))


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5795)
