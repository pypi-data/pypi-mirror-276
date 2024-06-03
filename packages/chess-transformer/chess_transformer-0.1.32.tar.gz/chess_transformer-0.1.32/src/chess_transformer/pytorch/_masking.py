from jaxtyping import Int
import torch
from torch import Tensor

def random_masking(
  batch: Int[Tensor, 'batch maxlen'],
  attn_mask: Int[Tensor, 'batch maxlen'] | None = None,
  *, mask_id: int, mask_prob: float
):
  """Mask `batch` with `mask_id` with probability `mask_prob`.
  - If provided, positions with `attn_mask == 0` are excluded from masking.
  """
  rand = torch.rand(batch.shape)
  indices = (rand < mask_prob) & (attn_mask is None or attn_mask == 1)
  output = batch.clone()
  output[indices] = mask_id
  return output
