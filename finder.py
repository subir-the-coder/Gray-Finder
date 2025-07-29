#!/usr/bin/env python3
import requests
import random
import re
import sys
import time
import argparse
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style, init
import socket
import os
import warnings
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

# commenting in every section to remember, anyone who wants to modify please write in comments in details

#colorama
init(autoreset=True)
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# ======================
# My BANNER
# Coder : Subir Sutradhar (Gray Code)
# Educational and authorized use only. Do not run this tool against targets you do not own or have explicit permission to test.
# ======================
def show_banner():
    print(Fore.RED + Style.BRIGHT + r"""
  ▄████  ██▀███   ▄▄▄     ▓██   ██▓     █████▒██▓ ███▄    █ ▓█████▄ ▓█████  ██▀███  
 ██▒ ▀█▒▓██ ▒ ██▒▒████▄    ▒██  ██▒   ▓██   ▒▓██▒ ██ ▀█   █ ▒██▀ ██▌▓█   ▀ ▓██ ▒ ██▒
▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄   ▒██ ██░   ▒████ ░▒██▒▓██  ▀█ ██▒░██   █▌▒███   ▓██ ░▄█ ▒
░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██  ░ ▐██▓░   ░▓█▒  ░░██░▓██▒  ▐▌██▒░▓█▄   ▌▒▓█  ▄ ▒██▀▀█▄  
░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒ ░ ██▒▓░   ░▒█░   ░██░▒██░   ▓██░░▒████▓ ░▒████▒░██▓ ▒██▒
 ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░  ██▒▒▒     ▒ ░   ░▓  ░ ▒░   ▒ ▒  ▒▒▓  ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
  ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░▓██ ░▒░     ░      ▒ ░░ ░░   ░ ▒░ ░ ▒  ▒  ░ ░  ░  ░▒ ░ ▒░
░ ░   ░   ░░   ░   ░   ▒   ▒ ▒ ░░      ░ ░    ▒ ░   ░   ░ ░  ░ ░  ░    ░     ░░   ░ 
      ░    ░           ░  ░░ ░                ░           ░    ░       ░  ░   ░     
                           ░ ░                               ░                      """)
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n                      G R A Y   F I N D E R v1.0")
    print(Fore.WHITE + Style.BRIGHT + "               The Web's Darkest Secrets Revealed | Crazy Automater\n")

# ======================
# CONFIGURATION NEEEDED, ADD MORE PATH IF KNOWN
# ======================
DEFAULT_PATHS = [
    '',  # Root path
    'admin/', 'wp-admin/', 'administrator/', 
    'login/', 'dashboard/', 'cpanel/',
    'robots.txt', 'sitemap.xml', '.env',
    'phpinfo.php', 'test.php', 'config.php',
    '.git/', 'backup/', 'wp-config.php',
    'debug.php', 'api/', 'wp-json/',
    'phpmyadmin/', 'mysql/', 'dbadmin/'
]

