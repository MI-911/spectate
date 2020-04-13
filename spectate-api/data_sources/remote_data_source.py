from typing import Set, Dict

import requests

from data_sources.data_source import DataSource


class RemoteDataSource(DataSource):
    def __init__(self, remote_url: str):
        self.remote_url = remote_url

    def experiments(self) -> Set[str]:
        return set(requests.get(f'{self.remote_url}/experiments').json())

    def results(self, experiment, metric, cutoff) -> Dict:
        return requests.get(f'{self.remote_url}/results/{experiment}/{metric}/{cutoff}').json()
