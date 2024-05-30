from typing import Sequence, Literal
from jaxtyping import Float
from haskellian import iter as I
import torch

def segment_encoding(
  seq_len: int, /, *, ends: Sequence[int],
  encoding: Float[torch.Tensor, 'max_len d_model']
) -> Float[torch.Tensor, 'seq_len d_model']:

  hidden_size = encoding.size(1)
  output = torch.zeros(seq_len, hidden_size, dtype=encoding.dtype, device=encoding.device)
  
  for i, (start, end) in I.pairwise([0, *ends]).enumerate():
    output[:, start:end] = encoding[:seq_len, i][..., None]

  return output

def pool_sample(
  embeds: Float[torch.Tensor, 'seq_len hidden_size'],
  word_ends: Sequence[int], *,
  num_moves: int,
  mode: Literal['mean', 'max'] = 'max'
) -> Float[torch.Tensor, 'num_moves hidden_size']:
  pool = torch.mean if mode == 'mean' else (lambda x, dim: torch.max(x, dim).values)
  output = torch.zeros(num_moves, embeds.size(1), dtype=embeds.dtype, device=embeds.device)
  for start, end in I.pairwise([0, *word_ends]):
    output[start:end] = pool(embeds[start:end], dim=0)
  return output

def pool_batch(
  embeds: Float[torch.Tensor, 'batch seq_len hidden_size'],
  word_ends: Sequence[Sequence[int]],
  *, mode: Literal['mean', 'max'] = 'max'
) -> Float[torch.Tensor, 'batch num_moves hidden_size']:
  
  max_moves = max(len(ends) for ends in word_ends)
  return torch.stack([
    pool_sample(embed, ends, mode=mode, num_moves=max_moves)
    for embed, ends in zip(embeds, word_ends)
  ])