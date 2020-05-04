from csv import reader
from pathlib import Path
from secrets import token_urlsafe
from itertools import cycle

import docker

UID2INFO_PATH = '/confs/uid2info.tsv'
UID2INFO = dict(reader(Path(UID2INFO_PATH).open('r'), delimiter = '\t'))
UIDS = sorted(UID2INFO.keys())

connection = docker.from_env()
HOSTS = sorted(node.attrs['Description']['Hostname'] for node in connection.nodes.list())

print('deploycs: found hosts:', HOSTS)

for uid, host in list(zip(UIDS, cycle(HOSTS))):
    print('deploycs: creating service: code-server-{}@{}'.format(uid, host))
    connection.services.create(
        image = '127.0.0.1:5000/danake/code-server:latest',
        name = 'code-server-{}'.format(uid),
        constraints = ['node.hostname=={}'.format(host)],
        mounts = ['coder-{}-volume:/home/coder/project'.format(uid)],
        networks = ['danake_backend_network'],
        labels = {'danake': 'code-server'}
    )