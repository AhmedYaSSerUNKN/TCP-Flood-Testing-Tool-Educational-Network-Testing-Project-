# TCP Flood Testing Tool – Educational Network Testing Project

This is an educational tool designed to demonstrate TCP/HTTP connection handling and network stress testing. It simulates multiple concurrent connections to a web server to help understand network behavior, threading, and socket programming in Python.

## Features

- TCP Flood Testing: Simulate multiple simultaneous TCP connections to a target server.
- HTTP Flood Testing: Optionally send HTTP requests for web server stress testing.
- Multithreading: Manage large numbers of connections efficiently using Python threads.
- Configurable Parameters: Easily set target IP, port, number of threads, and requests.
- Educational Comments: Well-commented code for learning purposes.

## Disclaimer

**This tool is for educational and research purposes only.**
Do not use it to attack or disrupt any network or server without explicit permission. Unauthorized use may be illegal and unethical.

## Requirements

- Python 3.x (no external dependencies; uses standard library)

## Installation

```bash
git clone https://github.com/AhmedYaSSerUNKN/TCP-Flood-Testing-Tool-Educational-Network-Testing-Project-.git
cd TCP-Flood-Testing-Tool-Educational-Network-Testing-Project-
```

## Usage

```bash
python tcp_flood.py --target <IP> --port <PORT> --threads <NUM_THREADS> --requests <NUM_REQUESTS>
```

**Example:**
```bash
python tcp_flood.py --target 192.168.1.100 --port 80 --threads 100 --requests 1000
```

**Parameters:**
- `--target`: Target server IP address or domain name
- `--port`: Target server port (e.g., 80 for HTTP)
- `--threads`: Number of concurrent threads/connections
- `--requests`: Total number of requests per thread

## How It Works

- Spawns multiple threads, each initiating TCP (or optionally HTTP) connections to the target server.
- Each thread can send a configurable number of requests.
- Useful for understanding how servers handle many simultaneous connections, and for learning about sockets and threading in Python.

## Example Output

```
[+] Thread 1: Successfully connected to 192.168.1.100:80
[+] Thread 2: Successfully connected to 192.168.1.100:80
...
```

## Educational Value

- Learn about network programming in Python.
- Understand threading and concurrency.
- Observe network/server behavior under stress.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

## Author

Ahmed Yasser Lotfy Belaih
