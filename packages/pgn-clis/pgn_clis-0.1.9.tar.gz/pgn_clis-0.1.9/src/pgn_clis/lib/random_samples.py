from typing import Sequence, NamedTuple, Iterable, TextIO
import os
import multiprocessing as mp
import random
import chess_utils as cu
import chess_notation as cn
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


def random_samples(
  inputs: TextIO, ucis: TextIO, *,
  num_samples: int, max_len: int = 150,
  seed: int | None = None, logstream: TextIO | None = None,
  num_procs: int | None = None
):
  num_procs = num_procs or os.cpu_count() or 1
  num_procs = max(1, num_procs-1) # leave one core for the collector
  proc_samples = num_samples // num_procs

  if logstream:
    print(f'Generating {num_samples} samples...', file=logstream)
    print(f'  max_len: {max_len}', file=logstream)
    print(f'  num_procs: {num_procs}', file=logstream)
    print(f'  seed: {seed or "random"}', file=logstream)
    print()

  q = mp.Queue()

  def collector(
    inputs: TextIO, ucis: TextIO,
    *, queue: mp.Queue,
    logstream: TextIO | None = None
  ):
    i = 0
    while True:
      data = queue.get()
      if data is None:
        break
      inputs.write(' '.join(data.inputs) + '\n')
      ucis.write(' '.join(data.ucis) + '\n')

      if logstream:
        i += 1
        if i % 100 == 0:
          print(f'\r{i} / {num_samples} ({100*i/num_samples:.2f}%)', end='', file=logstream)

  def generator(queue: mp.Queue, num_samples: int, seed: int | None):
    rng = random.Random(seed)
    for _ in range(num_samples):
      sample = random_sample(max_len, rng)
      queue.put(sample)

  collector_proc = mp.Process(target=collector, args=(inputs, ucis), kwargs=dict(queue=q, logstream=logstream))
  collector_proc.start()

  gen_procs: list[mp.Process] = []
  for _ in range(num_procs):
    gen_proc = mp.Process(target=generator, args=(q, proc_samples, seed))
    gen_proc.start()
    gen_procs.append(gen_proc)

  for gen_proc in gen_procs:
    gen_proc.join()

  q.put(None)
  collector_proc.join()
