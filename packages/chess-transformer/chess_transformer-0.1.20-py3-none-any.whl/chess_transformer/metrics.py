from typing import Sequence

def accuracy(labs: Sequence[str], preds: Sequence[str]) -> float:
  """Proportion of correct predictions."""
  return sum(l == p for l, p in zip(labs, preds)) / len(labs)

def uci_accuracy(labs: Sequence[str], preds: Sequence[str]) -> float:
  """Proportion of correct UCI predictions."""
  return sum((l == p or l == p[:4]) for l, p in zip(labs, preds)) / len(labs)