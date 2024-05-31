from typing import Mapping, TypeVar, Callable

K = TypeVar('K')
K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')
V1 = TypeVar('V1')
V2 = TypeVar('V2')

def map_v(f: Callable[[V1], V2], d: Mapping[K, V1]) -> Mapping[K, V2]:
  return { k: f(v) for k, v in d.items() }

def map_k(f: Callable[[K1], K2], d: Mapping[K1, V]) -> Mapping[K2, V]:
  return { f(k): v for k, v in d.items() }

def map_kv(f: Callable[[K1, V1], tuple[K2, V2]], d: Mapping[K1, V1]) -> Mapping[K2, V2]:
  return dict(f(k, v) for k, v in d.items())