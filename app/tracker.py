import os
import time
import sqlite3
from datetime import datetime
from database import add_record

def get_running_apps():
    """Get a list of all currently running applications on macOS."""
    cmd = """
    osascript -e '
        tell application "System Events"
            set appList to name of every application process where background only is false
        end tell
    '
    """
    try:
        result = os.popen(cmd).read().strip()
        # Split the result into a list and remove empty strings
        apps = [app.strip() for app in result.split(',') if app.strip()]
        return apps
    except Exception as e:
        print(f"Error getting running apps: {e}")
        return []

def track_app_usage():
    """Track all running apps and save to database every minute."""
    try:
        last_recorded_minute = None
        while True:
            current_time = datetime.now()
            current_minute = current_time.strftime('%Y-%m-%d %H:%M')
            
            # Only record if we're in a new minute
            if current_minute != last_recorded_minute:
                running_apps = get_running_apps()
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                
                print(f"\nTracking apps at {timestamp}:")
                for app in running_apps:
                    try:
                        add_record(app, timestamp)
                        print(f"✓ {app}")
                    except sqlite3.Error as e:
                        print(f"✗ Error tracking {app}: {e}")
                
                last_recorded_minute = current_minute
                print(f"Total apps tracked: {len(running_apps)}")
            
            # Sleep for a short time to prevent high CPU usage
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTracking stopped.")
