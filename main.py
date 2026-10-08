import json
import os
from datetime import datetime
import argparse

SESSIONS_FILE = "sessions.json"

def load_sessions():
    """Read existing sessions from Json file, or start fresh if none exist."""
    if not os.path.exists(SESSIONS_FILE):
        return[]
    with open(SESSIONS_FILE, "r") as f:
        return json.load(f)
    
def save_sessions(sessions):
    """Write the full list of sessions back to the JSON file."""
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=2)

def log_session(project, duration_minutes, notes=''):
    """
    Record a new work session and save it to the JSON file
    
    :param project: Name of the current project
    :param duration_minutes: time spent on
    :param notes: pointers for what was done and some for next session
    """
    sessions = load_sessions()
    entry = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'project': project,
        'duration_minutes': duration_minutes,
        'notes' : notes
    }
    sessions.append(entry)
    save_sessions(sessions)

    print(f"Logged : {duration_minutes} min on {project}")

#log_session("dev-tracker", 45, "wrote the logger")

def view_sessions():
    """
    Print a summary of all logged sessions, plus total time spent.
    """
    sessions = load_sessions()
    if not sessions:
        print("No sessions logged yet.")
        return
    total_minutes = 0
    for s in sessions:
        print(f'{s['date']} - {s['project']} ({s['duration_minutes']} min): {s['notes']}')
        total_minutes += s['duration_minutes']

    print(f'\nTotal Sessions : {len(sessions)}')
    print(f'Total time: {total_minutes} ({total_minutes / 60:.1f} hours)')

def main():
    parser = argparse.ArgumentParser(description="Track your dev work sessions.")
    subparser = parser.add_subparsers(dest="command")

    log_parser = subparser.add_parser("log", help="Log a new session")
    log_parser.add_argument("--project", required=True, help='Project name')
    log_parser.add_argument("--minute", type=int, required=True, help='Duration in minutes')
    log_parser.add_argument('--notes', default='', help='optional notes')

    args = parser.parse_args()

    if args.command == "log":
        log_session(args.project, args.minute, args.notes)

if __name__ == "__main__":
    main()