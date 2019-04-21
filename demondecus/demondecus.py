import flask, note_generator, json

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return flask.render_template('demondecus.html')

@app.route('/predict_note')
def predict_note():
    notes, composer = json.loads(flask.request.args.get('notes')), flask.request.args.get('composer')
    print(notes)
    return flask.jsonify({'result':note_generator.NoteGenerator.get_note(notes, composer)})

if __name__ == '__main__':
    app.debug = True
    app.run()
