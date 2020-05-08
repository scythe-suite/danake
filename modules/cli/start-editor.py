from csv import reader
from itertools import cycle
from os import environ
from secrets import token_urlsafe
from sys import stdin

import docker

DANAKE_VERSION = environ['DANAKE_VERSION']
DANAKE_REGISTRY = environ['DANAKE_REGISTRY']

UID2INFO_PATH = '/confs/uid2info.tsv'
UID2INFO = dict(reader(stdin, delimiter = '\t'))
UIDS = sorted(UID2INFO.keys())

connection = docker.from_env()

HOSTS = sorted(node.attrs['Description']['Hostname'] for node in connection.nodes.list())

print('starteditor: found hosts:', HOSTS)

for uid, host in list(zip(UIDS, cycle(HOSTS))):
    print('starteditor: creating service: editor-{}@{}'.format(uid, host))
    connection.services.create(
        image = '{}/editor:{}'.format(DANAKE_REGISTRY, DANAKE_VERSION),
        name = 'editor-{}'.format(uid),
        constraints = ['node.hostname=={}'.format(host)],
        hostname = 'editor-{}'.format(uid),
        mounts = ['editor-{}-volume:/home/coder'.format(uid)],
        networks = ['danake_editor_network'],
        labels = {'danake_role': 'editor', 'danake_host': host}
    )