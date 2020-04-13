import json
import os
from typing import Set, Dict, List

from data_sources.data_source import DataSource


class LocalDataSource(DataSource):
    def __init__(self, base_path: str):
        self.base_path = base_path

    def experiments(self) -> Set[str]:
        experiments = set()

        for item in os.listdir(self.base_path):
            if not os.path.isdir(os.path.join(self.base_path, item)):
                continue

            experiments.add(item)

        return experiments

    def results(self, experiment, metric, cutoff) -> Dict:
        experiment_path = os.path.join(self.base_path, experiment)

        if not os.path.isdir(experiment_path):
            return dict()

        model_scores = dict()
        for model in os.listdir(experiment_path):
            model_path = os.path.join(experiment_path, model)
            if not os.path.isdir(model_path):
                continue

            question_score = dict()
            for split in os.listdir(model_path):
                if not split.endswith('.json'):
                    continue

                with open(os.path.join(model_path, split), 'r') as fp:
                    model_result = json.load(fp)

                    for key, scores in model_result.items():
                        question_score[key] = scores[metric][cutoff]

            model_scores[model] = list(question_score.values())

        return model_scores
