#!/usr/bin/env python3

import re
import csv
from collections import defaultdict

error_messages = defaultdict(int)
per_user = defaultdict(lambda: {"INFO": 0, "ERROR": 0})

with open("syslog.log") as file:
    for line in file:
        # Use regular expressions to extract information from each log entry
        pattern = r"(INFO|ERROR) (.*) \((.*)\)"
        result = re.search(pattern, line)

        if result:
            log_type, message, user = result.groups()

            # Update the error_messages dictionary
            if log_type == "ERROR":
                error_messages[message] += 1

            # Update the per_user dictionary
            per_user[user][log_type] += 1

# Sort the error_messages dictionary by count in descending order
sorted_errors = sorted(error_messages.items(), key=lambda x: x[1], reverse=True)

# Add column names and write to error_message.csv
with open("error_message.csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Error", "Count"])
    writer.writerows(sorted_errors)

# Sort the per_user dictionary by username
sorted_users = sorted(per_user.items())

# Add column names and write to user_statistics.csv
with open("user_statistics.csv", "w") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Username", "INFO", "ERROR"])
    for user, log_counts in sorted_users:
        writer.writerow([user, log_counts["INFO"], log_counts["ERROR"]])
