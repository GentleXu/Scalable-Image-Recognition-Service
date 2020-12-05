
# web servers
app = Flask(__name__)

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 11111), app)
    http_server.serve_forever()
    app.run()