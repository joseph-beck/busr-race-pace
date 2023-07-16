import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime
from scipy import stats


def make_continuous_race_pace(data_path, dark_mode=False, node=True):
    # Read data from CSV file
    data = []
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    # Collect lap times for each driver
    drivers = {}
    for entry in data:
        driver_name = entry['DriverName']
        lap_number = int(entry['LapNumber'])
        lap_time = entry['Lap']

        if driver_name not in drivers:
            drivers[driver_name] = {'LapNumber': [], 'LapTime': []}

        drivers[driver_name]['LapNumber'].append(lap_number)
        drivers[driver_name]['LapTime'].append(lap_time)

    # Remove lap time outliers using IQR method
    for driver_name, lap_data in drivers.items():
        lap_number = lap_data['LapNumber']
        lap_time = lap_data['LapTime']
        lap_number_filtered = []
        lap_time_filtered = []

        for lap_num, lap in zip(lap_number, lap_time):
            if ':' in lap:
                lap_time_dt = datetime.datetime.strptime(lap, '%M:%S.%f')
                lap_seconds = lap_time_dt.minute * 60 + lap_time_dt.second + lap_time_dt.microsecond / 1e6
            else:
                lap_seconds = float(lap)

            lap_number_filtered.append(lap_num)
            lap_time_filtered.append(lap_seconds)

        lap_number_filtered = np.array(lap_number_filtered)
        lap_time_filtered = np.array(lap_time_filtered)

        lap_time_sorted = np.sort(lap_time_filtered)
        q1 = np.percentile(lap_time_sorted, 25)
        q3 = np.percentile(lap_time_sorted, 40)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        is_valid = (lap_time_filtered >= lower_bound) & (lap_time_filtered <= upper_bound)
        lap_number_filtered = lap_number_filtered[is_valid]
        lap_time_filtered = lap_time_filtered[is_valid]

        lap_data['LapNumber'] = lap_number_filtered.tolist()
        lap_data['LapTime'] = lap_time_filtered.tolist()

    if dark_mode:
        # Enable dark mode for the plot
        plt.style.use('dark_background')

    # Plot the lap times for each driver with overlapping lines
    plt.figure(figsize=(16, 8))  # Adjust the figure size as needed

    for driver_name, lap_data in drivers.items():
        lap_number = lap_data['LapNumber']
        lap_time = lap_data['LapTime']

        if node:
            plt.plot(lap_number, lap_time, label=driver_name)
        else:
            plt.plot(lap_number, lap_time, marker='o', label=driver_name)

    plt.xlabel('Lap Number')
    plt.ylabel('Lap Time (seconds)')
    plt.title('Comparison of Lap Times for Drivers')
    plt.legend(loc='upper right', bbox_to_anchor=(1.125, 1), fontsize=10)
    plt.grid(True)

    plt.show()


def make_average_race_pace(data_path, dark_mode=False, threshold=3):
    # Create a dictionary to store lap times per driver
    lap_times_per_driver = {}

    # Read lap data from CSV file and extract lap times
    with open(data_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            driver_name = row['DriverName']
            lap_time = row['Lap']

            if lap_time.startswith('0'):
                continue

            if ':' in lap_time:
                split_lap_time = lap_time.split(':')
                minutes, seconds = split_lap_time[0], split_lap_time[1]
                lap_time = float(minutes) * 60 + float(seconds)
            else:
                lap_time = float(lap_time)

            if driver_name in lap_times_per_driver:
                lap_times_per_driver[driver_name].append(lap_time)
            else:
                lap_times_per_driver[driver_name] = [lap_time]

    # Calculate the average lap time per driver
    drivers = lap_times_per_driver.keys()
    average_lap_times = [np.mean(lap_times_per_driver[driver]) for driver in drivers]

    # Filter out lap times that are considered outliers
    filtered_average_lap_times = stats.zscore(average_lap_times) < threshold
    drivers = [driver for i, driver in enumerate(drivers) if filtered_average_lap_times[i]]
    average_lap_times = [lap_time for i, lap_time in enumerate(average_lap_times) if filtered_average_lap_times[i]]

    # Find the fastest lap time
    fastest_lap_time = min(average_lap_times)

    # Calculate the relative lap times by subtracting the fastest lap time from each average lap time
    relative_lap_times = [lap_time - fastest_lap_time for lap_time in average_lap_times]

    if dark_mode:
        # Enable dark mode for the plot
        plt.style.use('dark_background')

    # Generate a color list for each driver
    colors = plt.cm.get_cmap('tab20').colors[:len(drivers)]

    # Create a larger figure to increase space for x-axis labels
    plt.figure(figsize=(12, 6))

    # Create a bar chart of relative lap times per driver
    plt.bar(drivers, relative_lap_times, color=colors)
    plt.xlabel('Driver')
    plt.ylabel('Relative Lap Time')
    plt.title('Average Race Pace relative to Fastest Driver')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels and align to the right
    plt.tight_layout()  # Adjust spacing to prevent labels from overlapping
    plt.show()
