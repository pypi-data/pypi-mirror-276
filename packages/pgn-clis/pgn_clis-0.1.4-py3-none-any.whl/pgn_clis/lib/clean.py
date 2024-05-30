import os

def run_clean(min_chars: int = 20):
  cmd = '|'.join([
    "sed '/^\[/d'",
    f"sed -n '/^.\{{{min_chars},\}}/p'",
    "sed '/{.*}/d'",
    "sed 's/[0-9]\+\. \?//g'",
    "sed 's/1\/2-1\/2$//'",
    "sed 's/1-0$//'",
    "sed 's/0-1$//'",
    "sed 's/*//'",
    "sed 's/[[:space:]]*$//'",
    "sed '/^$/d'"
  ])
  os.system(cmd)