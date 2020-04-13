from abc import ABC
from typing import Set, Dict, List


class DataSource(ABC):
    # List available experiments
    def experiments(self) -> Set[str]:
        pass

    # Get dict of model -> score for an experiment
    def results(self, experiment, metric, cutoff) -> Dict:
        pass
