from typing import Sequence
from dataclasses import dataclass
import os
from .experiment import Experiment

@dataclass
class Runs:
  base_path: str

  def __post_init__(self):
    os.makedirs(self.base_path, exist_ok=True)

  def experiments(self) -> Sequence[Experiment]:
    return [Experiment(id, self.base_path) for id in os.listdir(self.base_path)]
  
  def experiment(self, id: str) -> Experiment:
    return Experiment(id, self.base_path)