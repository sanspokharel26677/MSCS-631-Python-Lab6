# MSCS-631-Python-Lab6

# ICMP Traceroute Implementation in Python

## Overview
This project implements a basic **ICMP Traceroute** application in Python, allowing users to trace the route taken by packets from their machine to a specified destination. The program sends **ICMP Echo Requests** with incrementing TTL values and records the responses from intermediate routers until the final destination is reached.

## Features
- Uses **ICMP Echo Requests (Type 8)** and handles **ICMP Time Exceeded (Type 11)** and **ICMP Echo Reply (Type 0)** responses.
- Dynamically **accepts a user-input hostname** for traceroute instead of a hardcoded destination.
- Implements **timeout handling** and retries for each TTL value.
- Displays **round-trip time (RTT)** for each hop.
- Includes a **maximum execution time limit** of 10 seconds to prevent infinite execution.
- Handles **keyboard interruption gracefully**, providing a user-friendly exit message.

## Prerequisites
Before running the program, ensure that:
- You have **Python 3.x** installed.
- You run the script with **administrator/root privileges**, as raw sockets require elevated permissions.
- Your firewall or antivirus does not block **ICMP traffic** (optional but recommended).

## Installation
1. Clone this repository or download the script file.
2. Open a terminal and navigate to the project directory.
3. Ensure Python is installed by running:
   ```bash
   python3 --version
   ```

## Usage
To run the traceroute program, use:
```bash
sudo python3 traceroute.py
```
The program will prompt you to **enter a hostname** (e.g., `google.com`) and display the traceroute output.

### Example Run
```
Enter a hostname to trace route (e.g., google.com): www.google.com
 1   rtt=2 ms    192.168.1.1
 2   *    *    *    Request timed out.
 3   rtt=12 ms   159.111.144.122
 ...
 16  rtt=46 ms   172.217.4.196
```

## Expected Output
- Each line represents a **network hop**, showing the **RTT** and the responding router's IP.
- If a router does not respond, `Request timed out` is displayed.
- If the destination is unreachable, the program indicates `Destination Unreachable`.
- The program stops automatically if it reaches the final destination or **10 seconds elapse**.

## Challenges and Considerations
- Some routers **do not respond to ICMP** packets, causing timeouts.
- Certain destinations **block ICMP traffic** (e.g., YouTube returned `Destination Unreachable`).
- Running with **sudo/root privileges** is mandatory due to raw socket usage.
- The program **stops after 10 seconds** if the destination is not reached within that time.

## License
This project is provided for educational purposes and is open-source. Feel free to modify and enhance it!

## Author
**Sandesh Pokharel**

For any questions or improvements, feel free to contribute or reach out!


