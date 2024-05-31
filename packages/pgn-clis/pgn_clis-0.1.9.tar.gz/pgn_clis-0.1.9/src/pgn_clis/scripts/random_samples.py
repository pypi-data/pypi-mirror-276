from argparse import ArgumentParser

def main():

  parser = ArgumentParser()
  parser.add_argument('-n', '--num-samples', type=int, default=int(1e6))
  parser.add_argument('-l', '--max-len', type=int, default=150)
  parser.add_argument('-s', '--seed', type=int, default=None)
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('-r', '--replace', action='store_true')
  parser.add_argument('-p', '--num-procs', type=int, default=None)

  io_group = parser.add_mutually_exclusive_group(required=True)
  files_spec = io_group.add_argument_group()
  files_spec.add_argument('-i', '--inputs', type=str)
  files_spec.add_argument('-u', '--ucis', type=str)

  io_group.add_argument('-o', '--output', type=str)

  args = parser.parse_args()

  import os

  if args.output:
    os.makedirs(args.output, exist_ok=True)
    input_path = os.path.join(args.output, 'inputs.txt')
    uci_path = os.path.join(args.output, 'ucis.txt')
  else:
    input_path = args.inputs
    uci_path = args.ucis

  import sys
  from pgn_clis.lib.random_samples import random_samples

  mode = 'w' if args.replace else 'x'
  with open(input_path, mode) as inputs_f, open(uci_path, mode) as ucis_f:
    random_samples(
      inputs_f, ucis_f,
      num_samples=args.num_samples, max_len=args.max_len, num_procs=args.num_procs,
      seed=args.seed, logstream=sys.stderr if args.verbose else None
    )