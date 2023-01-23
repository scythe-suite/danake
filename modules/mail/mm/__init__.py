from csv import reader
from os import environ
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
  lines = list(data.splitlines())
  if len(lines) < 2: raise ValueError("Merge data must contain at least two lines: one header and at least one record.")
  badre = re.compile(r'[^A-Za-z0-9]+')
  headers, *rows = list(reader((_.strip() for _ in lines if _.strip()), delimiter = '\t'))
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
def token():
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
    if token == 'test':
      status = 'OK'
      info = {'name': 'Test Account', 'mail': 'test@email.me'}
    elif not token:
      status = 'MISSING_TOKEN'
    else:
      try:
          info = USTS.loads(token, max_age = app.config['TOKEN_DURATION'])
      except SignatureExpired:
          status = 'EXPIRED_TOKEN'
      except BadSignature:
          status = 'INVALID_TOKEN'
    if status != 'OK' or request.method == 'GET':
      return render_template('index.html', status = status, info = info)
    else:
      subject = request.form['subject']
      if not subject: subject = '[∂anake]: Mail merge from {}'.format(info['name'])
      text = request.form['text']
      if not text: return {'title': 'Missing data', 'body': 'Please provide the text for your message!'}
      if not request.form['data']: return {'title': 'Missing data', 'body': 'Please provide the merge data for your mails!'}
      try:
        data = data2dicts(request.form['data'])
      except (Exception, OSError) as err:
        return {'title': 'Error while processing merge data', 'body': 'The following error has been reported while processing merge data:\n<div class="reason">{}</div>'.format(err)}
      try:
        msgs = [make_message(dct, (info['name'], info['mail']), subject, text) for dct in data]
      except (Exception, OSError) as err:
        return {'title': 'Error while merging', 'body': 'The following error has been reported while preparing messages:\n<div class="reason">{}</div>'.format(err)}
      if request.form['mode'] == 'send':
        if token == 'test':
          return {'title': 'Test', 'body': 'It you had a valid token, {} emails would have been sent.'.format(len(data))}
        try:
          with mail.connect() as conn:
            for msg in msgs: conn.send(msg)
        except (Exception, OSError) as err:
          return {'title': 'Error while sending', 'body': 'The following error has been reported while sending:\n<div class="reason">{}</div>'.format(err)}
        return {'title': 'Success', 'body': 'Sent {} emails.'.format(len(data))}
      else:
        examples = '\n'.join(['First (at most) three of {} message(s):'.format(len(data))] + [
          '<pre class="mail-msg">{}</pre>'.format(msg.as_string()) for msg in msgs[:3]
        ])
        return {'title': 'Example messages', 'body': examples}