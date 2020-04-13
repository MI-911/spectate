#!flask/bin/python
from data_sources.aggregating_data_source import AggregatingDataSource
from data_sources.local_data_source import LocalDataSource
from flask import Flask, jsonify

app = Flask(__name__)
source = AggregatingDataSource([LocalDataSource('/results')])


@app.route('/experiments')
def experiments():
    return jsonify(list(source.experiments()))


@app.route('/results/<experiment>/<metric>/<cutoff>')
def results(experiment, metric, cutoff):
    return jsonify(source.results(experiment, metric, cutoff))


if __name__ == "__main__":
    app.run()
