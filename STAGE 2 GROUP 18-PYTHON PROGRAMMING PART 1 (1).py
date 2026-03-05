# --- Utility Functions ---

def dms_to_dd(d, m, s):
    return d + m / 60 + s / 3600

def dd_to_dms(dd):
    d = int(dd)
    m = int((dd - d) * 60)
    s = round((dd - d - m / 60) * 3600, 2)
    return d, m, s

def dms_to_seconds(d, m, s):
    return d * 3600 + m * 60 + s

def seconds_to_dms(seconds):
    d = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = round(seconds % 60, 2)
    return d, m, s

def format_dms(d, m, s):
    return f"{int(d)}° {int(m)}' {s}\""

def get_int_input(prompt):
    while True:
        try:
            return int(input(f"{prompt}: "))
        except ValueError:
            print("  ❌ Invalid input. Please enter an integer.")

def get_dms_input(prompt):
    print(f"\n Enter {prompt} in DMS:")
    d = get_int_input("  Degrees")
    m = get_int_input("  Minutes")
    s = get_int_input("  Seconds")
    return d, m, s

def back_bearing(dd):
    return (dd + 180) % 360

# --- Adjustment Function ---

def adjust_bearings(averages, stations):
    print("\n Enter total angular misclosure to be distributed among bearings:")
    d = get_int_input("Degrees")
    m = get_int_input("Minutes")
    s = get_int_input("Seconds")

    total_error_sec = dms_to_seconds(d, m, s)
    adjust_stations = stations[1:]  # Exclude K1
    correction_per_station = total_error_sec / len(adjust_stations)

    print(f"\n Total Misclosure: {total_error_sec} seconds")
    print(f" Correction per station (excluding {stations[0]}): {correction_per_station:.2f} seconds\n")

    adjusted_bearings = {}
    adjusted_bearings[stations[0]] = averages[stations[0]]  # K1 remains unchanged

    for station in adjust_stations:
        avg_dms_str = averages[station]
        parts = avg_dms_str.replace("°", "").replace("'", "").replace("\"", "").split()
        d, m, s = map(float, parts)
        avg_sec = dms_to_seconds(d, m, s)
        adjusted_sec = avg_sec - correction_per_station
        adj_d, adj_m, adj_s = seconds_to_dms(adjusted_sec)
        adjusted_bearings[station] = format_dms(adj_d, adj_m, adj_s)

    return adjusted_bearings

# --- Main Program ---
print("TRIANGULATION BOOKING SHEET ")
# Prompt for the station number
station_str= input("please enter station number")
station="E"
print("station")
def main():
    stations = ['K1', 'C', 'D', 'F', 'G', 'K2']
    face_lefts = {}
    face_rights = {}
    averages = {}

    print("\n Step 1: Enter Face Left (FL) bearings for all stations:")
    for station in stations:
        face_lefts[station] = get_dms_input(f"Face Left (FL) for station {station}")

    print("\n Step 2: Enter Face Right (FR) bearings for all stations:")
    for station in reversed (stations):
        face_rights[station] = get_dms_input(f"Face Right (FR) for station {station}")

    print("\n Step 3: Calculating average bearings...")

    for station in stations:
        fl_dd = dms_to_dd(*face_lefts[station])
        fr_dd = dms_to_dd(*face_rights[station])
        fr_back = back_bearing(fr_dd)
        avg_dd = (fl_dd + fr_back) / 2
        avg_dms = dd_to_dms(avg_dd)
        averages[station] = format_dms(*avg_dms)

    # Show initial values BEFORE prompting for misclosure
    print("\n Bearings Table (Before Adjustment):\n")
    print("{:<22}".format("Observation"), end="")
    for station in stations:
        print(f"{station:<18}", end="")
    print("\n" + "-" * (22 + len(stations) * 18))

    for label, data in [("Face Left (FL)", face_lefts), 
                        ("Face Right (FR)", face_rights), 
                        ("Average Bearing", averages)]:
        print(f"{label:<22}", end="")
        for station in stations:
            if isinstance(data[station], tuple):
                print(f"{format_dms(*data[station]):<18}", end="")
            else:
                print(f"{data[station]:<18}", end="")
        print()

    # Step 4: Now ask for misclosure and apply adjustment
    print("\n Step 4: Enter misclosure to adjust the bearings:")
    adjusted = adjust_bearings(averages, stations)

    # Print final adjusted table
    print("\n Final Bearings Table (With Adjustment):\n")
    print("{:<22}".format("Observation"), end="")
    for station in stations:
        print(f"{station:<18}", end="")
    print("\n" + "-" * (22 + len(stations) * 18))

    for label, data in [("Adjusted Bearing", adjusted)]:
        print(f"{label:<22}", end="")
        for station in stations:
            print(f"{data[station]:<18}", end="")
        print()

# Run the program
if __name__ == "__main__":
    main()
