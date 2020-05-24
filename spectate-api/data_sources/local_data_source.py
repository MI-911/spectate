import json
import math
import os
from collections import defaultdict
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

            question_score = defaultdict(list)
            for split in sorted(os.listdir(model_path)):
                if not split.endswith('.json'):
                    continue

                with open(os.path.join(model_path, split), 'r') as fp:
                    model_result = json.load(fp)

                    for key, scores in model_result.items():
                        score = scores[metric][cutoff]

                        # Since JSON cannot parse NaN treat all occurrences as zero
                        question_score.setdefault(key, []).append(0 if math.isnan(score) else score)

            # Return sorted by question number
            model_scores[model] = [pair[1] for pair in sorted(question_score.items(), key=lambda x: int(x[0]))]

        return model_scores
