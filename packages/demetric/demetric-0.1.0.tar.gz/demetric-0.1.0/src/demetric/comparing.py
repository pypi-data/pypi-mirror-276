from typing import Sequence
from .experiment import Experiment
from . import plot

def compare(experiments: Sequence[Experiment], metric: str):
  p = plot.metrics({ e.id: e.read(metric) for e in experiments })
  p.ax.set_title(f'{metric} comparison')
  p.ax.legend()
  p.ax.set_xlabel('step')
  p.ax.set_ylabel(metric)
  return p