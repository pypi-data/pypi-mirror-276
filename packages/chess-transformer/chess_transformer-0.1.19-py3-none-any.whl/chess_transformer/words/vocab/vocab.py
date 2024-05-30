from typing import Literal, Mapping, TypeAlias, Iterable, Sequence
import chess_notation as cn
from .sans import legal_sans

SpecialToken: TypeAlias = Literal['[PAD]', '[CLS]', '[SEP]', '[MASK]']
PAD: TypeAlias = Literal['[PAD]']
MASK: TypeAlias = Literal['[MASK]']
Vocabulary: TypeAlias = Mapping[str | SpecialToken, int]

def remove_symbols(san: str) -> str:
  """Remove check and mate symbols from a SAN move"""
  return san.replace('+', '').replace('#', '')

def make_vocab(words: Iterable[str]) -> Vocabulary:
  vocab = { word: i for i, word in enumerate(words) }
  return vocab | {
    '[PAD]': len(vocab),
    '[CLS]': len(vocab) + 1,
    '[SEP]': len(vocab) + 2,
    '[MASK]': len(vocab) + 3
  }

def legal(with_symbols: bool = False) -> Vocabulary:
  """Vocabulary containing all legal SAN moves
  - `with_symbols`: whether to include `+` and `#` (triples the size of the vocabulary, though)
  """
  return make_vocab(legal_sans(with_symbols))

def legal_styled(
  with_symbols: bool = False, *,
  motions: cn.MotionStyles = cn.MotionStyles(),
  effects: cn.KingEffectStyles = cn.KingEffectStyles(),
  languages: Sequence[cn.Language] = cn.LANGUAGES
) -> Vocabulary:
  """All legal sans, styled. Size 60953 with default parameters"""
  words = set()
  for san in legal_sans(with_symbols):
    words |= cn.all_representations(san, motions=motions, effects=effects, languages=languages)
  return make_vocab(words)
  