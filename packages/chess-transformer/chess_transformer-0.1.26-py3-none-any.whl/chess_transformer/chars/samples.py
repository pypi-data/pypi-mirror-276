from typing import Sequence, NamedTuple, Literal
import chess_utils as cu
from .._labels import Label, labels

class TokenizedInput(NamedTuple):
	tokens: Sequence[str | Literal['[SEP]']]
	ends: Sequence[int]

def tokenize(words: Sequence[str]) -> TokenizedInput:
	"""Split words into characters, adding '[SEP]' between words. `return.ends` are the original word end indices"""
	tokens = []
	ends = []
	end = 0
	for word in words:
		tokens.extend(word)
		tokens.append('[SEP]')
		end += len(word)
		ends.append(end)
	
	return TokenizedInput(tokens, ends)
	
class Sample(NamedTuple):
	inputs: TokenizedInput
	labs: Sequence[Label]

def parse_sample(inputs: str, ucis: str | None = None) -> Sample:
	sans = inputs.strip('\n').replace('+', '').replace('#', '').split(' ')
	toks = tokenize(sans)
	parsed_ucis = cu.sans2ucis(sans) if ucis is None else ucis.strip('\n').split(' ')
	labs = labels(parsed_ucis)
	return Sample(toks, labs)