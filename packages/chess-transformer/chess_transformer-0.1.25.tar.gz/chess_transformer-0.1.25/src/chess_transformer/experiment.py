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
    os.makedirs(self.path, exist_ok=self.mode != 'new')
    mode = 'w' if self.mode == 'replace' else 'x'

    if self.mode != 'append':
      with open(f'{self.path}/params.json', mode) as f:
        json.dump(self.params, f)
        
      with open(f'{self.path}/logs.csv', mode) as f:
        f.write('step,loss\n')

  def log(self, step: int, loss: float):
    with open(f'{self.path}/logs.csv', 'a') as f:
      f.write(f'{step},{loss}\n')
