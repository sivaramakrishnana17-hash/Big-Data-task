# Ajio Real-Time Log Harvesting System 🛍️📡

Our project acts as a central monitoring system that collects and processes logs from various simulated servers[cite: 4]. This is a robust, multi-threaded backend networking project built purely in Python that captures live server logs over TCP sockets, validates them in real-time, and stores them in a custom, space-efficient binary format.

## 🚀 Features & Architecture Flow

The system is built on an 8-step pipeline to handle high-velocity log data efficiently:

* **Step 1: Multiple Servers Generate Logs:** Every second, different systems (like a Login Server, Payment Server, or Database Server) generate logs documenting internal events[cite: 4].
* **Step 2: TCP Socket Communication:** The servers need a way to send logs to the monitoring system, so a TCP socket acts like a communication channel[cite: 4]. The socket ensures data reaches correctly, arrives in order, and no messages are lost[cite: 4].
* **Step 3: Multiple Simulated Servers:** Since we do not have real servers, we create Python programs that behave like them (simulated server instances)[cite: 4].
* **Step 4: Multi-Threaded Log Harvesting Daemon:** A single worker cannot handle everything efficiently, so threads are used[cite: 4]. Multiple workers (threads) handle the Login, Payment, and Database servers simultaneously (multi-threading)[cite: 4]. 
* **Step 5: Real-Time Stream Buffer Handling:** Sometimes the network may break the message, and the system cannot process incomplete information[cite: 4]. The system temporarily stores incoming data in a buffer until it forms a complete log[cite: 4].
* **Step 6: Regex Validation:** The system checks "Is this a proper log?" using a Regex pattern that acts like a security guard[cite: 4]. It verifies if the logs follow the correct format with a Date, Level, and Message[cite: 4]. 
* **Step 7: Structured Payload Creation:** Raw text logs are converted into organized data, allowing the computer to understand each part separately for easy searching[cite: 4].
* **Step 8: Partitioned Binary Storage:** Instead of storing everything together, the system separates logs by severity level (INFO, ERROR, WARNING) into separate binary files[cite: 4]. This means if you only want failed transactions, the system directly opens ERROR logs instead of searching millions of records[cite: 4].

## 📂 Project Structure & Files

The project relies on three main Python scripts:

* `log_server_simulator.py` : Pretends to be high-velocity branch servers that fire log lines continuously at random intervals[cite: 2].
* `log_harvester_daemon.py` : The central monitoring system that opens TCP socket connections, slices the stream, validates with regex, builds payloads, and dynamically partitions data into binary files[cite: 3].
* `read_binary_logs.py` : Reads back the binary partition files and decodes them into human-readable log lines[cite: 1].

## 🛠️ Prerequisites

* Python 3.x installed on your system.
* A code editor (Visual Studio Code recommended).
* No external libraries required (built entirely using Python's standard library: `socket`, `threading`, `re`, `struct`).

## ⚙️ How to Run on VS Code

1. **Set Up the Workspace:**
   * Open VS Code and create a new folder named `Ajio_Log_Analyzer`.
   * Create the three required files inside this folder: `log_server_simulator.py`, `log_harvester_daemon.py`, and `read_binary_logs.py`.
   * Paste your respective Python code into each file and save them.

2. **Start the Simulated Servers:**
   * Open a terminal in VS Code (`Terminal -> New Terminal`).
   * Run the simulator script:
     ```bash
     python log_server_simulator.py
     ```
   * Leave this terminal running to continuously broadcast logs.

3. **Start the Log Harvester:**
   * Split your VS Code terminal (using the split icon next to the plus sign in the terminal panel) so you have two terminals side-by-side.
   * In the new terminal pane, run the harvester daemon:
     ```bash
     python log_harvester_daemon.py
     ```
   * You will see live statistics updating as it ingests data. 
   * A new folder named `partitions` will automatically appear in your file explorer containing the `.bin` files[cite: 3].
   * After 15–20 seconds, press `Ctrl+C` in the harvester terminal to safely shut it down.

4. **Decode and Read the Processed Binary Data:**
   * In the terminal, run the reader script and pass it one of the newly generated binary files to prove the data is structured and recoverable[cite: 1]. For example:
     ```bash
     python read_binary_logs.py partitions/ajio-chennai_ERROR.bin
     ```
   * It will output the completely decoded, human-readable log records[cite: 1].