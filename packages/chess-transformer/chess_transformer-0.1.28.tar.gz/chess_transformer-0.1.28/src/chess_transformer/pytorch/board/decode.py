from jaxtyping import Float, Int
from haskellian import iter as I
import chess
import torch
from torch import Tensor, nn
from ...board._labels import decode_board
from .._decode import segmented_argmax
from .._loss import segmented_loss

ENDS = [13*(i+1) for i in range(64)]

def loss(
  logits: Float[Tensor, 'batch seq_len 64*13'],
  labels: Int[Tensor, 'batch seq_len 64'], *,
  ce_loss: nn.CrossEntropyLoss = nn.CrossEntropyLoss(ignore_index=-100)
) -> Float[Tensor, '']:
  """Cross-entropy loss summed across the board squares"""
  losses = segmented_loss(logits, labels, loss=ce_loss, ends=ENDS)
  return sum(l for l in losses if not torch.isnan(l)) # type: ignore

def argmax_boards(logits: Float[torch.Tensor, 'B L 64*13']) -> list[list[chess.Board]]:
  argmaxs = segmented_argmax(logits, ends=ENDS)
  return I.ndmap(decode_board, argmaxs) # type: ignore
