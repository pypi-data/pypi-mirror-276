from typing import Sequence
from jaxtyping import Float, Int
from haskellian import iter as I
import torch
from torch import Tensor, nn
from .._decode import segmented_argmax
from .._loss import segmented_loss
from ... import fen

ENDS = [13*(i+1) for i in range(64)]

def loss(
  logits: Float[Tensor, 'batch seq_len 64*13'],
  labels: Int[Tensor, 'batch seq_len 64'], *,
  ce_loss: nn.CrossEntropyLoss = nn.CrossEntropyLoss(ignore_index=-100)
) -> Float[Tensor, '']:
  """Cross-entropy loss summed across the board squares"""
  losses = segmented_loss(logits, labels, loss=ce_loss, ends=ENDS)
  return sum(l for l in losses if not torch.isnan(l)) # type: ignore

def argmax_fens(logits: Float[Tensor, 'B L 64*13']) -> list[list[str]]:
  argmaxs = segmented_argmax(logits, ends=ENDS)
  return I.ndmap(fen.decode_fen, argmaxs) # type: ignore

def metrics(sample_logits: Float[Tensor, 'L 64*13'], true_fens: Sequence[str]) -> fen.Metrics:
  pred_fens = argmax_fens(sample_logits)
  return fen.metrics(true_fens, pred_fens[0])