from typing import Sequence

def accuracy(labs: Sequence[str], preds: Sequence[str]) -> float:
  """Proportion of correct predictions."""
  return sum(l == p for l, p in zip(labs, preds)) / len(labs)