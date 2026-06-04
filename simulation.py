import numpy as np
import configparser
import sys
import os
from ultrasound import simulate_ascan, find_echo_time, calculate_depth

# Read configuration
config = configparser.ConfigParser()
config.read(sys.argv[1])

# Get parameters
velocity = float(config.get('settings', 'velocity'))
depth_start = float(config.get('settings', 'depth_start'))
depth_end = float(config.get('settings', 'depth_end'))
num_depths = int(config.get('settings', 'num_depths'))
frequency = float(config.get('settings', 'frequency'))
noise_level = float(config.get('settings', 'noise_level'))

# Get paths
data_folder = config.get('paths', 'data_folder')
os.makedirs(data_folder, exist_ok=True)
signal_file = config.get('paths', 'signal_file')
echo_times_file = config.get('paths', 'echo_times_file')
amplitudes_file = config.get('paths', 'amplitudes_file')

# Depths to simulate
depths = np.linspace(depth_start, depth_end, num_depths)

echo_times = []
amplitudes = []
signals = []

print("Running simulation...")
for i, depth in enumerate(depths):
    print(f"  Depth {i+1}/{num_depths}: {depth*100:.1f} cm")
    
    t, signal = simulate_ascan(depth, velocity, frequency, noise_level)
    signals.append(signal)
    
    echo_time = find_echo_time(signal)
    if echo_time:
        echo_times.append(echo_time)
        sample_idx = int(echo_time * 10e6)
        amplitudes.append(abs(signal[sample_idx]))
    else:
        echo_times.append(0)
        amplitudes.append(0)

# Save data
signals = np.array(signals)
echo_times = np.array(echo_times)
amplitudes = np.array(amplitudes)

np.save(signal_file, signals)
np.save(echo_times_file, echo_times)
np.save(amplitudes_file, amplitudes)

print("\n✅ Simulation complete!")
print(f"   Signals saved to: {signal_file}")
print(f"   Echo times saved to: {echo_times_file}")
print(f"   Amplitudes saved to: {amplitudes_file}")