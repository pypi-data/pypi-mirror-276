from typing import Sequence, NamedTuple, Iterable, TextIO
from tqdm import tqdm
import chess_utils as cu
import chess
import random

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

def random_samples(
  inputs: TextIO, ucis: TextIO, *,
  num_samples: int, max_len: int = 150,
  seed: int | None = None, logstream: TextIO | None = None
):
  rng = random.Random(seed)
  iter = tqdm(range(num_samples), file=logstream, miniters=100) if logstream else range(num_samples)
  for _ in iter:
    sample = random_sample(max_len, rng)
    print(' '.join(sample.inputs), file=inputs)
    print(' '.join(sample.ucis), file=ucis)