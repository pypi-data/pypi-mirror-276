import os

def run_lichess_download(year: int, month: int, output: str | None = None):
  url = f'https://database.lichess.org/standard/lichess_db_standard_rated_{year}-{month:02}.pgn.zst'
  cmd = f'wget {url}'
  if output is not None:
    cmd += f' -O {output}'
  os.system(cmd)