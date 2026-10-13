#!/usr/bin/env python3

import argparse
import subprocess
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Authorized network discovery helper"
    )
    parser.add_argument(
        "target",
        help="IP address or CIDR network you are authorized to scan"
    )
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path.home() / "security" / "recon"
    output_dir.mkdir(parents=True, exist_ok=True)

    normal_output = output_dir / f"scan_{timestamp}.nmap"
    xml_output = output_dir / f"scan_{timestamp}.xml"

    print(f"[+] Target : {args.target}")
    print(f"[+] Report : {normal_output}")
    print(f"[+] XML    : {xml_output}")
    print("[+] Starting host discovery...")

    command = [
        "nmap",
        "-sn",
        args.target,
        "-oN",
        str(normal_output),
        "-oX",
        str(xml_output),
    ]

    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("[-] Nmap is not installed.")
        raise SystemExit(1)
    except subprocess.CalledProcessError as exc:
        print(f"[-] Nmap exited with code {exc.returncode}")
        raise SystemExit(exc.returncode)

    print("[+] Discovery complete.")


if __name__ == "__main__":
    main()
