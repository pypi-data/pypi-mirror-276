from typing import Iterable, Sequence, Callable
import fs
from haskellian import iter as I
import chess_transformer as ct

def iterate_samples(
  input_files: Sequence[str], uci_files: Sequence[str],
  *, skip: int = 0
) -> Iterable[ct.Sample]:
  inputs = fs.concat_lines(input_files)
  ucis = fs.concat_lines(uci_files)
  for inp, uci in I.skip(skip, zip(inputs, ucis)):
    yield ct.parse_sample(inp, uci)
