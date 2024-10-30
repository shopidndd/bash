import os
import sqlite3
import subprocess
import time
import threading

# Set up SQLite database
DB_PATH = "monitoring_logs.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS file_changes (timestamp TEXT, event TEXT, path TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS network_activity (timestamp TEXT, connection TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS syslog (timestamp TEXT, message TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS auth_log (timestamp TEXT, message TEXT)''')
conn.commit()

# Insert log entry into the database
def insert_log(table, data):
    cursor.execute(f"INSERT INTO {table} VALUES (?, ?)", data)
    conn.commit()

# Monitor file changes in /tmp
def monitor_file_changes():
    while True:
        result = subprocess.run(["inotifywait", "-e", "create,delete,modify,attrib", "/tmp"], capture_output=True, text=True)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        insert_log("file_changes", (timestamp, result.stdout.strip(), "/tmp"))
        time.sleep(1)

# Monitor network activity for specific ports or IPs
def monitor_network_activity():
    while True:
        result = subprocess.run(["netstat", "-tunap"], capture_output=True, text=True)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        for line in result.stdout.splitlines():
            if "4444" in line or "192.168.1.100" in line:
                insert_log("network_activity", (timestamp, line.strip()))
        time.sleep(2)

# Monitor syslog and auth log
def monitor_system_logs():
    syslog_path = "/var/log/syslog"
    authlog_path = "/var/log/auth.log"
    with open(syslog_path, "r") as syslog, open(authlog_path, "r") as authlog:
        syslog.seek(0, os.SEEK_END)
        authlog.seek(0, os.SEEK_END)
        while True:
            syslog_line = syslog.readline()
            authlog_line = authlog.readline()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            if syslog_line:
                insert_log("syslog", (timestamp, syslog_line.strip()))
            if authlog_line:
                insert_log("auth_log", (timestamp, authlog_line.strip()))
            time.sleep(1)

# Close database connection on exit
def close_connection():
    conn.close()

# Start monitoring in background
file_thread = threading.Thread(target=monitor_file_changes)
network_thread = threading.Thread(target=monitor_network_activity)
syslog_thread = threading.Thread(target=monitor_system_logs)

file_thread.start()
network_thread.start()
syslog_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    close_connection()

