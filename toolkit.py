import argparse
import sys
from modules import port_scanner, ftp_bruteforce

def print_banner():
    print("""
    ================================================
    🛡️   PENETRATION TESTING TOOLKIT v1.0   🛡️
    ================================================
    """)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Modular Penetration Testing Toolkit")
    subparsers = parser.add_subparsers(dest="module", help="Available Modules")

    # Port Scanner Module
    port_parser = subparsers.add_parser("portscan", help="Run the Port Scanner")
    port_parser.add_argument("target", help="Target IP or hostname")
    port_parser.add_argument("-p", "--ports", default="1-1024", help="Port range (e.g., 1-1024)")
    port_parser.add_argument("-t", "--threads", type=int, default=50, help="Number of threads")

    # FTP Bruteforce Module
    ftp_parser = subparsers.add_parser("ftpbrute", help="Run the FTP Brute-Forcer")
    ftp_parser.add_argument("target", help="Target FTP server IP or hostname")
    ftp_parser.add_argument("-u", "--user", required=True, help="Username to brute-force")
    ftp_parser.add_argument("-w", "--wordlist", required=True, help="Path to password dictionary file")

    args = parser.parse_args()

    if args.module == "portscan":
        start_port, end_port = map(int, args.ports.split('-'))
        port_scanner.run(args.target, start_port, end_port, args.threads)
    elif args.module == "ftpbrute":
        ftp_bruteforce.run(args.target, args.user, args.wordlist)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
