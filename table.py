from csv import reader
from pathlib import Path
from sys import exit

import docker
from itsdangerous import URLSafeTimedSerializer

CONFS_PATH = 'confs/auth-config.py'
UID2INFO_PATH = 'confs/uid2info.tsv'
COOKIE_MAP_PATH = 'confs/cookie2ip.tsv'

UID2INFO = dict(reader(Path(UID2INFO_PATH).open('r'), delimiter = '\t'))

CONFS = {}
with open(CONFS_PATH, "r") as inf:
  exec(inf.read(), CONFS)

USTS = URLSafeTimedSerializer(CONFS['SECRET_KEY'])

client = docker.from_env()
service = client.services.get('danake_code-server')

IPS = [task['NetworksAttachments'][0]['Addresses'][0].split('/')[0] for task in service.tasks({'desired-state': 'running'})]

if len(IPS) != len(UID2INFO):
  exit(f'Scale code-server to {len(UID2INFO)} with:\n\n\tdocker service scale danake_code-server={len(UID2INFO)}')

Path(COOKIE_MAP_PATH).write_text('\n'.join((f'{USTS.dumps(info)}\t{ip};' for ip, info in zip(IPS, UID2INFO.values()))))
#secrets.token_urlsafe(32)