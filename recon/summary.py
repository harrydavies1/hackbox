#!/usr/bin/env python3

import re
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: summary.py <nmap-report>")
        raise SystemExit(1)

    report = Path(sys.argv[1])

    if not report.exists():
        print(f"[-] File not found: {report}")
        raise SystemExit(1)

    hosts = []

    for line in report.read_text().splitlines():
        match = re.match(r"Nmap scan report for (\S+)", line)

        if match:
            hosts.append(match.group(1))

    print(f"[+] Hosts discovered: {len(hosts)}")
    print()

    for number, host in enumerate(hosts, start=1):
        print(f"{number:02d}. {host}")


if __name__ == "__main__":
    main()
