# PGN CLIs

- `clean-pgns`:
  ```bash
  cat games.pgn clean-pgns > inputs.txt
  ```
- `lichess-download`:
  ```bash
  lichess-download -y 2021 -m 12
  ```
- `sans2ucis`
  ```bash
  cat inputs.txt | sans2ucis -v > ucis.txt
  ```

- `style-sans`
  ```bash
  cat inputs.txt | style-sans -v > styled.txt
  ```

- `random-samples`
  ```bash
  random-samples -n 1000000 -l 300 -v -o output/folder # or -i inputs.txt -u ucis.txt
  ```