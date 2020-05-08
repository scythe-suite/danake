from csv import reader
from secrets import token_urlsafe
from sys import stdin

UID2INFO = dict(reader(stdin, delimiter = '\t'))
UIDS = sorted(UID2INFO.keys())

COOKIES = [token_urlsafe(32) for uid in UIDS]

print('\n'.join(
  f'{cookie}\t{uid};' for cookie, uid in zip(COOKIES, UIDS)
))