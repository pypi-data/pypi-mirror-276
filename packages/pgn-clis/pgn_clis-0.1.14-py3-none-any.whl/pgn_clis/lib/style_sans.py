from typing import TextIO
import fs
import chess_notation as cn

def process_line(line: str) -> str:
  sans = line.strip().split()
  notation = cn.random_notation()
  return ' '.join(cn.styled(sans, notation)) + '\n'

def run_style_sans(
  input: TextIO, output: TextIO, *,
  num_procs: int | None = None, chunk_size: int = 10000,
  logstream: TextIO | None = None
):
  fs.parallel_map(input, output, process_line, num_procs=num_procs, chunk_size=chunk_size, logstream=logstream)