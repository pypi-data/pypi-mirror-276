from typing import Sequence, Iterable, NamedTuple, Literal, TypeAlias
import chess_utils as cu

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
	
promotion_ids = dict(n=1, b=2, r=3, q=4)
def encode_promotion(piece: Literal['n', 'b', 'r', 'q'] | None) -> int:
  return 0 if piece is None else promotion_ids[piece]

def encode_uci(e2e4q: str) -> tuple[int, int, int, int, int]:
  from_file = ord(e2e4q[0]) - ord('a')
  from_rank = int(e2e4q[1]) - 1
  to_file = ord(e2e4q[2]) - ord('a')
  to_rank = int(e2e4q[3]) - 1
  promotion = encode_promotion(e2e4q[4] if len(e2e4q) == 5 else None) # type: ignore
  return from_file, from_rank, to_file, to_rank, promotion

Label: TypeAlias = tuple[int, int, int, int, int]

def labels(ucis: Iterable[str]) -> Sequence[Label]:
	return [encode_uci(uci) for uci in ucis]

class Sample(NamedTuple):
	inputs: TokenizedInput
	labs: Sequence[Label]

def parse_sample(inputs: str, ucis: str | None = None) -> Sample:
	sans = inputs.strip('\n').replace('+', '').replace('#', '').split(' ')
	toks = tokenize(sans)
	parsed_ucis = cu.sans2ucis(sans) if ucis is None else ucis.strip('\n').split(' ')
	labs = labels(parsed_ucis)
	return Sample(toks, labs)