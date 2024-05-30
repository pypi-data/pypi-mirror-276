from dataclasses import dataclass
import os
import json

@dataclass
class Experiment:
  path: str
  params: dict
  replace: bool = False

  def __post_init__(self):
    os.makedirs(self.path, exist_ok=self.replace)
    mode = 'w' if self.replace else 'x'
    with open(f'{self.path}/params.json', mode) as f:
      json.dump(self.params, f)

    with open(f'{self.path}/logs.csv', mode) as f:
      f.write('step,loss\n')

  def log(self, step: int, loss: float):
    with open(f'{self.path}/logs.csv', 'a') as f:
      f.write(f'{step},{loss}\n')