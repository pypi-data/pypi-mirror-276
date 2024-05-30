from typing import Sequence
from jaxtyping import Int, Float
import torch
from torch import nn, Tensor
from transformers import BertConfig, BertModel
from ..chars.pos_enc import positional_encoding
from ..chars.segmented import segment_encoding

class CharBert(nn.Module):

  pos_enc: Float[Tensor, 'd_model max_len']
  
  def __init__(
    self, *,
    vocab_size: int,
    max_len: int,
    hidden_size: int = 768,
    attention_heads: int = 12
  ):
    super().__init__()
    # BERT configuration
    self.config = BertConfig(
      vocab_size=vocab_size,
      hidden_size=hidden_size,
      num_attention_heads=attention_heads,
      max_position_embeddings=max_len
    )
    self.register_buffer('pos_enc', positional_encoding(max_len, hidden_size))
    self.embedding = nn.Embedding(vocab_size, hidden_size)
    self.bert = BertModel(self.config)
    self.fc = nn.Linear(hidden_size, 4 * 8 + 5)

  def forward(
    self, input_ids: Int[Tensor, 'batch seq_len'],
    word_ends: Sequence[Sequence[int]]
  ) -> Float[Tensor, 'batch seq_len 37']:
    pos_enc = torch.stack([
      segment_encoding(input_ids.size(1), ends=ends, encoding=self.pos_enc)
      for ends in word_ends
    ])
    embedded: Float[Tensor, 'batch seq_len hidden_size'] = self.embedding(input_ids)
    x: Float[Tensor, 'batch seq_len hidden_size'] = embedded + pos_enc
    y = self.bert(inputs_embeds=x)
    seq_output = y.last_hidden_state
    return self.fc(seq_output)
