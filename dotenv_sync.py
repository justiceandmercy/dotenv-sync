"""dotenv-sync: compare .env and .env.example keys."""

import argparse
import sys
from pathlib import Path


ENV_NAMES = (".env", ".env.local", ".env.development", ".env.production")


def parse_keys(path):
    """Return the set of variable names defined in an env file."""
    keys = set()
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return keys
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        if not key:
            continue
        if not (key[0].isalpha() or key[0] == "_"):
            continue
        if not all(c.isalnum() or c == "_" for c in key):
            continue
        keys.add(key)
    return keys


def find_pairs(root):
    """Locate .env/.env.example pairs under root."""
    root = Path(root)
    pairs = []
    for name in ENV_NAMES:
        env_path = root / name
        example_path = root / (name + ".example")
        if env_path.is_file() or example_path.is_file():
            pairs.append((env_path, example_path))
    if not pairs and (root / ".env.example").is_file():
        pairs.append((root / ".env", root / ".env.example"))
    return pairs


def diff(env_keys, example_keys):
    """Return (missing_in_example, stale_in_example) sorted lists."""
    return sorted(env_keys - example_keys), sorted(example_keys - env_keys)


def report(results):
    ok = True
    for env_path, example_path, missing, stale in results:
        if not (missing or stale):
            continue
        ok = False
        print(f"{env_path} <-> {example_path}")
        if missing:
            print("  missing in example (add these):")
            for key in missing:
                print(f"    - {key}")
        if stale:
            print("  stale in example (remove or document):")
            for key in stale:
                print(f"    - {key}")
    if ok:
        print("All env files in sync.")
    return 0 if ok else 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="dotenv-sync", description="Check .env vs .env.example key parity."
    )
    parser.add_argument("path", nargs="?", default=".", help="directory to scan")
    args = parser.parse_args(argv)
    pairs = find_pairs(args.path)
    if not pairs:
        print("No .env/.env.example pairs found.")
        return 0
    results = []
    for env_path, example_path in pairs:
        env_keys = parse_keys(env_path) if env_path.is_file() else set()
        example_keys = parse_keys(example_path) if example_path.is_file() else set()
        missing, stale = diff(env_keys, example_keys)
        results.append((env_path, example_path, missing, stale))
    return report(results)


if __name__ == "__main__":
    sys.exit(main())
