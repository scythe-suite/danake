from csv import reader
from itertools import cycle
from os import environ
from pathlib import Path
from secrets import token_urlsafe

import docker

DANAKE_VERSION = environ['DANAKE_VERSION']
EDITOR_IMAGE = '127.0.0.1:5000/danake/editor:' + DANAKE_VERSION

UID2INFO_PATH = '/confs/uid2info.tsv'
UID2INFO = dict(reader(Path(UID2INFO_PATH).open('r'), delimiter = '\t'))
UIDS = sorted(UID2INFO.keys())

connection = docker.from_env()

HOSTS = sorted(node.attrs['Description']['Hostname'] for node in connection.nodes.list())

print('starteditor: found hosts:', HOSTS)

for uid, host in list(zip(UIDS, cycle(HOSTS))):
    print('starteditor: creating service: editor-{}@{}'.format(uid, host))
    connection.services.create(
        image = EDITOR_IMAGE,
        name = 'editor-{}'.format(uid),
        constraints = ['node.hostname=={}'.format(host)],
        mounts = ['editor-{}-volume:/home/coder/project'.format(uid)],
        networks = ['danake_backend_network'],
        labels = {'danake': 'editor'}
    )