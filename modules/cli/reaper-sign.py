from csv import reader
from os import environ
from subprocess import check_call
from sys import stdin

UID2INFO = dict(reader(stdin, delimiter = '\t'))
UIDS = sorted(UID2INFO.keys())
REAPER_SESSION = environ.get('REAPER_SESSION', '')

for uid in UIDS:
    check_call(['ssh', 'editor-{}'.format(uid), 'curl -sL http://reaper.srv.di.unimi.it/tm/santini/{}/{} | python3 | bash'.format(REAPER_SESSION, uid)])