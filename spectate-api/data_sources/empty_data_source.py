from typing import Set, Dict

from data_sources.data_source import DataSource


class EmptyDataSource(DataSource):
    def experiments(self) -> Set[str]:
        return set()

    def results(self, experiment, metric, cutoff) -> Dict:
        return dict()
