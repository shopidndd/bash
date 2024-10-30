#!/bin/bash

# Unified Monitoring Script
LOG_DIR="/tmp/monitoring_logs"
mkdir -p "$LOG_DIR"

# Define log files for each monitored component
FILE_CHANGE_LOG="$LOG_DIR/file_changes.log"
NETWORK_LOG="$LOG_DIR/network_activity.log"
SYSLOG_LOG="$LOG_DIR/syslog.log"
AUTH_LOG="$LOG_DIR/auth_log.log"
PROCESS_LOG="$LOG_DIR/process_activity.log"
CRON_LOG="$LOG_DIR/cron_jobs.log"
AUDIT_LOG="$LOG_DIR/audit_log.log"

echo "Starting unified monitoring. Logs are saved in $LOG_DIR."

# Monitor file changes in /tmp and log them
inotifywait -m /tmp -e create -e delete -e modify -e attrib > "$FILE_CHANGE_LOG" &
echo "File change monitoring started for /tmp. Logging to $FILE_CHANGE_LOG."

# Monitor network connections (specific IP/port) and log them
watch -n 2 "netstat -tunap | grep -E '4444|192.168.1.100'" > "$NETWORK_LOG" &
echo "Network activity monitoring started. Logging to $NETWORK_LOG."

# Monitor system logs for suspicious activity and log them
tail -f /var/log/syslog > "$SYSLOG_LOG" &
echo "Syslog monitoring started. Logging to $SYSLOG_LOG."

tail -f /var/log/auth.log > "$AUTH_LOG" &
echo "Auth log monitoring started. Logging to $AUTH_LOG."

# Monitor specific processes related to suspicious activity and log them
watch -n 2 "ps aux | grep -E 'bash|tcpdump|nc'" > "$PROCESS_LOG" &
echo "Process activity monitoring started. Logging to $PROCESS_LOG."

# Monitor cron jobs for any new entries and log them
watch -n 60 "crontab -l" > "$CRON_LOG" &
echo "Cron job monitoring started. Logging to $CRON_LOG."

# Monitor audit logs if available
if [ -f /var/log/audit/audit.log ]; then
  tail -f /var/log/audit/audit.log > "$AUDIT_LOG" &
  echo "Audit log monitoring started. Logging to $AUDIT_LOG."
else
  echo "Audit log not found. Skipping audit monitoring."
fi

echo "Unified monitoring is now active. Press Ctrl+C to stop monitoring."

# Wait for all background processes to complete
wait
"""

import base64

# Encode the Bash script content
encoded_bash_script = base64.b64encode(bash_script_content.encode()).decode()

# Step 2: Write the encoded content to a Python script that can decode and execute it
decode_and_execute_script = f"""\
import base64
import subprocess

# Encoded Bash script
encoded_script = \"\"\"{encoded_bash_script}\"\"\"

# Decode and execute
decoded_script = base64.b64decode(encoded_script).decode()
subprocess.run(decoded_script, shell=True)
"""

# Save the decode-and-execute script to a Python file
with open("/mnt/data/decode_and_execute_script.py", "w") as f:
    f.write(decode_and_execute_script)

