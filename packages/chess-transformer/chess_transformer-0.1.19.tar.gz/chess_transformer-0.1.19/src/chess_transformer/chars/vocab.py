from typing import Mapping, Literal, TypeAlias
import string

SpecialToken: TypeAlias = Literal['[PAD]', '[SEP]']
Char2Num: TypeAlias = Mapping[str | SpecialToken, int]
Num2Char: TypeAlias = Mapping[int, str | SpecialToken]

VOCABULARY = string.ascii_letters + string.digits + '-='
char2num: Char2Num = { char: i for i, char in enumerate(VOCABULARY) } | {
  '[PAD]': len(VOCABULARY),
  '[SEP]': len(VOCABULARY) + 1
}
num2char: Num2Char = { i: char for char, i in char2num.items() }