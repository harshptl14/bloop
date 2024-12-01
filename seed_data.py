from app.database import initialize_database, add_record
from datetime import datetime
def seed_data():
    """Seed the database with initial data."""
    apps = [
        ("Chrome", "2024-11-24T09:00:00"),
        ("Visual Studio Code", "2024-11-24T09:30:00"),
        ("Slack", "2024-11-24T10:00:00"),
        ("Spotify", "2024-11-24T10:30:00"),
        # Add more apps
        ("ARC", datetime.now().isoformat()),  # Added comma here
        ("Safari", datetime.now().isoformat())
    ]

    initialize_database()
    for app_name, timestamp in apps:
        add_record(app_name, timestamp)
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
