from typing import NamedTuple, Sequence
from ..vocab import Vocabulary
from ._labels import labels, Label

class Sample(NamedTuple):
  input_ids: Sequence[int]
  labs: Sequence[Label]

def parse_sample(
  inputs: str, *,
  vocab: Vocabulary
) -> Sample:
	sans = inputs.strip('\n').replace('+', '').replace('#', '').split(' ')
	input_ids = [vocab[san] for san in sans]
	labs = labels(sans)
	return Sample(input_ids, labs)