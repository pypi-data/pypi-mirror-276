from typing import Literal
from dataclasses import dataclass
import os
import json

@dataclass
class Experiment:
  path: str
  params: dict
  mode: Literal['replace', 'append', 'new'] = 'new'

  def __post_init__(self):

    self.created = {}
    os.makedirs(self.path, exist_ok=self.mode != 'new')
    mode = 'w' if self.mode == 'replace' else 'x'

    if self.mode != 'append':
      with open(f'{self.path}/params.json', mode) as f:
        json.dump(self.params, f)

  def _create_log(self, metric: str):
    mode = 'w' if self.mode == 'replace' else 'x'
    with open(f'{self.path}/{metric}.csv', mode) as f:
      f.write(f'step,{metric}\n')

  def log(self, metric: str, step: int, value: float):
    if metric not in self.created and self.mode != 'append':
      self._create_log(metric)
      self.created[metric] = True

    with open(f'{self.path}/{metric}.csv', 'a') as f:
      f.write(f'{step},{value}\n')
