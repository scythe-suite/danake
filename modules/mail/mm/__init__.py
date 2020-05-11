from csv import reader
from os import environ
from pathlib import Path
import re

import click
from flask import Flask, Response, abort, render_template, request
from flask_mail import Mail, Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

app = Flask(__name__, instance_relative_config = True)
app.config.from_mapping(
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024,
    SECRET_KEY = 'dev-only-key',
    TOKEN_DURATION = 60 * 60 * 24 * 30 # 1 month
)
app.config.from_pyfile('config.py', silent = True)
app.config.from_pyfile('/config.py', silent = True)
mail = Mail(app)

USTS = URLSafeTimedSerializer(app.config['SECRET_KEY'])
DANAKE_AUTH = environ.get('DANAKE_AUTH', app.config['SECRET_KEY'])

def data2dicts(data):
    badre = re.compile(r'[^A-Za-z0-9]+')
    headers, *rows = list(reader((_.strip() for _ in data.splitlines() if _.strip()), delimiter = '\t'))
    headers = list(map(lambda _: badre.sub('', _).lower(), headers))
    num_headers = len(headers)
    dicts = []
    for n, row in enumerate(rows, 1):
      if len(row) != num_headers: raise ValueError('Row {} contains {} fields, while there are {} headers.'.format(n, len(row), num_headers))
      d = dict(zip(headers, row))
      d.update(dict(enumerate(row)))
      dicts.append(d)
    return dicts

def make_message(dct, sender, subject, text):
  try:
    subject = subject.format(**dct)
  except KeyError as err:
    raise ValueError('Some fields in the subject are not present in merge data ({})'.format(err))
  try:
    body = text.format(**dct)
  except KeyError as err:
    raise ValueError('Some fields in the message text are not present in merge data ({})'.format(err))
  if 'mail' in dct: mail = dct['mail']
  elif 'email' in dct: mail = dct['email']
  else: raise ValueError('There is no field named "mail" or "email" in merge data.')
  return Message(sender = sender, recipients = [mail], body = body, subject = subject)

@app.route('/token', methods = ['POST'])
def tokens():
    auth = request.headers.get('X-DANAKE-AUTH')
    name = request.form.get('name', None)
    mail = request.form.get('mail', None)
    if auth is None or auth != DANAKE_AUTH: abort(401)
    return Response(
      'Token for "{} <{}>":\n\n{}{}\n'.format(
        name,
        mail,
        request.url_root,
        USTS.dumps({'name': name, 'mail': mail})
    ), mimetype = 'text/plain')

@app.route('/', methods = ['GET', 'POST'])
@app.route('/<string:token>', methods=['GET', 'POST'])
def index(token = None):
    status = 'OK'
    info = None
    if not token:
        status = 'MISSING_TOKEN'
    else:
        try:
            info = USTS.loads(token, max_age = app.config['TOKEN_DURATION'])
        except SignatureExpired:
            status = 'EXPIRED_TOKEN'
        except BadSignature:
            status = 'INVALID_TOKEN'
    if request.method == 'GET':
      return render_template('index.html', status = status, info = info)
    else:
      print(request.form)
      subject = request.form['subject']
      if not subject: subject = '[∂anake]: Mail merge from {}'.format(info['name'])
      text = request.form['text']
      if not text: return {'title': 'Error', 'body': 'Please provide the text for your message!'}
      if not request.form['data']: return {'title': 'Error', 'body': 'Please provide the merge data for your mails!'}
      try:
        data = data2dicts(request.form['data'])
      except Exception as err:
        return {'title': 'Error', 'body': str(err)}
      if request.form['mode'] == 'send':
        with mail.connect() as conn:
          for dct in data: conn.send(make_message(dct, (info['name'], info['mail']), subject, text))
        return {'title': 'Success', 'body': 'Sent {} emails.'.format(len(data))}
      else:
        body = ['First (at most) three of {} message(s):'.format(len(data))]
        for dct in data[:3]:
          msg = make_message(dct, (info['name'], info['mail']), subject, text)
          body.append('<pre class="mail-msg">{}</pre>'.format(msg.as_string()))
        mail.send(msg)
        return {'title': 'Example messages', 'body': '\n'.join(body)}