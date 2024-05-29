from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('--min-chars', '-m', type=int, default=20)

  args = parser.parse_args()

  from pgn_clis.lib.clean import run_clean
  run_clean(args.min_chars)