#!/usr/bin/env python3
import os
import sys
import time
import shutil
import socket
import subprocess
from pathlib import Path

R = "\033[91m"
G = "\033[92m"
C = "\033[96m"
Y = "\033[93m"
M = "\033[95m"
W = "\033[97m"
X = "\033[0m"

REPO_DIR = Path.home() / "zaka-defensive-repositories"

# Curated defensive and security-auditing repositories.
REPOS = {
    "1": ("Lynis security auditing", "https://github.com/CISOfy/lynis.git"),
    "2": ("YARA malware identification", "https://github.com/VirusTotal/yara.git"),
    "3": ("OWASP Core Rule Set", "https://github.com/coreruleset/coreruleset.git"),
    "4": ("Sigma detection rules", "https://github.com/SigmaHQ/sigma.git"),
    "5": ("Fail2ban intrusion prevention", "https://github.com/fail2ban/fail2ban.git"),
    "6": ("AIDE file integrity tool", "https://github.com/aide/aide.git"),
    "7": ("Wazuh security monitoring", "https://github.com/wazuh/wazuh.git"),
    "8": ("osquery endpoint visibility", "https://github.com/osquery/osquery.git"),
}


def clear():
    os.system("clear")


def line(char="═", color=R, width=68):
    print(color + char * width + X)


def slow(message, color=G, delay=0.008):
    for ch in str(message):
        print(color + ch + X, end="", flush=True)
        time.sleep(delay)
    print()


def speak(message):
    speaker = shutil.which("espeak-ng")
    if speaker:
        try:
            subprocess.Popen(
                [speaker, "-v", "en-us", "-s", "145", str(message)[:250]],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            pass


def pause():
    input(f"\n{Y}Press ENTER to return to menu...{X}")


def progress(label, duration=0.7):
    print(f"{C}{label}{X}")
    total = 20
    for i in range(total + 1):
        bar = "█" * i + "░" * (total - i)
        print(f"\r{G}[{bar}] {i * 5:3d}%{X}", end="", flush=True)
        time.sleep(duration / total)
    print("\n")


def run_cmd(args, timeout=40):
    """Run a fixed command without a shell."""
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,
        )
        print(result.stdout.strip() or "(No output)")
        print(f"\nExit code: {result.returncode}")
    except FileNotFoundError:
        print(f"{Y}Tool not installed: {args[0]}{X}")
    except subprocess.TimeoutExpired:
        print(f"{Y}Timed out. Try again or inspect the tool manually.{X}")
    except OSError as exc:
        print(f"{R}Error: {exc}{X}")


def banner():
    clear()
    print(R + r"""
███████╗ █████╗ ██╗  ██╗ █████╗
╚════██║██╔══██╗██║ ██╔╝██╔══██╗
  ███╔═╝███████║█████╔╝ ███████║
██╔══╝  ██╔══██║██╔═██╗ ██╔══██║
███████╗██║  ██║██║  ██╗██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
""" + X)
    print(C + "          R E D   H A C K E R S   T E A M" + X)
    print(M + "          DEFENSIVE SECURITY CONSOLE" + X)
    line()
    print(W + "     AUDIT  |  MONITOR  |  DETECT  |  PROTECT" + X)
    line()


def intro():
    banner()
    speak("This is the best. Zaka Red Hackers Team. Welcome my bro. Defensive security console starting.")
    progress("Initializing local console")
    progress("Checking security utilities")
    slow("[OK] Local console initialized.", G)
    slow("[INFO] No remote system was accessed.", C)
    slow("WELCOME MY BRO", R, 0.035)
    time.sleep(0.5)


def system_info():
    clear()
    line()
    slow("SYSTEM INFORMATION", C)
    line()
    run_cmd(["uname", "-a"])
    if shutil.which("free"):
        run_cmd(["free", "-h"])
    if shutil.which("df"):
        run_cmd(["df", "-h", "/"])
    pause()


def internet_check():
    clear()
    line()
    slow("INTERNET CONNECTIVITY", C)
    line()
    for host in ("1.1.1.1", "8.8.8.8"):
        try:
            with socket.create_connection((host, 443), timeout=4):
                print(f"{G}[ONLINE]{X} {host}:443 reachable")
        except OSError:
            print(f"{Y}[NO CONNECTION]{X} {host}:443 unreachable")
    pause()


