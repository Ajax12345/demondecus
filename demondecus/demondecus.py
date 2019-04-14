import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return flask.render_template('demondecus.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
