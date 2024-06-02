from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-y', '--year', type=int, required=True)
  parser.add_argument('-m', '--month', type=int, required=True)
  parser.add_argument('-o', '--output', type=str, default=None, help='Passed to "wget -O"`. Use "-" for stdout.')

  args = parser.parse_args()

  from pgn_clis.lib.download import run_lichess_download
  run_lichess_download(year=args.year, month=args.month, output=args.output)