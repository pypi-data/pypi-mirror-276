from typing import Sequence
from jaxtyping import Float, Int
from torch import Tensor, nn
import torch
from .._loss import segmented_loss
from ... import uci
from .decode import argmax_ucis

def loss(
  logits: Float[Tensor, 'batch seq_len 36'],
  labels: Int[Tensor, 'batch seq_len 5'], *,
  ce_loss: nn.CrossEntropyLoss = nn.CrossEntropyLoss(ignore_index=-100)
) -> Float[Tensor, '']:
  losses = segmented_loss(logits, labels, loss=ce_loss, ends=[8, 16, 24, 32, 36])
  return sum(l for l in losses if not torch.isnan(l)) # type: ignore
  # nan may happen if all promotion labels are -100 (which is quite likely)

def metrics(sample_logits: Float[Tensor, 'L 5'], true_ucis: Sequence[str]) -> uci.Metrics:
  pred_ucis = argmax_ucis(sample_logits)
  return uci.metrics(true_ucis, pred_ucis[0])