def dns_check():
    clear()
    line()
    slow("DNS LOOKUP", C)
    line()
    host = input("Domain (example.com): ").strip()
    if not host or "/" in host or any(c.isspace() for c in host):
        print(f"{R}Invalid domain.{X}")
    else:
        try:
            addresses = sorted({x[4][0] for x in socket.getaddrinfo(host, None)})
            for address in addresses:
                print(f"{G}{address}{X}")
        except socket.gaierror as exc:
            print(f"{R}DNS lookup failed: {exc}{X}")
    pause()


def tls_check():
    clear()
    line()
    slow("HTTPS / TLS CHECK", C)
    line()
    host = input("Hostname (example.com): ").strip()
    if (
        not host or "/" in host or ":" in host
        or any(c.isspace() for c in host) or host.startswith("-")
    ):
        print(f"{R}Enter a hostname only.{X}")
    elif shutil.which("curl"):
        run_cmd([
            "curl", "-I", "--connect-timeout", "8",
            "--max-time", "15", "--", "https://" + host
        ], timeout=20)
    else:
        print("Install curl first.")
    pause()


def firewall_check():
    clear()
    line()
    slow("FIREWALL STATUS", C)
    line()
    found = False
    for binary, args, label in (
        ("ufw", ["ufw", "status", "verbose"], "UFW"),
        ("nft", ["nft", "list", "ruleset"], "nftables"),
        ("iptables", ["iptables", "-S"], "iptables"),
    ):
        if shutil.which(binary):
            found = True
            print(f"\n{Y}--- {label} ---{X}")
            run_cmd(args)
    if not found:
        print("No supported firewall utility found.")
    pause()


def local_ports():
    clear()
    line()
    slow("LOCAL LISTENING PORTS", C)
    line()
    if shutil.which("ss"):
        run_cmd(["ss", "-lntup"])
    else:
        print("The ss command is unavailable.")
    pause()


def service_status():
    clear()
    line()
    slow("SECURITY SERVICE STATUS", C)
    line()
    if not shutil.which("systemctl"):
        print("systemctl is not available in this environment.")
    else:
        for service in ("fail2ban", "ufw", "clamav-daemon", "suricata", "auditd"):
            print(f"\n{Y}--- {service} ---{X}")
            run_cmd(["systemctl", "is-active", service], timeout=10)
    pause()


def fail2ban_check():
    clear()
    line()
    slow("FAIL2BAN STATUS", C)
    line()
    if shutil.which("fail2ban-client"):
        run_cmd(["fail2ban-client", "status"])
    else:
        print("Install with: apt install fail2ban")
    pause()


def updates_check():
    clear()
    line()
    slow("AVAILABLE PACKAGE UPDATES", C)
    line()
    print("This lists updates; it does not install them.")
    if shutil.which("apt"):
        run_cmd(["apt", "list", "--upgradable"], timeout=60)
    else:
        print("APT is not available.")
    pause()


def lynis_audit():
    clear()
    line()
    slow("LYNIS SECURITY AUDIT", C)
    line()
    print("Local audit. Review findings before making changes.")
    if shutil.which("lynis"):
        run_cmd(["lynis", "audit", "system", "--no-colors"], timeout=300)
    else:
        print("Install with: apt install lynis")
    pause()


def clamav_scan():
    clear()
    line()
    slow("CLAMAV FILE SCAN", C)
    line()
    scanner = shutil.which("clamscan")
    if not scanner:
        print("Install with: apt install clamav")
        pause()
        return

    raw = input("Folder to scan (blank = home folder): ").strip()
    target = Path(raw).expanduser() if raw else Path.home()
    if not target.exists() or not target.is_dir():
        print(f"{R}Folder not found or not a directory.{X}")
        pause()
        return

    print(f"Target: {target}")
    if input("Type SCAN to continue: ").strip() != "SCAN":
        print("Cancelled.")
        pause()
        return
    run_cmd([scanner, "-r", "--infected", str(target)], timeout=1800)
    pause()


def nmap_check():
    clear()
    line()
    slow("AUTHORIZED SINGLE-HOST CHECK", C)
    line()
    print("Only scan a system you own or have explicit permission to test.")
    target = input("Single IP or hostname (no ranges): ").strip()
    if (
        not target or target.startswith("-") or "/" in target
        or any(c.isspace() for c in target) or len(target) > 253
    ):
        print(f"{R}Invalid target. Enter one host only.{X}")
        pause()
        return
    if not shutil.which("nmap"):
        print("Install with: apt install nmap")
        pause()
        return
    if input("Type AUTHORIZED to confirm permission: ").strip() != "AUTHORIZED":
        print("Cancelled.")
        pause()
        return
    run_cmd([
        "nmap", "-sT", "-F", "-T3", "--reason",
        "--host-timeout", "60s", target
    ], timeout=90)
    pause()



