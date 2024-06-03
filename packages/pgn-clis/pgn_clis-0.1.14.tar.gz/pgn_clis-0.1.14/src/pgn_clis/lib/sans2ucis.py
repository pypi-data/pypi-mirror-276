from typing import TextIO
import fs
import chess_utils as cu

def process_line(line: str) -> str:
  sans = line.strip().split()
  return ' '.join(cu.sans2ucis(sans)) + '\n'

def run_sans2ucis(
  input: TextIO, output: TextIO, *,
  num_procs: int | None = None, chunk_size: int = 10000,
  logstream: TextIO | None = None
):
  fs.parallel_map(input, output, process_line, num_procs=num_procs, chunk_size=chunk_size, logstream=logstream)