from gevent.pywsgi import WSGIServer
from da import app

http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()