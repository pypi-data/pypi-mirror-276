from typing import Sequence, Mapping
from jaxtyping import Float
from torch import Tensor
from ..uci import metrics as uci_metrics
from ..fen import metrics as fen_metrics

def metrics(
  uci: Float[Tensor, 'L 5'],
  fen: Float[Tensor, 'L 64*13'],
  *,
  true_ucis: Sequence[str],
  true_fens: Sequence[str],
) -> Mapping[str, float]:
  return {
    f'uci-{k}': v for k, v in uci_metrics(uci, true_ucis).items()
  } | {
    f'fen-{k}': v for k, v in fen_metrics(fen, true_fens).items()
  } # type: ignore