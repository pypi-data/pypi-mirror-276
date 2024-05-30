from typing import Sequence
from jaxtyping import Float
import torch
import chess_utils as cu

def decode_file(file: int):
  return chr(file + ord('a'))

def decode_rank(rank: int):
  return str(rank + 1)

def decode_uci(from_file: int, from_rank: int, to_file: int, to_rank: int):
  return decode_file(from_file) + decode_rank(from_rank) + decode_file(to_file) + decode_rank(to_rank)

def argmax_ucis(logits: Float[torch.Tensor, 'B L 37']) -> Sequence[Sequence[str]]:
  batch_size = logits.size(0)
  from_files = torch.argmax(logits[:, :, 0:8].reshape(batch_size, -1, 8), dim=-1)
  from_ranks = torch.argmax(logits[:, :, 8:16].reshape(batch_size, -1, 8), dim=-1)
  to_files = torch.argmax(logits[:, :, 16:24].reshape(batch_size, -1, 8), dim=-1)
  to_ranks = torch.argmax(logits[:, :, 24:32].reshape(batch_size, -1, 8), dim=-1)
  
  return [
    [
      decode_uci(*[int(i.item()) for i in idxs])
      for idxs in zip(from_files[b], from_ranks[b], to_files[b], to_ranks[b])
    ]
    for b in range(batch_size)
  ]

def greedy_pgn(logits: Float[torch.Tensor, 'B L 37']) -> Sequence[Sequence[str]]:
  return [list(cu.ucis2sans(ucis)) for ucis in argmax_ucis(logits)]