from typing import Sequence, TypedDict
import numpy as np
from haskellian import iter as I
import chess_utils as cu
from ._decode import decode_ucis

def accuracy(labs: Sequence[str], preds: Sequence[str]) -> float:
  """Proportion of correct predictions."""
  return sum(l == p for l, p in zip(labs, preds)) / len(labs)

def uci_accuracy(labs: Sequence[str], preds: Sequence[str]) -> float:
  """Proportion of correct UCI predictions."""
  return sum((l == p or l == p[:4]) for l, p in zip(labs, preds)) / len(labs)

class Metrics(TypedDict):
  uci_acc: float
  san_acc: float
  len_ratio: float

def metrics(uci_labs: Sequence[str], uci_preds: Sequence[str]) -> Metrics:
  san_labs = list(cu.ucis2sans(uci_labs))
  san_preds = list(decode_ucis(uci_preds))
  uci_acc = uci_accuracy(uci_labs, uci_preds)
  san_acc = accuracy(san_labs, san_preds)
  len_ratio = len(san_preds) / len(san_labs)
  return Metrics(uci_acc=uci_acc, san_acc=san_acc, len_ratio=len_ratio)

def batch_metrics(uci_labs: Sequence[Sequence[str]], uci_preds: Sequence[Sequence[str]]) -> Metrics:
  sample_metrics = [metrics(labs, preds) for labs, preds in zip(uci_labs, uci_preds)]
  return {
    k: np.mean(I.pluck(sample_metrics, k)) # type: ignore
    for k in sample_metrics[0].keys()
  } # type: ignore
