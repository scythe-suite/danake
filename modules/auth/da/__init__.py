from csv import reader
import os
from pathlib import Path

from flask import Flask, Response, abort, jsonify, redirect, render_template, request, send_file, make_response
from jinja2 import pass_context, Template
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from markupsafe import Markup

app = Flask(__name__, instance_relative_config = True)
app.config.from_mapping(
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024,
    PICTURES_FOLDER = '/pictures',
    UID2INFO_PATH = '/uid2info.tsv',
    COOKIE2UID_PATH = '/cookie2uid.map',
    MESSAGES = { # the following are jinja2 templates
      'CAMERA_ERROR': 'Please allow this page to access your webcam, if the camera is busy with another application, try closing such application and reload this page.',
      'OK': '''
                <p>Dear <samp>{{info}}</samp>, welcome to the δanake authentication system.</p>
                <p>
                    In this phase you are required to upload a picture of yourself
                    capturing your face along with one of your valid personal IDs
                    (passport, driving license, national ID card).
                </p>
                <p>
                    When you are ready, please
                    <ol>
                        <li>Click on the <i class="icono-camera"></i> button.</li>
                        <li>
                            Allow this page to use your camera
                            by accepting the permission prompted.
                        </li>
                        <li>
                            The box on the left shows the live video from your camera.
                            Strike a pose next to your personal ID,
                            then press the shutter button <i class="icono-camera"></i>.
                            The image captured will be showed in the box on the right.
                            You can repeat this step as many times as you want
                            (do not worry
                            if the quality of the picture is too low:
                            in such case you will be reached by one of the exam assistants).
                        </li>
                        <li>
                            When your picture is ready to go,
                            click the send button <i class="icono-signIn"></i>
                            and wait to be redirected to the exam system.
                        </li>
                    </ol>
                </p>
            ''',
      'MISSING_TOKEN': 'The <em>token</em> is <strong>missing</strong> in your URL.',
      'EXPIRED_TOKEN': 'The <em>token</em> in your URL is <strong>expired</strong>, contact the service administrator if this should not be the case.',
      'UNREGISTERED_UID': 'The <em>token</em> in your URL corresponds to an <strong>unregistered</strong> <em>user id</em>. Should not this be the case, then contact the service administrator.',
      'INVALID_TOKEN': 'The <em>token</em> in your URL is <strong>invalid</strong>. Should not this be the case, then contact the service administrator.'
    },
    SECRET_KEY = 'dev-only-key',
    COOKIE_DURATION = 60 * 60 * 4, # 4h
    TOKEN_DURATION = 60 * 60 * 5 # 5h
)
app.config.from_pyfile('config.py', silent = True)
app.config.from_pyfile('/config.py', silent = True)

@pass_context
def render_message(context, value):
    return Markup(Template(value).render(context))
app.jinja_env.filters['render_message'] = render_message

for key in 'PICTURES_FOLDER', 'UID2INFO_PATH', 'COOKIE2UID_PATH':
  if not app.config[key].startswith('/'):
    app.config[key] = str(Path(app.instance_path) / app.config[key])

UID2INFO = dict(
  reader(Path(app.config['UID2INFO_PATH']).open('r'), delimiter = '\t')
)

UID2COOKIE = dict(
  (uid[:-1], cookie) for cookie, uid in reader(Path(app.config['COOKIE2UID_PATH']).open('r'), delimiter = '\t')
)

Path(app.instance_path).mkdir(exist_ok = True)
PICTURES_FOLDER_PATH = Path(app.config['PICTURES_FOLDER']).absolute()
PICTURES_FOLDER_PATH.mkdir(exist_ok = True, parents = True)

DANAKE_AUTH = os.environ.get('DANAKE_AUTH', app.config['SECRET_KEY'])

USTS = URLSafeTimedSerializer(app.config['SECRET_KEY'])

@app.route('/picture/<string:uid>')
def picture(uid):
    auth = request.cookies.get('danake_auth')
    if auth is None or auth != DANAKE_AUTH: abort(401)
    dst = PICTURES_FOLDER_PATH / (uid + '.png')
    if not dst.exists(): abort(404)
    return send_file(dst)

@app.route('/pictures/<string:auth>')
def pictures(auth = None):
    if auth is None or auth != DANAKE_AUTH: abort(401)
    uid2info = [(uid, info, (PICTURES_FOLDER_PATH / (uid + '.png')).exists()) for uid, info in sorted(UID2INFO.items())]
    resp = make_response(render_template('pictures.html', uid2info = uid2info))
    resp.set_cookie('danake_auth', DANAKE_AUTH)
    return resp

@app.route('/tokens')
def tokens():
    auth = request.headers.get('X-DANAKE-AUTH')
    if auth is None or auth != DANAKE_AUTH: abort(401)
    return Response(
      '\n'.join('{}\t{}{}'.format(uid, request.url_root, USTS.dumps(uid)) for uid in UID2COOKIE.keys()),
      mimetype = 'text/plain'
    )

@app.route('/stats')
def stats():
    files = list(map(lambda p: str(p.relative_to(PICTURES_FOLDER_PATH)), PICTURES_FOLDER_PATH.rglob('*.png')))
    return {
        'info': {'pictures': len(files), 'uids': len(UID2INFO)},
        'uid2info': UID2INFO,
        'pictures': files,
    }

@app.route('/', methods = ['GET', 'POST'])
@app.route('/<string:token>', methods=['GET', 'POST'])
def index(token = None):
    status = None
    info = None
    if not token:
        status = 'MISSING_TOKEN'
    else:
        try:
            uid = USTS.loads(token, max_age = app.config['TOKEN_DURATION'])
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
        preauth = PICTURES_FOLDER_PATH / (uid + '.preauth')
        if preauth.exists():
            try:
                fd = os.open(str(dst), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except OSError as e:
                if e.errno == os.EEXIST:
                    return redirect('/cs/')
                else:
                    raise
            response = make_response(redirect('/cs/'))
            response.set_cookie(
              'danake_routing', UID2COOKIE[uid],
              max_age = app.config["COOKIE_DURATION"],
              secure = True,
              samesite = 'Strict'
            )
            return response
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
    return render_template('index.html', status = status, info = info, messages = app.config['MESSAGES'])


