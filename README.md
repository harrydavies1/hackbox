# Hackbox — Raspberry Pi Security Toolkit

Hackbox is a lightweight Bash + Python menu for **authorized** network inventory, diagnostics, passive packet capture, DNS analysis, and local security audits.

> **Hardware-tested on a Raspberry Pi 3 Model B (Pi 3B)** with **Raspberry Pi OS Lite 64-bit (aarch64)**. Network discovery, Nmap, tcpdump, SSH configuration and LAN diagnostics were run on that Pi during development. **This GitHub copy was reconstructed from our previous chats** and the complete 14-option menu has **not yet been tested end-to-end** on the physical Pi. Not every feature or Wi-Fi adapter has been hardware-tested.

## Hardware requirements

| Hardware | Requirement |
| --- | --- |
| Raspberry Pi | **Pi 3 Model B — tested platform**. Other models might work but aren't verified. |
| microSD | **32 GB used**; 16 GB+ recommended, especially for PCAP files. |
| Power | Stable **5V / 2.5A** Pi 3-class power supply; powered USB hub if peripherals need more current. |
| Network | **Ethernet recommended**, particularly for SSH and LAN inventory. |
| Keyboard/screen | Optional; headless use via SSH works. |
| External USB Wi-Fi dongle | Optional for normal networking and scans, **required for monitor-mode capture on the tested Pi**. |

### Wi-Fi dongle: monitor mode and injection support

The Raspberry Pi 3B's **built-in Broadcom/brcmfmac Wi-Fi** on the development system does **not advertise monitor mode**. For the Wi-Fi Passive Capture menu, use a compatible USB adapter with a Linux driver that supports monitor mode.

Recommended budget chipset: **Atheros AR9271** using the Linux **ath9k_htc** driver and appropriate firmware. Common choices are **Alfa AWUS036NHA** and **TP-Link TL-WN722N V1 only**. **TL-WN722N V2/V3 have different hardware**; don't assume they work the same way. Generic AR9271 adapters may be inexpensive, but check the real chipset with lsusb after delivery. The previously discussed low-cost **Plyisty AR9271-style dongle** is **not verified on this Pi**.

**AR9271 is 2.4 GHz only**, not 5 GHz. Monitor-mode and packet-injection compatibility depend on the adapter's actual revision, firmware, driver and kernel. Packet injection is **not required** for Hackbox's passive capture menu. Use active wireless testing only within an explicitly authorized lab.

Check a plugged-in dongle with:

~~~bash
lsusb
sudo dmesg | tail -n 40
iw dev
iw list
~~~

Inspect **Supported interface modes** for the **USB adapter's own phy** and look for **monitor**. Keep Ethernet connected so you don't lose SSH when changing Wi-Fi settings.

## Software

Developed on **Raspberry Pi OS Lite 64-bit**, Python **3.13.5**, Nmap **7.95**, tcpdump **4.99.5**, Git **2.47.3** (kernel **6.18.50+rpt-rpi-v8** during testing). Exact versions need not match.

~~~bash
sudo apt update
sudo apt install -y bash python3 git nmap iproute2 dnsutils tcpdump iw network-manager tshark
# Optional:
sudo apt install -y avahi-utils ufw
~~~

Some features require sudo. The included Python programs only use the **standard library**; **Scapy is not required** for the currently included tools.

## Repository layout

~~~text
hackbox/
├── README.md
├── .gitignore
├── scripts/
│   ├── hackbox           # Main Bash menu
│   └── security-recon    # Legacy recon launcher
└── recon/
    ├── discover.py       # Authorized Nmap discovery and reports
    └── summary.py        # Parse host discovery reports
~~~

The included Python helpers and the security-recon launcher reproduce code from the chats; parts of the main menu were **reconstructed** from previously discussed functionality, not extracted from the Pi.

## Menu

| # | Feature |
| --- | --- |
| 1 | LAN Device Inventory |
| 2 | Nmap OS / Device Identification |
| 3 | Network Discovery |
| 4 | Network Information |
| 5 | Service Discovery |
| 6 | DNS Lookup |
| 7 | Packet Capture |
| 8 | Wi-Fi Reconnaissance |
| 9 | Wi-Fi Passive Capture |
| 10 | PCAP Analysis |
| 11 | ARP Change Monitor |
| 12 | Local Security Audit |
| 13 | Saved Results |
| 14 | DNS Device Monitor |

## Quick start

The repository is **private**. Use a GitHub account with access and Git credentials or an SSH key to clone:

~~~bash
git clone https://github.com/harrydavies1/hackbox.git
cd hackbox
bash scripts/hackbox
~~~

