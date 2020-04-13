from typing import Set, Dict, List

from data_sources.data_source import DataSource


class AggregatingDataSource(DataSource):
    def __init__(self, sources: List[DataSource]):
        self.sources = sources

    def experiments(self) -> Set[str]:
        experiments = set()

        for source in self.sources:
            experiments.update(source.experiments())

        return experiments

    def results(self, experiment, metric, cutoff) -> Dict:
        model_scores = dict()

        for source in self.sources:
            model_scores.update(source.results(experiment, metric, cutoff))

        return model_scores
