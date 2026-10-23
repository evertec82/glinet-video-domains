#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
import urllib.request
from pathlib import Path

DOMAIN = re.compile(r"^(?=.{1,253}\.?$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", re.I)
RULE_PREFIXES = ("DOMAIN,", "DOMAIN-SUFFIX,")


def normalize(value: str) -> str | None:
    value = value.strip().lower().rstrip(".")
    if value.startswith("+.") or value.startswith("*."):
        value = value[2:]
    for prefix in RULE_PREFIXES:
        if value.upper().startswith(prefix):
            value = value.split(",", 2)[1].strip().lower().rstrip(".")
            break
    if value.startswith(("#", "//")) or not value:
        return None
    try:
        ipaddress.ip_network(value, strict=False)
        return None
    except ValueError:
        pass
    return value.encode("idna").decode("ascii") if DOMAIN.fullmatch(value) else None


def parse(text: str, kind: str) -> set[str]:
    if kind == "plain":
        values = text.splitlines()
    elif kind == "clash":
        values = []
        in_payload = False
        for line in text.splitlines():
            stripped = line.strip()
            if stripped == "payload:":
                in_payload = True
            elif in_payload and stripped.startswith("-"):
                value = stripped[1:].strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                values.append(value)
    else:
        raise ValueError(f"unsupported format: {kind}")
    return {domain for value in values if isinstance(value, str) and (domain := normalize(value))}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "glinet-video-domains/1.0"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return response.read().decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default="sources.json")
    parser.add_argument("--output", default="dist/video-domains.txt")
    args = parser.parse_args()
    config = json.loads(Path(args.sources).read_text())
    domains: set[str] = set()
    for source in config["sources"]:
        parsed = parse(fetch(source["url"]), source["format"])
        if not parsed:
            raise RuntimeError(f"{source['name']} produced zero domains")
        print(f"{source['name']}: {len(parsed)}", file=sys.stderr)
        domains.update(parsed)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(sorted(domains)) + "\n")
    print(f"total: {len(domains)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

