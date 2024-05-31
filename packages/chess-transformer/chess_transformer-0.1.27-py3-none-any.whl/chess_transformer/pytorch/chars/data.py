from typing import Sequence, NamedTuple
from jaxtyping import Int
from torch import Tensor
import torch
from haskellian import iter as I
from ...chars import Char2Num, char2num as default_char2num, parse_sample as _parse_sample, Sample as GenericSample

class Sample(NamedTuple):
  input_ids: Int[Tensor, 'seq_len']
  word_ends: Sequence[int]
  labs: Int[Tensor, 'seq_len 5']

class Batch(NamedTuple):
  input_ids: Int[Tensor, 'batch seq_len']
  word_ends: Sequence[Sequence[int]]
  labs: Int[Tensor, 'batch seq_len 5']

def sample_from(sample: GenericSample, char2num: Char2Num = default_char2num) -> Sample:
  input_ids = [char2num[tok] for tok in sample.inputs.tokens]
  return Sample(torch.tensor(input_ids), sample.inputs.ends, torch.tensor(sample.labs))

def collate_same(batch: Sequence[Sample], *, max_len: int, pad_token_id: int, ignore_idx: int = -100) -> Batch:
  """Pad the input_ids and labs to the same length. (Used by BERT1)"""

  input_ids, ends, labs = I.unzip(batch)
  batch_size = len(input_ids)
  max_len = min(max(len(x) for x in input_ids), max_len)
  padded_input_ids = torch.full((batch_size, max_len), fill_value=pad_token_id)
  padded_labs = torch.full((batch_size, max_len, 5), fill_value=ignore_idx)

  for i in range(batch_size):
    padded_input_ids[i, :len(input_ids[i])] = input_ids[i][:max_len]
    padded_labs[i, :len(labs[i])] = labs[i][:max_len]

  return Batch(padded_input_ids, ends, padded_labs)

def collate_separate(batch: Sequence[Sample], *, max_len: int, pad_token_id: int, ignore_idx: int = -100) -> Batch:
  """Pad input_ids and labels separately (used by pooled-BERT)"""

  input_ids, ends, labs = I.unzip(batch)
  batch_size = len(input_ids)
  max_input_len = min(max(len(x) for x in input_ids), max_len)
  max_lab_len = min(max(len(x) for x in labs), max_len)
  padded_input_ids = torch.full((batch_size, max_input_len), fill_value=pad_token_id)
  padded_labs = torch.full((batch_size, max_lab_len, 5), fill_value=ignore_idx)

  for i in range(batch_size):
    padded_input_ids[i, :len(input_ids[i])] = input_ids[i][:max_len]
    padded_labs[i, :len(labs[i])] = labs[i][:max_len]

  return Batch(padded_input_ids, ends, padded_labs)