from database import initialize_database, fetch_records
from tracker import track_app_usage
from prediction import BloomFilter, CountMinSketch
from datetime import datetime

def predict_apps():
    """Predict frequently used apps based on history."""
    current_hour = datetime.now().hour
    prev_hour = (current_hour - 1) % 24
    next_hour = (current_hour + 1) % 24
    
    query = """
        SELECT app_name, COUNT(*) as count 
        FROM app_usage 
        WHERE CAST(strftime('%H', timestamp) AS INTEGER) BETWEEN ? AND ?
        GROUP BY app_name 
        ORDER BY count DESC
    """
    # Use the earlier hour and later hour for the range
    hours = (min(prev_hour, current_hour, next_hour), 
            max(prev_hour, current_hour, next_hour))
    app_usage = fetch_records(query, hours)

    print(f"Debug - Checking apps used between {hours[0]}:00 and {hours[1]}:00")
    print("Debug - Query results:", app_usage)
    
    if not app_usage:
        print(f"\nNo app usage data found for time period {hours[0]}:00-{hours[1]}:00.")
        return

    # Initialize Bloom Filter and Count-Min Sketch
    bloom = BloomFilter(size=1000, hash_count=5)
    cms = CountMinSketch(width=500, depth=5)

    # Add apps to both data structures with their frequencies
    for app, count in app_usage:
        for _ in range(int(count)):  # Add multiple times based on frequency
            bloom.add(app)
            cms.add(app)

    # Predict frequently used apps
    print(f"\nPredicted frequently used apps for time period {hours[0]}:00-{hours[1]}:00:")
    predictions = [(app, cms.count(app)) for app, _ in app_usage if bloom.check(app)]
    predictions.sort(key=lambda x: x[1], reverse=True)

    for app, frequency in predictions[:5]:  # Show top 5 predictions
        print(f"- {app} (likely to be used {frequency} times)")

def main():
    initialize_database()
    while True:
        print("\n1. Track App Usage")
        print("2. Predict Frequently Used Apps")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            track_app_usage()
        elif choice == "2":
            predict_apps()
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
