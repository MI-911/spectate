#!flask/bin/python
import os
import sys

from flask_cors import CORS
from loguru import logger

from data_sources.aggregating_data_source import AggregatingDataSource
from data_sources.empty_data_source import EmptyDataSource
from data_sources.local_data_source import LocalDataSource
from flask import Flask, jsonify, request

from data_sources.remote_data_source import RemoteDataSource

import numpy as np

from scipy.stats import ttest_rel

app = Flask(__name__)
source = EmptyDataSource()
cors = CORS(app, resources={r"/spectate/*": {"origins": "*"}})
significance_level = 0.05


@app.route('/spectate/experiments')
def experiments():
    return jsonify(list(source.experiments()))


@app.route('/spectate/table/<experiment>/<metric>/<cutoff>')
def table(experiment, metric, cutoff):
    questions = int(request.args.get('questions', 5))
    model_results = source.results(experiment, metric, cutoff)

    rows = [['Model'] + [f'{i + 1}' for i in range(questions)]]

    for model, values in model_results.items():
        row = [model]

        for question_idx in range(len(values)):
            scores = values[question_idx]

            mean = np.mean(scores)
            std = np.std(scores)

            content = f'{mean:.2f}±{std:.2f}'

            to_compare = [scores]
            if question_idx:
                # Compare against values for the previous #questions
                to_compare.append(values[question_idx - 1])

                # In some cases, there may be an uneven amount of splits if testing is still ongoing
                # In these cases, we perform the t-test on the minimum list length
                min_length = len(min(to_compare, key=len))
                p_value = ttest_rel(*[lst[:min_length] for lst in to_compare])[1]

                if p_value < significance_level:
                    content += '*'

            row.append(content)

        print(values)

        rows.append(row)

    return jsonify(rows)


@app.route('/spectate/results/<experiment>/<metric>/<cutoff>')
def results(experiment, metric, cutoff):
    model_results = source.results(experiment, metric, cutoff)

    # Each value is a list containing a score for each split
    # Users can optionally choose to get the arithmetic mean representation of these scores
    if request.args.get('mean') == 'yes':
        for model, values in model_results.items():
            model_results[model] = [np.mean(question_scores) for question_scores in values]

    return jsonify(model_results)


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
