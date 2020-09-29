from logic import table, the_maker
from flask import Flask, jsonify, json
import flask
from flask.templating import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return open('src/index.html').read()

@app.route('/concorrentes')
def concorrentes_sumario():
    out = the_maker.maker().get_list()
    return jsonify(out)

@app.route('/concorrentes/pagina')
def concorrente_by_pag():
    pag = flask.request.args.get('pagina')
    out = the_maker.maker().get_pag(int(pag)-1)
    return jsonify(out)

@app.route('/concorrentes/codigo')
def concorrentes_by_id():
    codigo = flask.request.args.get('codigo')
    out = the_maker.maker().get_place_json(int(codigo))
    return jsonify(out)

if __name__ == '__main__':
    app.run()