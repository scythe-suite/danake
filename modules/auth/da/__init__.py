from csv import reader
import os
from pathlib import Path

import click
from flask import Flask, abort, jsonify, redirect, render_template, request, url_for
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

__version__ = '0.1.0-beta'

app = Flask(__name__, instance_relative_config = True)
app.config.from_mapping(
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024,
    PICTURES_FOLDER = '/pictures',
    UID2INFO_PATH = '/uid2info.tsv',
    COOKIE2UID_PATH = '/cookie2uid.map',
    SECRET_KEY = 'dev-only-key',
    COOKIE_DURATION = 60 * 60 * 4, # 4h
    TOKEN_DURATION = 60 * 60 * 5 # 5h
)
app.config.from_pyfile('config.py', silent = True)
app.config.from_pyfile('/config.py', silent = True)

USTS = URLSafeTimedSerializer(app.config['SECRET_KEY'])

UID2INFO = dict(
  reader(Path(app.config['UID2INFO_PATH']).open('r'), delimiter = '\t')
)
UID2COOKIE = dict(
  (uid[:-1], cookie) for cookie, uid in reader(Path(app.config['COOKIE2UID_PATH']).open('r'), delimiter = '\t')
)

Path(app.instance_path).mkdir(exist_ok = True)
PICTURES_FOLDER_PATH = Path(app.config['PICTURES_FOLDER']).absolute()
PICTURES_FOLDER_PATH.mkdir(exist_ok = True, parents = True)

@app.cli.command("get-token")
@click.argument("uid")
def get_token(uid):
    print(USTS.dumps(uid))

@app.cli.command("get-cookie")
@click.argument("uid")
def get_cookie(uid):
    print(UID2COOKIE[uid])

@app.route('/stats')
def stats():
    files = list(map(lambda p: str(p.relative_to(PICTURES_FOLDER_PATH)), PICTURES_FOLDER_PATH.rglob('*.png')))
    return {
        'info': {'pictures': len(files), 'uids': len(UID2INFO)},
        'uid2info': UID2INFO,
        'pictures': files,
    }

@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:token>', methods=['GET', 'POST'])
def index(token = None):
    status = None
    info = None
    if not token:
        status = 'MISSING_TOKEN'
    else:
        try:
            uid = USTS.loads(token, COOKIE_DURATION = app.config['TOKEN_DURATION'])
        except SignatureExpired:
            status = 'EXPIRED_TOKEN'
        except BadSignature:
            status = 'INVALID_TOKEN'
        else:
            try:
                info = UID2INFO[uid]
            except KeyError:
                status = 'UNREGISTERED_UID'
            else:
                status = 'OK'
    if status == 'OK':
      dst = PICTURES_FOLDER_PATH / (uid + '.png')
      if dst.exists(): return redirect('/cs/')
      if request.method == 'POST':
          if 'photo' not in request.files: abort(400)
          file = request.files['photo']
          try:
              fd = os.open(str(dst), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
          except OSError as e:
              if e.errno == os.EEXIST:
                  return redirect('/cs/')
              else:
                  raise
          fobj = os.fdopen(fd, 'wb')
          try:
              file.save(fobj)
              fobj.close()
          except OSError:
              abort(500)
          return jsonify({
            'status': 'ok',
            'cookie': f'danake_routing={UID2COOKIE[uid]}; Max-Age={app.config["COOKIE_DURATION"]}; Path=/; Secure; SameSite=Strict' })
    return render_template('index.html', status = status, info = info)
