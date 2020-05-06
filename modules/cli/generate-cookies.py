from csv import reader
from pathlib import Path
from secrets import token_urlsafe

UID2INFO_PATH = '/confs/uid2info.tsv'
COOKIE2UID_PATH = '/confs/cookie2uid.map'

UID2INFO = dict(reader(Path(UID2INFO_PATH).open('r'), delimiter = '\t'))
UIDS = sorted(UID2INFO.keys())

COOKIES = [token_urlsafe(32) for uid in UIDS]

Path(COOKIE2UID_PATH).write_text('\n'.join(
  f'{cookie}\t{uid};' for cookie, uid in zip(COOKIES, UIDS)
))