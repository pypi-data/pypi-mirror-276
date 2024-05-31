from typing import Sequence, Literal
from jaxtyping import Int, Float
from torch import nn, Tensor
from transformers import BertConfig, BertModel
from ..chars.pos_enc import positional_encoding
from ..chars.segmented import pool_batch

class BertPool(nn.Module):

  pos_enc: Float[Tensor, 'd_model max_len']
  pool: Literal['mean', 'max']
  
  def __init__(
    self, *,
    vocab_size: int,
    max_len: int,
    pool: Literal['mean', 'max'] = 'max',
    pre_nheads: int = 12,
    pre_layers: int = 2,
    pre_ff_dims: int = 2048,
    hidden_size: int = 768,
    attention_heads: int = 12,
  ):
    super().__init__()
    # BERT configuration
    self.config = BertConfig(
      vocab_size=vocab_size,
      hidden_size=hidden_size,
      num_attention_heads=attention_heads,
      max_position_embeddings=max_len
    )
    self.pool = pool
    self.register_buffer('pos_enc', positional_encoding(max_len, hidden_size))
    self.pre_layers = nn.TransformerEncoder(
      nn.TransformerEncoderLayer(hidden_size, nhead=pre_nheads, dim_feedforward=pre_ff_dims, batch_first=True),
      num_layers=pre_layers
    )
    self.embedding = nn.Embedding(vocab_size, hidden_size)
    self.bert = BertModel(self.config)
    self.fc = nn.Linear(hidden_size, 4 * 8 + 5)

  def forward(
    self, input_ids: Int[Tensor, 'batch seq_len'],
    word_ends: Sequence[Sequence[int]]
  ) -> Float[Tensor, 'batch seq_len 37']:
    
    embeds: Float[Tensor, 'batch seq_len hidden_size'] = self.embedding(input_ids)
    enhanced_embeds: Float[Tensor, 'batch seq_len hidden_size'] = self.pre_layers(embeds)
    pooled_embeds = pool_batch(enhanced_embeds, word_ends, mode=self.pool)
    move_embeds: Float[Tensor, 'batch moves hidden_size'] = self.pos_enc[None, :len(pooled_embeds[1]), :] + pooled_embeds

    y = self.bert(inputs_embeds=move_embeds)
    seq_output = y.last_hidden_state
    return self.fc(seq_output)