def install_tool():
    clear()
    line()
    slow("DEFENSIVE TOOL INSTALLER", C)
    line()

    packages = {
        "1": ("Lynis audit", "lynis"),
        "2": ("ClamAV scanner", "clamav"),
        "3": ("Nmap host checker", "nmap"),
        "4": ("YARA", "yara"),
        "5": ("Fail2ban", "fail2ban"),
        "6": ("Suricata IDS", "suricata"),
        "7": ("AIDE file integrity", "aide"),
        "8": ("Auditd", "auditd"),
        "9": ("Rkhunter", "rkhunter"),
        "10": ("Chkrootkit", "chkrootkit"),
        "11": ("Tcpdump", "tcpdump"),
        "12": ("UFW firewall", "ufw"),
        "13": ("Git", "git"),
        "14": ("Curl", "curl"),
        "15": ("Wget", "wget"),
        "16": ("Nftables", "nftables"),
        "17": ("Wireshark", "wireshark"),
        "18": ("AppArmor utilities", "apparmor-utils"),
        "19": ("Unattended upgrades", "unattended-upgrades"),
        "20": ("Debsums file verification", "debsums"),
        "21": ("DNS utilities", "dnsutils"),
        "22": ("Net-tools", "net-tools"),
        "23": ("IP routing utilities", "iproute2"),
        "24": ("GnuPG", "gnupg"),
        "25": ("JSON command-line tools", "jq"),
        "26": ("System activity tools", "sysstat"),
        "27": ("Process viewer", "htop"),
        "28": ("Rsyslog", "rsyslog"),
        "29": ("OpenSSH server", "openssh-server"),
        "30": ("File integrity utilities", "integrit"),
    }

    for key, (name, package) in packages.items():
        print(f"{G}[{key:>2}]{X} {name} ({package})")
    print(f"{Y}[0]{X} Back")

    choice = input("\nSelect package: ").strip()
    if choice == "0":
        return
    if choice not in packages:
        print("Invalid selection.")
        pause()
        return
    if not shutil.which("apt-get"):
        print("APT is not available.")
        pause()
        return

    name, package = packages[choice]
    print(f"\nSelected: {name}")
    print("This installs software from your configured APT repositories.")
    if input("Type INSTALL to continue: ").strip() != "INSTALL":
        print("Cancelled.")
        pause()
        return

    try:
        result = subprocess.run(["apt-get", "install", "-y", package], check=False)
        print(f"\nAPT exit code: {result.returncode}")
    except OSError as exc:
        print(f"Installer error: {exc}")
    pause()


def clone_repo():
    import json
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

    clear()
    line()
    slow("DEFENSIVE GITHUB REPOSITORY BROWSER", C)
    line()
    print("Searching blue-team, DFIR, incident-response and monitoring projects.")
    print("Results are public GitHub repositories, not a guarantee of safety.")
    print("The browser downloads source only; it never executes cloned code.")

    query = "blue-team"
    url = "https://api.github.com/search/repositories?" + urlencode({
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
    })

    try:
        request = Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "ZAKA-Defensive-Console",
            },
        )
        with urlopen(request, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
        repositories = data.get("items", [])[:100]
    except Exception as exc:
        print(f"{Y}GitHub search failed: {exc}{X}")
        print("Check internet access, GitHub availability and API rate limits.")
        pause()
        return

    if not repositories:
        print("No repositories returned by GitHub.")
        pause()
        return

    print(f"\nFound {len(repositories)} repositories (maximum 100):")
    for index, repo in enumerate(repositories, 1):
        name = repo.get("full_name", "unknown")
        stars = repo.get("stargazers_count", 0)
        description = (repo.get("description") or "No description").replace("\n", " ")
        if len(description) > 88:
            description = description[:85] + "..."
        print(f"{G}[{index:03}]{X} {name}  ★ {stars}")
        print(f"      {description}")

    print(f"\n{Y}[0]{X} Back")
    choice = input("Repository number to clone: ").strip()
    if choice == "0":
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(repositories)):
        print("Invalid selection.")
        pause()
        return
    if not shutil.which("git"):
        print("Git is not installed. Use the tool installer first.")
        pause()
        return

    repo = repositories[int(choice) - 1]
    full_name = repo.get("full_name", "")
    clone_url = repo.get("clone_url", "")
    if (
        not full_name or not clone_url.startswith("https://github.com/")
        or ".." in full_name or full_name.startswith("/")
    ):
        print("Repository metadata did not pass basic validation.")
        pause()
        return

    folder = full_name.replace("/", "__")
    destination = REPO_DIR / folder
    REPO_DIR.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        print(f"Destination already exists: {destination}")
        pause()
        return

    print(f"\nRepository: {full_name}")
    print(f"Description: {repo.get('description') or 'No description'}")
    print("Review the repository, its maintainers, code and license before use.")
    if input("Type CLONE to download source only: ").strip() != "CLONE":
        print("Cancelled.")
        pause()
        return

    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", clone_url, str(destination)],
            check=False,
            timeout=600,
        )
        if result.returncode == 0:
            print(f"{G}Source cloned to: {destination}{X}")
            print("No scripts or installers were automatically executed.")
        else:
            print(f"{R}Git clone failed with exit code {result.returncode}.{X}")
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"Clone error: {exc}")
    pause()


