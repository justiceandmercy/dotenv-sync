# dotenv-sync

A small, dependency-free CLI that verifies your `.env` files stay in key parity with their `.env.example` templates. Catches missing keys before deploy and stale example keys after refactors.

## Features

- Scans a directory for `.env` / `.env.example` (and `.env.local`, `.env.development`, `.env.production`) pairs.
- Reports keys present in `.env` but missing from `.env.example` (add them).
- Reports keys present in `.env.example` but absent from `.env` (stale or undocumented).
- Pure standard library, no external dependencies.
- Non-zero exit code on any diff, suitable for CI.

## Install

```sh
pip install dotenv-sync
```

Or run from source:

```sh
python dotenv_sync.py .
```

## Usage

```sh
dotenv-sync [path]
```

Example output:

```
.env <-> .env.example
  missing in example (add these):
    - STRIPE_WEBHOOK_SECRET
  stale in example (remove or document):
    - OLD_API_KEY
```

Exit status is `1` when any pair differs, `0` otherwise.

## License

MIT
