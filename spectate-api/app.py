#!flask/bin/python
import os
import sys

from flask_cors import CORS
from loguru import logger

from data_sources.aggregating_data_source import AggregatingDataSource
from data_sources.empty_data_source import EmptyDataSource
from data_sources.local_data_source import LocalDataSource
from flask import Flask, jsonify

from data_sources.remote_data_source import RemoteDataSource

app = Flask(__name__)
source = EmptyDataSource()
cors = CORS(app, resources={r"/spectate/*": {"origins": "*"}})


@app.route('/spectate/experiments')
def experiments():
    return jsonify(list(source.experiments()))


@app.route('/spectate/results/<experiment>/<metric>/<cutoff>')
def results(experiment, metric, cutoff):
    return jsonify(source.results(experiment, metric, cutoff))


def _get_source(src):
    if os.path.exists(src):
        logger.info(f'Using local source {src}')

        return LocalDataSource(src)

    logger.info(f'Using remote source {src}')

    return RemoteDataSource(src)


if __name__ == "__main__":
    sources = os.environ.get('SOURCES', None)
    if not sources:
        logger.error('No sources specified.')

        sys.exit(1)

    source = AggregatingDataSource([_get_source(src) for src in sources.split(';')])

    app.run(host='0.0.0.0')