# ======================
# MAIN SCANNER
# ======================
class GrayFinder:
    def __init__(self):
        self.config = {
            'delay': 1.5,
            'timeout': 20,
            'max_retries': 2,
            'verify_ssl': True,
            'user_agents': [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Googlebot/2.1 (+http://www.google.com/bot.html)"
            ],
            'headers': {
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'DNT': '1'
            }
        }
        self.found = set()
    
    def get_headers(self):
        headers = self.config['headers'].copy()
        headers['User-Agent'] = random.choice(self.config['user_agents'])
        headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        return headers
    
    def test_url(self, url):
        for attempt in range(self.config['max_retries']):
            try:
                time.sleep(self.config['delay'])
                response = requests.get(
                    url,
                    headers=self.get_headers(),
                    timeout=self.config['timeout'],
                    verify=self.config['verify_ssl'],
                    allow_redirects=True
                )
                return response
            except requests.exceptions.SSLError:
                print(Fore.YELLOW + f"[!] SSL Error - Trying without verification: {url}")
                self.config['verify_ssl'] = False
                continue
            except Exception as e:
                if attempt == self.config['max_retries'] - 1:
                    return None
                time.sleep(1)
        return None
    
    def scan(self, base_url, paths):
        results = []
        for path in paths:
            target_url = urljoin(base_url, path)
            print(f"Testing: {target_url.ljust(80)}", end='\r')
            
            response = self.test_url(target_url)
            if not response:
                results.append((target_url, "Connection failed"))
                continue
            
            if response.status_code == 200:
                self.found.add(target_url)
                status = "Accessible"
                
                sensitive = self.find_sensitive_data(response.text)
                if sensitive:
                    status = f"Accessible (Sensitive data found : {', '.join(sensitive)})"
                
                results.append((target_url, status))
            
            elif response.status_code in [401, 403]:
                results.append((target_url, "Protected"))
            else:
                results.append((target_url, f"HTTP {response.status_code}"))
        
        return results
    
    def find_sensitive_data(self, content):
        patterns = [
            r"(api[_-]?key|secret)[=:]\s*[\w-]+",
            r"password\s*=\s*['\"]?[\w!@#$%^&*()]+",
            r"(aws_access_key_id|aws_secret_access_key)\s*=\s*[\w-]+",
            r"db_(user|pass|host|name)\s*=\s*['\"][^'\"]+['\"]",
            r"(\b[A-Za-z0-9+/]{40,}\b|\b[A-Za-z0-9+/]{20,}={0,2}\b)"  
        ]
        found = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            found.extend(matches)
        return list(set(found))

# ======================
# CLI
# ======================
def load_custom_paths(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return []

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="Gray Finder - Advanced Web Path Scanner")
    parser.add_argument("url", help="Target URL (e.g., https://example.com)")
    parser.add_argument("-w", "--wordlist", help="Custom wordlist file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--no-ssl", action="store_true", help="Disable SSL verification")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads (default: 5)")
    args = parser.parse_args()
    
    # Initializing scanner
    scanner = GrayFinder()
    if args.no_ssl:
        scanner.config['verify_ssl'] = False
    
    # Target
    base_url = args.url if args.url.startswith(('http://', 'https://')) else f'https://{args.url}'
    domain = urlparse(base_url).netloc
    
    # Preparing paths
    paths = DEFAULT_PATHS
    if args.wordlist:
        custom_paths = load_custom_paths(args.wordlist)
        paths.extend(custom_paths)
    
    # Verifing connection
    try:
        port = 443 if base_url.startswith('https://') else 80
        socket.create_connection((domain, port), timeout=10)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to connect to {domain}: {str(e)}")
        sys.exit(1)
    
    # Scanning started
    print(f"\n{Fore.CYAN}Scanning {base_url} with {len(paths)} paths using {args.threads} threads...\n")
    
    # Threading for faster scanning
    results = []
    
    def scan_path(path):
        return scanner.scan(base_url, [path])[0]
    
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(scan_path, path) for path in paths]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    # Result Section
    print("\n" + "="*80)
    for url, status in results:
        if "Accessible" in status:
            color = Fore.GREEN
        elif "Sensitive" in status:
            color = Fore.RED
        elif "Protected" in status:
            color = Fore.YELLOW
        else:
            color = Fore.BLUE
        print(f"{color}[{status[0]}] {url} - {status}")
    
    # Saving Results
    if args.output:
        with open(args.output, 'w') as f:
            f.write(f"Scan results for {base_url}\n")
            f.write(f"Scanned paths: {len(paths)}\n")
            f.write(f"Found accessible: {len(scanner.found)}\n\n")
            for url, status in results:
                f.write(f"{url} - {status}\n")
        print(f"\n{Fore.GREEN}Results saved to {args.output}")

if __name__ == "__main__":
    main()
