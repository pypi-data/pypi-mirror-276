from typing import Iterable, Sequence
import fs

def iterate_samples(
  input_files: Sequence[str], uci_files: Sequence[str],
) -> Iterable[tuple[str, str]]:
  inputs = fs.concat_lines(input_files)
  ucis = fs.concat_lines(uci_files)
  yield from zip(inputs, ucis)
