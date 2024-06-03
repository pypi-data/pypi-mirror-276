from typing import Sequence, TypedDict
import numpy as np
from haskellian import iter as I

class Metrics(TypedDict):
  acc: float
  game_acc: float

def accuracy(labs: Sequence[str], preds: Sequence[str]):
  return len([1 for lab, pred in zip(labs, preds) if lab == pred]) / len(labs)

def game_accuracy(labs: Sequence[str], preds: Sequence[str]):
  return I.take_while(lambda x: x[0] == x[1], zip(labs, preds)).len() / len(labs)

def metrics(fen_labs: Sequence[str], fen_preds: Sequence[str]) -> Metrics:
  return Metrics(
    acc=accuracy(fen_labs, fen_preds),
    game_acc=game_accuracy(fen_labs, fen_preds)
  )

def batch_metrics(fen_labs: Sequence[Sequence[str]], fen_preds: Sequence[Sequence[str]]) -> Metrics:
  sample_metrics = [metrics(labs, preds) for labs, preds in zip(fen_labs, fen_preds)]
  return {
    k: np.mean(I.pluck(sample_metrics, k)) # type: ignore
    for k in sample_metrics[0].keys()
  } # type: ignore
