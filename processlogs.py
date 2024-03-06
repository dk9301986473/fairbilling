from datetime import datetime, timedelta
import sys

def process_log_file(file_path):
    # Dictionary to store user sessions
    user_sessions = {}

    # Variables to track earliest and latest times in the log file
    earliest_time = None
    latest_time = None

    # List to track active sessions with no matching "End"
    active_sessions = {}

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Split the line into components
            components = line.strip().split(' ')

            # Ignore invalid lines
            if len(components) != 3:
                print(f"Warning: Invalid line at line {line_number}: {line}")
                continue

            timestamp_str, username, action = components

            try:
                timestamp = datetime.strptime(timestamp_str, '%H:%M:%S')
            except ValueError:
                print(f"Warning: Invalid timestamp at line {line_number}: {line}")
                continue

            # Update earliest and latest times
            if earliest_time is None or timestamp < earliest_time:
                earliest_time = timestamp
            if latest_time is None or timestamp > latest_time:
                latest_time = timestamp

            # Update user sessions
            if username not in user_sessions:
                user_sessions[username] = []

            if action == 'Start':
                # Start a new session
                user_sessions[username].append({'start': timestamp})
                active_sessions[username] = timestamp
            elif action == 'End':
                # End the latest active session for the user if there are active sessions
                if username in active_sessions:
                    user_sessions[username].append({'start': active_sessions[username], 'end': timestamp})
                    del active_sessions[username]
                else:
                    # If there are no active sessions, handle the case appropriately
                    print(f"Warning: 'End' action with no matching 'Start' for {username} at {timestamp}")

    # Handle active sessions with no matching "End"
    for username, start_time in active_sessions.items():
        user_sessions[username].append({'start': start_time, 'end': latest_time})

    # Print the headers
    print("Username\tSessions\tTotal Duration (seconds)")

    # Calculate and print the results
    print_results(user_sessions, latest_time)

def print_results(user_sessions, latest_time):
    for username, sessions in user_sessions.items():
        total_duration = 0
        num_sessions = 0

        for session in sessions:
            if 'end' not in session:
                # Set the end time to be the latest time in the file
                session['end'] = latest_time

            duration = (session['end'] - session['start']).total_seconds()
            total_duration += duration
            num_sessions += 1

        print(f"{username}\t{num_sessions}\t{int(total_duration)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]
        process_log_file(file_path)
