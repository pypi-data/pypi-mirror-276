from typing_extensions import Iterable, Mapping, TypeVar, LiteralString
from dataclasses import dataclass
import os
from haskellian import Iter, iter as I, dicts as D
from .meta import Meta

K = TypeVar('K', bound=LiteralString)

@dataclass
class Dataset(Iterable[Mapping[str, str]]):

  base_path: str
  meta: Meta

  @classmethod
  def read(cls, base: str) -> 'Dataset':
    with open(os.path.join(base, 'meta.json')) as f:
      meta = Meta.model_validate_json(f.read())
    return Dataset(base, meta)
  
  @classmethod
  def create(cls, base: str, meta: Meta, *, overwrite: bool = False) -> 'Dataset':
    os.makedirs(base, exist_ok=True)
    mode = 'x' if not overwrite else 'w'
    with open(os.path.join(base, 'meta.json'), mode) as f:
      f.write(meta.model_dump_json())
    return Dataset(base, meta)
  
  def keys(self):
    return list(self.meta.files.keys())
  
  def file(self, key: str) -> Meta.File | None:
    if key in self.meta.files:
      file = self.meta.files[key]
      return Meta.File(file=os.path.join(self.base_path, file.file), compression=file.compression)
    return None
  
  @I.lift
  def iterate(self, key: str) -> Iterable[str]:
    file = self.file(key)
    if file:
      if file.compression == 'zstd':
        from .compression import iterate
        yield from iterate(file.file)
      else:
        with open(file.file) as f:
          yield from f

  def samples(self, *keys: K) -> Iter[Mapping[K, str]]:
    keys = keys or list(self.meta.files.keys()) # type: ignore
    return D.zip({
      k: self.iterate(k)
      for k in keys
    })

  def __iter__(self):
    return iter(self.samples())

  def __len__(self) -> int:
    return self.meta.samples