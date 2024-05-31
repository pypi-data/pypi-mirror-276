from typing import Literal, Mapping, TypeAlias, Iterable, Sequence
import chess_notation as cn
from .sans import legal_sans, sort_key

SpecialToken: TypeAlias = Literal['[PAD]', '[CLS]', '[SEP]', '[MASK]']
PAD: TypeAlias = Literal['[PAD]']
MASK: TypeAlias = Literal['[MASK]']
Vocabulary: TypeAlias = Mapping[str | SpecialToken, int]

def remove_symbols(san: str) -> str:
  """Remove check and mate symbols from a SAN move"""
  return san.replace('+', '').replace('#', '')

def make_vocab(words: Iterable[str]) -> Vocabulary:
  return { word: i for i, word in enumerate(words) }

def legal(with_symbols: bool = False, *, pad_token: str = '[PAD]') -> Vocabulary:
  """Vocabulary containing all legal SAN moves
  - `with_symbols`: whether to include `+` and `#` (triples the size of the vocabulary, though)
  """
  return make_vocab(legal_sans(with_symbols) + [pad_token])

def legal_styled(
  with_symbols: bool = False, *,
  motions: cn.MotionStyles = cn.MotionStyles(),
  effects: cn.KingEffectStyles = cn.KingEffectStyles(),
  languages: Sequence[cn.Language] = cn.LANGUAGES,
  pad_token: str = '[PAD]',
) -> Vocabulary:
  """All legal sans, styled. Size 60953 with default parameters
  - Legal SANs come first, then all representations
  """
  legal = legal_sans(with_symbols)
  words = set()
  for san in legal:
    words |= cn.all_representations(san, motions=motions, effects=effects, languages=languages)
  new_words = words - set(legal)
  sorted_words = sorted(new_words, key=sort_key)
  return make_vocab(legal + [pad_token] + sorted_words)
  