def clone_zaka_launcher():
    import subprocess
    from pathlib import Path

    url = "https://github.com/zakakingpapa-pixel/zaka-red-hackers-team.git"
    dest = Path.home() / "zaka-defensive-repositories" / "zaka-red-hackers-team-codex-launcher"

    print("\nZAKA RED HACKERS TEAM — CODEX LAUNCHER")
    print("Repository:", url)
    print("Destination:", dest)

    if dest.exists():
        print("\nRepository folder already exists:", dest)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        confirm = input('Type CLONE to download this repository: ').strip()
        if confirm != "CLONE":
            print("Cancelled.")
            pause()
            return
        result = subprocess.run(["git", "clone", "--depth", "1", url, str(dest)])
        if result.returncode != 0:
            print("Clone failed. Check Git and internet access.")
            pause()
            return

    launcher = dest / "zaka-red-hackers-team"
    print("\nINSTALL AND RUN INSTRUCTIONS")
    print("1. Install Node.js and npm if they are not installed.")
    print("2. Install Codex CLI:")
    print("   npm install -g @openai/codex@latest")
    print("3. Enter the downloaded folder:")
    print("   cd " + str(dest))
    print("4. Make the launcher executable:")
    print("   chmod +x zaka-red-hackers-team")
    print("5. Start the launcher:")
    print("   ./zaka-red-hackers-team")
    print("6. Follow the Codex sign-in prompts using your own account.")
    print("\nRun these commands manually after reviewing the repository.")
    print("The launcher has not been executed automatically.")
    pause()


def menu():
    clear()
    print(R + r"""
╔══════════════════════════════════════════════════════════════╗
║                 ZAKA SECURITY CONSOLE                       ║
╚══════════════════════════════════════════════════════════════╝
""" + X)
    items = [
        ("01", "System information"),
        ("02", "Internet connectivity"),
        ("03", "DNS lookup"),
        ("04", "HTTPS/TLS check"),
        ("05", "Firewall status"),
        ("06", "Local listening ports"),
        ("07", "Fail2ban status"),
        ("08", "Available package updates"),
        ("09", "Lynis security audit"),
        ("10", "ClamAV folder scan"),
        ("11", "Authorized single-host Nmap check"),
        ("12", "Install defensive tools"),
        ("13", "Clone curated GitHub repositories"),
        ("14", "Security service status"),
        ("15", "Clone ZAKA Codex launcher repository"),
    ]
    for number, label in items:
        print(f"{G}[{number}]{X} {W}{label}{X}")
    print(f"{R}[00]{X} Exit")
    line("─", C)


def main():
    intro()
    actions = {
        "1": system_info, "01": system_info,
        "2": internet_check, "02": internet_check,
        "3": dns_check, "03": dns_check,
        "4": tls_check, "04": tls_check,
        "5": firewall_check, "05": firewall_check,
        "6": local_ports, "06": local_ports,
        "7": fail2ban_check, "07": fail2ban_check,
        "8": updates_check, "08": updates_check,
        "9": lynis_audit, "09": lynis_audit,
        "10": clamav_scan,
        "11": nmap_check,
        "12": install_tool,
        "13": clone_repo,
        "14": service_status,
        "15": clone_zaka_launcher,
    }
    while True:
        menu()
        choice = input(f"\n{R}ZAKA{X}@{G}DEFENSE{X} > ").strip().lower()
        if choice in ("0", "00", "exit", "quit"):
            speak("Zaka defensive console shutting down. Stay safe.")
            print(f"{G}Stay safe. Console closed.{X}")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print(f"{R}Invalid selection.{X}")
            time.sleep(0.8)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Y}Console interrupted. Goodbye.{X}")
