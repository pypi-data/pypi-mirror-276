from jaxtyping import Int, Float
from torch import Tensor, nn

def loss(
  logits: Float[Tensor, 'batch seq_len 37'],
  labels: Int[Tensor, 'batch seq_len'], *,
  ce_loss: nn.CrossEntropyLoss = nn.CrossEntropyLoss(ignore_index=-100)
) -> Float[Tensor, 'batch']:
  """Cross-entropy loss across the separate categories
  - `logits[..., 0:8]`: start_file
  - `logits[..., 8:16]`: start_rank
  - `logits[..., 16:24]`: end_file
  - `logits[..., 24:32]`: end_rank
  - `logits[..., 32:37]`: promotion
  """
  split_logits = [
    logits[:, :, 0:8] .reshape(-1, 8),
    logits[:, :, 8:16].reshape(-1, 8),
    logits[:, :, 16:24].reshape(-1, 8),
    logits[:, :, 24:32].reshape(-1, 8),
    logits[:, :, 32:37].reshape(-1, 5),
  ]

  split_labs = [
    labels[:, :, 0].reshape(-1),
    labels[:, :, 1].reshape(-1),
    labels[:, :, 2].reshape(-1),
    labels[:, :, 3].reshape(-1),
    labels[:, :, 4].reshape(-1),
  ]
  losses = [ce_loss(logits, labs) for logits, labs in zip(split_logits, split_labs)]
  return sum(losses) # type: ignore