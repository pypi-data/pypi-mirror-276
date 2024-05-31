import math
from jaxtyping import Float
import torch

def positional_encoding(max_len: int, d_model: int) -> Float[torch.Tensor, 'max_len d_model']:
  position = torch.arange(max_len)[:, None]
  div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
  pe = torch.zeros(max_len, d_model)
  pe[:, 0::2] = torch.sin(position * div_term)
  pe[:, 1::2] = torch.cos(position * div_term)
  return pe