This runs the GitHub copy **without overwriting your existing working Hackbox**. It writes runtime files under ~/security/recon, ~/security/network and ~/security/reports (outside the repository).

To test discovery directly:

~~~bash
python3 recon/discover.py --help
python3 recon/discover.py 192.168.1.0/24
~~~

Replace that example network with a target you own or are explicitly permitted to scan.

### Optional installation alongside your previous setup

Only replace the older scripts **after verifying the repo version**:

~~~bash
mkdir -p ~/security/scripts ~/security/recon
cp -a ~/security/scripts/hackbox ~/security/scripts/hackbox.backup 2>/dev/null || true
cp scripts/hackbox scripts/security-recon ~/security/scripts/
cp recon/discover.py recon/summary.py ~/security/recon/
chmod +x ~/security/scripts/hackbox ~/security/scripts/security-recon
~~~

The legacy security-recon launcher expects Python helpers in ~/security/recon.

## Troubleshooting

### "hackbox: command not found"

Run **bash scripts/hackbox** in the repo. For a globally accessible installed command:

~~~bash
chmod +x ~/security/scripts/hackbox
echo 'export PATH="$HOME/security/scripts:$PATH"' >> ~/.bashrc
source ~/.bashrc
command -v hackbox
~~~

Or invoke ~/security/scripts/hackbox directly.

### "Permission denied", Nmap OS detection fails, or captures fail

Run the menu as your normal user. Individual privileged commands request **sudo**. Ensure your user has sudo rights. OS guesses from Nmap are probabilistic and can be inconclusive even when a device is reachable.

### Missing nmap, tshark, tcpdump, dig, iw, nmcli or capinfos

~~~bash
command -v nmap tshark tcpdump dig iw nmcli capinfos
sudo apt install -y nmap tshark tcpdump dnsutils iw network-manager
~~~

### LAN Device Inventory is empty or names say "unknown"

The inventory reads the Pi's **neighbor table**, not all possible IPs on the network. Offline devices, recently inactive hosts and separate VLANs won't necessarily appear. Hostnames may lack reverse-DNS or mDNS records.

~~~bash
ip route
ip neigh show
~~~

Use **menu 3 — Network Discovery** to scan a subnet you are authorized to assess.

### Built-in Wi-Fi won't enter monitor mode

This is expected on the tested **Pi 3B's brcmfmac driver/firmware**. Use a monitor-capable external USB adapter and verify its chipset, driver, and interface with **lsusb**, **iw dev**, and **iw list**. Do not assume a generic Wi-Fi dongle supports monitor mode.

### Wi-Fi Passive Capture sees no 802.11 frames

Check that the external USB adapter is operating in **monitor mode**, that you're using its interface rather than the internal radio, and that the selected channel is relevant. An ordinary managed-mode Wi-Fi connection is not an 802.11 monitor interface. USB power problems can also cause drops.

### DNS Device Monitor sees only the Pi, not a phone or Fire Stick

On a **switched Ethernet LAN**, the Pi usually cannot see another device's unicast DNS packets. You can confirm local traffic with:

~~~bash
sudo tcpdump -ni eth0 port 53
# From a second terminal:
dig example.com
~~~

Device-to-domain attribution requires that clients query a **DNS resolver you administer**, or that you have access to authorized router resolver logs or mirrored traffic. **Hackbox does not install a LAN DNS server.** Cached, encrypted or hard-coded DNS may not appear. A public DNS lookup for netflix.com **does not reveal a Fire Stick's local IP**.

### IP address changed / SSH won't connect

Check the Pi's address with **hostname -I** or your router's connected-client list. Reserve a local DHCP address in the router for stable access. Keep SSH allowed if using UFW. Only expose DNS services to authorized LAN clients if you later configure your own resolver.

### Reports missing or SD card full

Look under **~/security/recon**, **~/security/network**, and **~/security/reports**. Use **df -h** to check remaining space. Captures can grow quickly. Avoid committing reports or captures.

## Security and privacy

Only capture or scan authorized traffic. The **.gitignore** excludes common PCAP formats, private keys, environment files and reports; **always review git status before pushing**. A private repository is still not appropriate for credentials or sensitive traffic dumps.

## Testing status

- **Verified on Raspberry Pi 3 Model B:** OS/platform, network interfaces, Nmap discovery, tcpdump capturing the Pi's own DNS, SSH configuration, and LAN diagnostics.
- **Code-level checked:** Bash menu syntax and Python compilation of this reconstructed snapshot.
- **Not yet verified end-to-end on the Pi:** all 14 menu operations as shipped in this repository, USB AR9271 adapter behavior, and full multi-device DNS attribution.
