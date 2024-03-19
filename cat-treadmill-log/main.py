import time

# Constants
TREADMILL_DIAMETER = 1  # Diameter of the treadmill in meters
INTERVAL = 10  # Time interval in seconds
IGNORE_THRESHOLD = 1  # Ignore triggers within 1 second after the previous trigger

def calculate_distance_and_speed(start_time, end_time, trigger_count):
    """Calculate the distance and speed based on trigger count and time.

    Args:
        start_time (float): The start time of the record cycle.
        end_time (float): The end time of the record cycle.
        trigger_count (int): Number of triggers during the record cycle.

    Returns:
        tuple: A tuple containing the distance (in kilometers) and speed (in kilometers per hour).
    """
    elapsed_time = end_time - start_time
    distance = trigger_count * TREADMILL_DIAMETER * 3.14159  # Circumference = pi * diameter
    distance_km = distance / 1000  # Convert meters to kilometers
    speed = distance / elapsed_time  # Speed = distance / time
    speed_kmh = speed * 3600 / 1000  # Convert meters/second to kilometers/hour
    return distance_km, speed_kmh

def sensor_trigger():
    """Simulate sensor triggers at irregular intervals."""
    #  To simulate standard run
    for _ in range(5):
        time.sleep(2)
        yield True
    #  To simulate and test turns in direction - sensor triggered too fast
    time.sleep(0.3)
    yield True
    time.sleep(0.3)
    yield True
    #  To simulate when cat left but return - test end of old and start of new records
    time.sleep(12)
    yield True
    #  To simulate standard run
    for _ in range(5):
        time.sleep(2)
        yield True
    #  Needed to end old run
    time.sleep(12)
    yield True

def record_sensor_data(file_path):
    """Record sensor data periodically and write it to a file.

    Args:
        file_path (str): The file path to write the sensor data.
    """
    trigger_count = 0
    start_time = None
    end_time = None
    last_trigger_time = None

    sensor = sensor_trigger()

    while True:
        # Wait for sensor trigger
        next(sensor)
        print("sensor trigger")

        current_time = time.time()

        if start_time is None:
            start_time = current_time
            last_trigger_time = current_time
            continue  # Skip the rest of the loop to prevent counting this trigger

        time_since_last_trigger = current_time - last_trigger_time
        if time_since_last_trigger < IGNORE_THRESHOLD:
            print("Ignoring trigger within 1 second of previous trigger.")
            continue  # Skip the rest of the loop

        if current_time - start_time >= INTERVAL:
            print("Over 10 seconds since last trigger - end this record cycle")
            end_time = current_time
            distance, speed = calculate_distance_and_speed(start_time, end_time, trigger_count)
            with open(file_path, "a") as file:
                file.write(f"Start time: {time.strftime('%H:%M:%S - %d/%m/%y', time.localtime(start_time))} - ")
                file.write(f"End time: {time.strftime('%H:%M:%S - %d/%m/%y', time.localtime(end_time))}\n")
                file.write(f"Distance: {distance:.2f} kilometers\n")  # Updated to kilometers
                file.write(f"Speed: {speed:.2f} kilometers/hour\n\n")  # Updated to kilometers/hour

            start_time = current_time
            trigger_count = 0

        trigger_count += 1
        last_trigger_time = current_time

if __name__ == "__main__":
    file_path = "log.txt"
    record_sensor_data(file_path)
