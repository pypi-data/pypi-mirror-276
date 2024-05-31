from typing import Sequence
import os
from glob import glob
from pydantic import BaseModel

class Meta(BaseModel):
  class Files(BaseModel):
    san: str | None = None
    uci: str
    styled: str | None = None
  samples: int
  source: str
  files: Files

def read_meta(base: str) -> Meta:
  with open(os.path.join(base, 'meta.json')) as f:
    return Meta.model_validate_json(f.read())
  
def input_files(base: str, meta: Meta | None = None) -> Sequence[str]:
  meta = meta or read_meta(base)
  files = meta.files.styled or meta.files.san
  if files is None:
    raise ValueError('No input files found in meta')
  return glob(os.path.join(base, files))

def uci_files(base: str, meta: Meta | None = None) -> Sequence[str]:
  meta = meta or read_meta(base)
  return glob(os.path.join(base, meta.files.uci))
