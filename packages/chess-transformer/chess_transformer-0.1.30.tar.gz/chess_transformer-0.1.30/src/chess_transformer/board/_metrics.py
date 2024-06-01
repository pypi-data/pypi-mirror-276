from typing import Sequence, TypedDict
import numpy as np
from haskellian import iter as I
import chess_utils as cu
import chess

class Metrics(TypedDict):
  acc: float
  game_acc: float

def metrics(san_labs: Sequence[str], board_preds: Sequence[chess.Board]) -> Metrics:
  
  if san_labs == []:
    return Metrics(acc=0, game_acc=0)

  equals = 0
  end_correct = None
  board = chess.Board()
  for i, san in enumerate(san_labs):
    if board.board_fen() == board_preds[0].board_fen():
      equals += 1
    elif end_correct is None:
      end_correct = i

    board.push_san(san)

  acc = equals / len(san_labs)
  game_acc = 1 if end_correct is None else end_correct / len(san_labs)

  return Metrics(acc=acc, game_acc=game_acc)

def batch_metrics(san_labs: Sequence[Sequence[str]], board_preds: Sequence[Sequence[chess.Board]]) -> Metrics:
  sample_metrics = [metrics(labs, preds) for labs, preds in zip(san_labs, board_preds)]
  return {
    k: np.mean(I.pluck(sample_metrics, k)) # type: ignore
    for k in sample_metrics[0].keys()
  } # type: ignore
