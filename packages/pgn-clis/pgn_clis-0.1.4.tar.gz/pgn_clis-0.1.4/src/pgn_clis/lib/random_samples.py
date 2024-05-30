from typing import Sequence, NamedTuple, Iterable, TextIO
import os
from multiprocessing import Pool
import random
from haskellian import iter as I
from tqdm import tqdm
import chess_utils as cu
import chess

class Sample(NamedTuple):
  inputs: Sequence[str]
  ucis: Sequence[str]

def random_sample(max_len: int = 150, rng = random.Random()) -> Sample:
  board = chess.Board()
  inputs = []
  ucis = []

  for _ in range(max_len):
    move = cu.random.move(board, rng)
    if not move:
      break
    san = board.san(move)
    board.push(move)
    inputs.append(san)
    ucis.append(move.uci())

  return Sample(inputs, ucis)

def random_batch(num_samples: int, max_len: int = 150, rng = random.Random()) -> Sequence[Sample]:
  return [random_sample(max_len, rng) for _ in range(num_samples)]

def random_samples(
  inputs: TextIO, ucis: TextIO, *,
  num_samples: int, max_len: int = 150, chunk_size: int = 100,
  seed: int | None = None, logstream: TextIO | None = None,
  num_procs: int | None = None
):
  num_procs = num_procs or os.cpu_count() or 1
  rng = random.Random(seed)
  iter = tqdm(range(num_samples), file=logstream, miniters=100) if logstream else range(num_samples)
  with Pool() as pool:
    for _ in I.batch(chunk_size, iter):
      samples = pool.apply(random_batch, (chunk_size, max_len, rng))
      for sample in samples:
        print(' '.join(sample.inputs), file=inputs)
        print(' '.join(sample.ucis), file=ucis)